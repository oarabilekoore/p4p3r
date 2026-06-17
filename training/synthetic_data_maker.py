from PIL import Image, ImageDraw
from types import SimpleNamespace
import os

def createA4Page():
    page = SimpleNamespace(
        width: 210,
        height: 297,
    )

