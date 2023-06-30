from dataclasses import dataclass

from AdminApi.models.commands.branch import Branch
from AdminApi.models.commands.serializer import Serializer

"""It is a mock object created just for example"""


@dataclass
class Admin(Serializer):
    email: str
    password: str


@dataclass
class Company(Serializer):
    id: int
    name: str
    tariff: str
    admin: Admin
    branches: list[Branch]

    def __post_init__(self):
        if isinstance(self.branches, Branch):
            self.branches = [self.branches]
