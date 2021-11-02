from dataclasses import dataclass

DEFAULT_ORG_NAME = 'Sans organisation'
DEFAULT_ORG_LOGO = 'https://static.data.gouv.fr/_themes/gouvfr/img/placeholders/organization.png?_=1.0.0'
DEFAULT_DESCRIPTION = 'Aucune description'


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
    resources_count: int
    concat_title_org: str
    organization_id: str
    temporal_coverage_start: str
    temporal_coverage_end: str
    spatial_granularity: str
    spatial_zones: str
    description: str
    dataset_resources: int = 0
    organization_logo: str = DEFAULT_ORG_LOGO
    organization: str = DEFAULT_ORG_NAME

    def __post_init__(self):
        if self.description is None:
            self.description = DEFAULT_DESCRIPTION
