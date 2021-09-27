import ast
import csv
from tempfile import NamedTemporaryFile

import click
from dependency_injector.wiring import inject, Provide
from flask import current_app, Flask
from flask.cli import with_appcontext
from app.containers import Container
from app.utils import download_catalog
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


@inject
def seed_db(search_client: SearchClient = Provide[Container.search_client]) -> None:
    with NamedTemporaryFile(delete=False) as dataset_fd:
        download_catalog(current_app.config['DATASET_CATALOG_URL'], dataset_fd)
    with NamedTemporaryFile(delete=False) as org_fd:
        download_catalog(current_app.config['ORG_CATALOG_URL'], org_fd)

    with open(dataset_fd.name) as dataset_csvfile, open(org_fd.name) as org_csvfile:
        dataset_rows = list(csv.DictReader(dataset_csvfile, delimiter=';'))
        org_rows = list(csv.DictReader(org_csvfile, delimiter=';'))

        search_client.clean_index("dataset")

        with click.progressbar(dataset_rows) as bar:
            for dataset in bar:
                body = {
                    'remote_id': dataset['id'],
                    'title': dataset['title'],
                    'url': dataset['url'],
                    'description': dataset['description'],
                    'featured': dataset['featured']
                }
                for org in org_rows:
                    if org['id'] == dataset['organization_id']:
                        body.update({
                            'organization_name': org['name'],
                            'organization_badges': ast.literal_eval(org['badges'])
                        })
                search_client.index(Dataset(**body), "dataset")


@click.command("seed-db")
@with_appcontext
def seed_db_command() -> None:
    click.echo("Seeding the database.")
    seed_db()
    click.echo("Done.")


def init_app(app: Flask) -> None:
    app.cli.add_command(seed_db_command)
