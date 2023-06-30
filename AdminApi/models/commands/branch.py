from dataclasses import dataclass, field
from typing import Optional

from random_words import RandomWords

from AdminApi.models.commands.serializer import Serializer
from enums.branch import DeliveryOptions


@dataclass
class Location(Serializer):
    lat: float = 11.8254998
    lng: float = 22.1178763


@dataclass
class Branch(Serializer):
    id: Optional[int] = None
    name: str = RandomWords().random_word()
    address: str = 'USA, Fl'
    addressDescription: Optional[str] = RandomWords().random_word()
    location: Location = Location()
    phones: list[int] = field(default_factory=lambda: [+319510626060])
    deliveryOptions: str = DeliveryOptions.PICKUP.value


@dataclass
class BranchUpdateDeliveryOptions(Serializer):
    branchId: Optional[int] = None
    deliveryOptions: list[str] = field(default_factory=lambda: [DeliveryOptions.PICKUP.value])


@dataclass
class BranchUpdate(Serializer):
    deliveryOptions: list[BranchUpdateDeliveryOptions] = field(default_factory=lambda: [BranchUpdateDeliveryOptions()])

    def __post_init__(self):
        if isinstance(self.deliveryOptions, BranchUpdateDeliveryOptions):
            self.deliveryOptions = [self.deliveryOptions]
