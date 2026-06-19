from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import NamedTuple

from PIL import Image, ImageDraw, ImageFont

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

    draw.line([(leftMarginX, 0), (leftMarginX, heightPx)], fill="#E05050", width=4)
    draw.line([(rightMarginX, 0), (rightMarginX, heightPx)], fill="#E05050", width=2)

    return PageCanvas(img=img, draw=draw, size=size, page=page)


class Font(Enum):
    JustAnotherHand = _ASSETS / "JustAnotherHand-Regular.ttf"
    PatrickHand = _ASSETS / "PatrickHand-Regular.ttf"
    Pacifico = _ASSETS / "Pacifico-Regular.ttf"
    CaveatMedium = _ASSETS / "Caveat-Medium.ttf"
    CaveatSemiBold = _ASSETS / "Caveat-SemiBold.ttf"
    CaveatBold = _ASSETS / "Caveat-Bold.ttf"
    CaveatRegular = _ASSETS / "Caveat-Regular.ttf"
    CaveatVariable = _ASSETS / "Caveat-VariableFont_wght.ttf"

    def load(self, sizePx: int) -> ImageFont.FreeTypeFont:
        if not self.value.exists():
            raise FileNotFoundError(f"Font file not found: {self.value}")
        return ImageFont.truetype(str(self.value), size=sizePx)


class Writer(NamedTuple):
    row: int
    col: float
    text: str
    font: Font
    fontSizePx: int = 60
    color: str = "#1A1A2E"


def renderText(canvas: PageCanvas, ink: Writer) -> None:
    spec: PageSpec = canvas.page.value
    sz: PageSizeSpec = canvas.size.value

    leftMarginX = cmToPx(spec.leftBorderOffset)
    rightMarginX = cmToPx(sz.w - spec.rightBorderOffset)
    topY = cmToPx(spec.topLineOffset)
    bottomY = cmToPx(sz.h - spec.bottomLineOffset)

    writingWidth = rightMarginX - leftMarginX
    writingHeight = bottomY - topY
    lineGap = writingHeight / max(spec.noOfRuledLines - 1, 1)

    x = int(leftMarginX + ink.col * writingWidth)
    y = int(topY + ink.row * lineGap)

    pilFont = ink.font.load(ink.fontSizePx)
    canvas.draw.text((x, y), ink.text, font=pilFont, fill=ink.color, anchor="ls")


canvas = createPage(PageSize.A4, Page.FeintAndMargin4Quire)

renderText(
    canvas,
    Writer(
        row=0,
        col=0.4,
        text="Hello, PaperMd",
        font=Font.Pacifico,
    ),
)

out = Path("output_page.png")
canvas.img.save(out, dpi=(TARGET_DPI, TARGET_DPI))
print(f"Saved → {out}")
