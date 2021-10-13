from dataclasses import dataclass

DEFAULT_ORG_NAME = 'Sans organisation'
DEFAULT_ORG_LOGO = 'https://static.data.gouv.fr/_themes/gouvfr/img/placeholders/organization.png?_=1.0.0'
DEFAULT_DESCRIPTION = 'Aucune déscription'


@dataclass
class Dataset:
    id: str
    title: str
    url: str
    orga_sp: int
    orga_followers: int
    dataset_views: int
    dataset_followers: int
    dataset_reuses: int
    dataset_featured: int
    concat_title_org: str
    organization_id: str
    temporal_coverage_start: str
    temporal_coverage_end: str
    spatial_granularity: str
    spatial_zones: str
    dataset_resources: int = 0
    description: str = DEFAULT_DESCRIPTION
    organization_logo: str = DEFAULT_ORG_LOGO
    organization: str = DEFAULT_ORG_NAME