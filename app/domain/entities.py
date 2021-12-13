import dataclasses

DEFAULT_ORG_NAME = 'Sans organisation'
DEFAULT_ORG_LOGO = 'https://static.data.gouv.fr/_themes/gouvfr/img/placeholders/organization.png?_=1.0.0'
DEFAULT_DESCRIPTION = 'Aucune description'


@dataclasses.dataclass
class Organization:
    id: str
    name: str
    description: str
    url: str
    orga_sp: int
    created_at: str
    orga_followers: int
    orga_datasets: int


@dataclasses.dataclass
class Dataset:
    id: str
    title: str
    acronym: str
    url: str
    created_at: str
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
    organization_logo: str = DEFAULT_ORG_LOGO
    organization: str = DEFAULT_ORG_NAME

    def __post_init__(self):
        if self.description is None:
            self.description = DEFAULT_DESCRIPTION


@dataclasses.dataclass
class Reuse:
    id: str
    title: str
    slug: str
    url: str
    created_at: str
    orga_sp: int
    orga_followers: int
    reuse_views: int
    reuse_followers: int
    reuse_datasets: int
    reuse_featured: int
    concat_title_org: str
    organization_id: str
    description: str
    organization: str = DEFAULT_ORG_NAME
