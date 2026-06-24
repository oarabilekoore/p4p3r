from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import NamedTuple

from PIL import Image, ImageDraw

_ASSETS = Path("../assets/fonts")
TARGET_DPI: int = 300
INCH_PER_CM: float = 1 / 2.54


@dataclass(frozen=True)
class PageSpec:
    noOfRuledLines: int
    topLineOffset: float
    bottomLineOffset: float
    leftBorderOffset: float
    rightBorderOffset: float


@dataclass(frozen=True)
class PageSizeSpec:
    w: float
    h: float


class Page(Enum):
    FeintAndMargin4Quire = PageSpec(
        noOfRuledLines=30,
        topLineOffset=2.2,
        bottomLineOffset=1.3,
        leftBorderOffset=2.1,
        rightBorderOffset=1.4,
    )


class PageSize(Enum):
    A4 = PageSizeSpec(w=21.0, h=29.7)


class PageCanvas(NamedTuple):
    img: Image.Image
    draw: ImageDraw.ImageDraw
    size: PageSize
    page: Page


def cmToPx(cm: float, dpi: int = TARGET_DPI) -> int:
    return int(cm * dpi * INCH_PER_CM)


def createPage(size: PageSize, page: Page) -> PageCanvas:
    spec: PageSpec = page.value
    sz: PageSizeSpec = size.value

    widthPx = cmToPx(sz.w)
    heightPx = cmToPx(sz.h)

    img = Image.new("RGB", (widthPx, heightPx), color="#F5F5F5")
    draw = ImageDraw.Draw(img)

    leftMarginX = cmToPx(spec.leftBorderOffset)
    rightMarginX = cmToPx(sz.w - spec.rightBorderOffset)
    topY = cmToPx(spec.topLineOffset)
    bottomY = cmToPx(sz.h - spec.bottomLineOffset)

    writingHeight = bottomY - topY
    lineGap = writingHeight / max(spec.noOfRuledLines - 1, 1)

    for i in range(spec.noOfRuledLines):
        y = int(topY + i * lineGap)
        draw.line([(0, y), (widthPx, y)], fill="#A5C7E8", width=2)

    draw.line([(leftMarginX, 0), (leftMarginX, heightPx)],
              fill="#E05050", width=4)
    draw.line([(rightMarginX, 0), (rightMarginX, heightPx)],
              fill="#E05050", width=2)

    return PageCanvas(img=img, draw=draw, size=size, page=page)
