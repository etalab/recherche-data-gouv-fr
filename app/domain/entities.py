import dataclasses


@dataclasses.dataclass
class Dataset:
    id: str
    title: str
    acronym: str
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
    organization: str
    dataset_resources: int = 0
