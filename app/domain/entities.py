from dataclasses import dataclass, field

DEFAULT_ORG_NAME = 'Sans organisation'


@dataclass
class Dataset:
    id: str
    title: str
    url: str
    description: str
    es_orga_sp: int
    es_orga_followers: int
    es_dataset_views: int
    es_dataset_followers: int
    es_dataset_featured: int
    es_concat_title_org: str
    logo: str
    organization_id: str
    organization: str = DEFAULT_ORG_NAME