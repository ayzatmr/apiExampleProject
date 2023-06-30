from enum import auto

from enums.base import AutoName


class DeliveryOptions(AutoName):
    PICKUP = auto()
    DELIVERY = auto()
