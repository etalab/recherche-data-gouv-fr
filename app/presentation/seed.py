import json
import pandas as pd
from tempfile import NamedTemporaryFile

import click
from dependency_injector.wiring import inject, Provide
from flask import current_app, Flask
from flask.cli import with_appcontext
from app.containers import Container
from app.infrastructure.utils import download_catalog
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


@inject
def seed_db(search_client: SearchClient = Provide[Container.search_client]) -> None:

    click.echo("Cleaning indices.")

    search_client.delete_index()
    search_client.create_index()

    click.echo("Downloading catalogs.")

    with NamedTemporaryFile(delete=False) as dataset_fd:
        download_catalog(current_app.config['DATASET_CATALOG_URL'], dataset_fd)
    with NamedTemporaryFile(delete=False) as org_fd:
        download_catalog(current_app.config['ORG_CATALOG_URL'], org_fd)

    click.echo("Processing data.")

    with open(dataset_fd.name) as dataset_csvfile, open(org_fd.name) as org_csvfile:
        # Dataframe catalogue dataset
        dfd = pd.read_csv(dataset_csvfile, dtype=str, sep=";")
        # Dataframe catalogue orga
        dfo = pd.read_csv(org_csvfile, dtype="str", sep=";")

        # Récupèration de l'information "service public" depuis la colonne badge.
        # Attribution de la valeur 4 si c'est un SP, 1 si ça ne l'est pas
        dfo['es_orga_sp'] = dfo['badges'].apply(lambda x: 4 if 'public-service' in x else 1)

        # Sauvegarde en mémoire du dataframe avec uniquement les infos pertinentes
        dfo = dfo[['logo', 'id', 'es_orga_sp', 'metric.followers']]

        # Renommage de l'id de l'organisation et de la métrique followers
        dfo = dfo.rename(columns={'id': 'organization_id', 'metric.followers': 'es_orga_followers'})

        # Merge des deux dataframes (dataset et orga) pour n'en garder qu'un seul unique
        # La colonne de jointure est l'id de l'organisation. On fait un merge de type left join
        df = pd.merge(dfd, dfo, on='organization_id', how='left')

        # Modification de certaines colonnes pour optimiser par la suite la recherche ES
        # Les trois colonnes metric.views metric.followers et es_orga_followers sont converties en float
        # (elles étaient préalablement des string)
        df['metric.views'] = df['metric.views'].astype(float)
        df['metric.followers'] = df['metric.followers'].astype(float)
        df['es_orga_followers'] = df['es_orga_followers'].astype(float)

        # Afin qu'une métrique ne soit pas plus d'influente que l'autre, on normalise chacune des valeurs de ces colonnes
        # dans 5 catégorie (de 1 à 5)
        # Les "bins" utilisés pour chacune d'entre elles sont préparées "à la main". (difficile en effet d'avoir des bins
        # automatiques en sachant que l'immense majorité des datasets ont une valeur de 0 pour ces 3 métriques)
        # Comment lire :
        # Datasets de 0 vues = valeur 1
        # Datasets entre 1 et 49 vues = valeur 2
        # Datasets entre 50 et 499 vues = valeur 3
        # Datasets entre 500 et 4999 vues = Valeur 4
        # Datasets entre 5000 et 'nombre de vues max d'un dataset' = Valeur 5
        mvbins = [-1, 0, 50, 500, 5000, df['metric.views'].max()]
        df['es_dataset_views'] = pd.cut(df['metric.views'], mvbins, labels=list(range(1,6)))
        mfbins = [-1, 0, 2, 10, 40, df['metric.followers'].max()]
        df['es_dataset_followers'] = pd.cut(df['metric.followers'], mfbins, labels=list(range(1,6)))
        fobins = [-1, 0, 10, 50, 100, df['es_orga_followers'].max()]
        df['es_orga_followers'] = pd.cut(df['es_orga_followers'], fobins, labels=list(range(1,6)))

        # Création d'un champs "es_concat_title_org" concatenant le nom du titre et de l'organisation (de nombreuses recherches concatènent ces deux types de données)
        df['es_concat_title_org'] = df['title'] + ' ' + df['organization']

        # Création d'un champ "es_dataset_featured" se basant sur la colonne features. L'objectif étant de donner un poids plus grand aux datasets featured
        # Poids de 5 quand le dataset est featured, 1 sinon
        df['es_dataset_featured'] = df['featured'].apply(lambda x: 5 if x == 'True' else 1)

        # Sauvegarde en mémoire du dataframe avec uniquement les infos pertinentes
        df = df[['id', 'title', 'url', 'organization', 'organization_id', 'description', 'logo', 'es_orga_sp', 'es_orga_followers', 'es_dataset_views', 'es_dataset_followers', 'es_concat_title_org', 'es_dataset_featured']]
        # Convertion du dataframe en string json séparée par des \n
        df_as_json = df.to_json(orient='records', lines=True)

        click.echo("Seeding the database.")

        with click.progressbar(df_as_json.split('\n')) as bar:
            for json_document in bar:
                if json_document != '':
                    # Convertion de la string json en dictionnaire
                    jdict = json.loads(json_document)
                    search_client.index_dataset(Dataset(**jdict))

        click.echo("Done.")


@click.command("seed-db")
@with_appcontext
def seed_db_command() -> None:
    seed_db()


def init_app(app: Flask) -> None:
    app.cli.add_command(seed_db_command)
