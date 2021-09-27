from dataclasses import dataclass, field

DEFAULT_ORG_NAME = 'Sans organisation'


@dataclass
class Dataset:
    remote_id: str
    title: str
    url: str
    description: str
    featured: bool
    organization_name: str = DEFAULT_ORG_NAME
    organization_badges: list[str] = field(default_factory=list)
