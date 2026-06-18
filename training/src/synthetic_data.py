from PIL import Image, ImageDraw, ImageFont
from types import SimpleNamespace
from typing import NamedTuple
from path import Path
from enum import Enum
import os

TARGET_DPI = 300


def create_a4_page() -> Image, ImageDraw:
    pageDimensions = SimpleNamespace(
        w=21.0,
        h=29.7,
        topLineOffset=2.2,
        bottomLineOffset=1.3,
        leftBorderLineOffset=2.1,
        rightBorderLineOffset=1.4,
        noOfRuledLines=30  # 32 lines in total including the top adnd bottomL
    )

    def cmToPx(cm: float) -> int:
        return int(round((cm * TARGET_DPI)/2.54))
    width_px = cmToPx(pageDimensions.w)
    height_px = cmToPx(pageDimensions.h)

    page = Image.new("RGB", (width_px, height_px), color="#F5F5F5")
    draw = ImageDraw.Draw(page)

    left_margin_x = cmToPx(pageDimensions.leftBorderLineOffset)
    right_margin_x = cmToPx(
        pageDimensions.w - pageDimensions.rightBorderLineOffset)
    top_line_y = cmToPx(pageDimensions.topLineOffset)
    bottom_line_y = cmToPx(pageDimensions.h - pageDimensions.bottomLineOffset)

    writing_zone_height = bottom_line_y - top_line_y
    line_gap = writing_zone_height / (pageDimensions.noOfRuledLines - 1)

    for i in range(pageDimensions.noOfRuledLines):
        current_y = int(top_line_y + (i * line_gap))
        """draw all horizontal lines"""
        draw.line([0, current_y, width_px, current_y], fill="#A5C7E8", width=2)
        # Left vertical margin line (Thicker prominent red)
        draw.line([left_margin_x, 0, left_margin_x, height_px],
                  fill="#E05050", width=4)
        # Right vertical margin line (Thinner structural red boundary
        draw.line([right_margin_x, 0, right_margin_x,
                  height_px], fill="#E05050", width=2)

    return page, draw


class Font(Enum):
    JustAnotherHand = Path("./assets/JustAnotherHand-Regular.ttf")
    PatrickHandRegular = Path("./assets/PatrickHand-Regular.ttf")
    PacifoRegular = Path("./assets/Pacifico-Regular.ttf")
    CaveatMedium = Path("./assets/Caveat-Medium.ttf")
    CaveatSemiBold = Path("./assets/Caveat-SemiBold.ttf")
    CaveatBold = Path("./assets/Caveat-Bold.ttf")
    CaveatRegular = Path("./assets/Caveat-Regular.ttf")
    CaveatVariable = Path("./assets/Caveat-VariableFont_wght.ttf")


for font in Font:
    if not font.exists():
        raise FileNotFoundError(f"Font misssing in assets dir: {font}")


class Writer(NamedTuple):
    row: int
    col: int
    text: str


def render_text(pen: ImageDraw, ink: Writer):


page, pen = create_a4_page()
writer = Writer(row=2, col=0, text="Hello World")

render_text(pen, writer)
