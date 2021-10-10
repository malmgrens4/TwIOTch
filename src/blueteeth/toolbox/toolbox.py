import os
from src.blueteeth.models.PhueLight import PhueLight
from src.blueteeth.models.RCCar import RCCar
from src.blueteeth.models.BalloonBox import BalloonBox
from src.blueteeth.models.SpaceNeedle import SpaceNeedle

camaro = None
needle = None
phue_light = None
balloon_box = None
space_needle = None

def get_phuelight():
    global phue_light
    if phue_light is None:
        phue_light = PhueLight()
    return phue_light


def get_camaro():
    global camaro
    if camaro is None:
        camaro = RCCar(os.environ['CAMARO_MAC'])
    return camaro


def get_needle():
    global needle
    if needle is None:
        needle = RCCar(os.environ['NEEDLE_MAC'])
    return needle


def get_balloon_box():
    global balloon_box
    if balloon_box is None:
        balloon_box = BalloonBox(os.environ['BALLOON_BOX_MAC'])
    return balloon_box


def get_space_needle():
    global space_needle
    if space_needle is None:
        space_needle = SpaceNeedle(os.environ['SPACE_NEEDLE_MAC'])
    return space_needle
