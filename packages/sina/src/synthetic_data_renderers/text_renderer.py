from enum import Enum
from pathlib import Path
from typing import NamedTuple, Tuple

import numpy as np
from PIL import Image, ImageFont, ImageDraw
import scipy.ndimage as ndimage

from src.synthetic_data_renderers.page_renderer import (
    PageSpec,
    PageSizeSpec,
    PageCanvas,
    cmToPx
)

_ASSETS = Path(__file__).resolve().parent.parent.parent / "assets" / "fonts"
TARGET_DPI: int = 300
INCH_PER_CM: float = 1 / 2.54


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


def apply_elastic_transform(image: Image.Image, alpha: float, sigma: float) -> Image.Image:
    """
    Applies an elastic deformation field to a PIL image layer.
    """
    image_arr = np.array(image)
    shape = image_arr.shape

    # Generate smooth random displacement vectors
    dx = ndimage.gaussian_filter(
        (np.random.rand(*shape[:2]) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = ndimage.gaussian_filter(
        (np.random.rand(*shape[:2]) * 2 - 1), sigma, mode="constant", cval=0) * alpha

    # Map the grid indices
    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    indices = np.reshape(y + dy, (-1, 1)), np.reshape(x + dx, (-1, 1))

    # Remap channels (handles RGBA correctly to keep backgrounds transparent)
    distorted_channels = []
    for i in range(shape[2]):
        distorted_channel = ndimage.map_coordinates(
            image_arr[:, :, i], indices, order=1, mode='constant', cval=0)
        distorted_channels.append(distorted_channel.reshape(shape[:2]))

    return Image.fromarray(np.stack(distorted_channels, axis=-1))


def renderText(
    canvas: PageCanvas,
    ink: Writer,
    alpha: float = 15.0,
    sigma: float = 4.0
) -> Tuple[int, int, int, int]:
    """
    Renders font text onto a local patch, warps it elastically to mimic human handwriting, 
    and composites it onto the global page canvas.

    Returns:
        Tuple[int, int, int, int]: The adjusted (x_min, y_min, x_max, y_max) bounding box 
                                   of the distorted text for YOLO dataset labeling.
    """
    spec: PageSpec = canvas.page.value
    sz: PageSizeSpec = canvas.size.value

    # 1. Coordinate calculation relative to margins
    leftMarginX = cmToPx(spec.leftBorderOffset)
    rightMarginX = cmToPx(sz.w - spec.rightBorderOffset)
    topY = cmToPx(spec.topLineOffset)
    bottomY = cmToPx(sz.h - spec.bottomLineOffset)

    writingWidth = rightMarginX - leftMarginX
    writingHeight = bottomY - topY
    lineGap = writingHeight / max(spec.noOfRuledLines - 1, 1)

    target_x = int(leftMarginX + ink.col * writingWidth)
    target_y = int(topY + ink.row * lineGap)

    # 2. Get font dimensions to dynamically isolate font workspace
    pilFont = ink.font.load(ink.fontSizePx)

    # Use getbbox to find exact dimensions of the target string
    bbox = canvas.draw.textbbox((0, 0), ink.text, font=pilFont, anchor="ls")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Add an execution buffer padding around the patch to allow safe deformation space
    padding = int(max(alpha * 2, 20))
    patch_w = text_w + (padding * 2)
    patch_h = text_h + (padding * 2)

    # 3. Create isolated text transparent patch
    text_patch = Image.new("RGBA", (patch_w, patch_h), (0, 0, 0, 0))
    patch_draw = ImageDraw.Draw(text_patch)

    # Render text at baseline anchor inside the local patch coordinates
    render_x = padding - bbox[0]
    render_y = padding - bbox[1]
    patch_draw.text((render_x, render_y), ink.text,
                    font=pilFont, fill=ink.color, anchor="ls")

    # 4. Warping
    warped_patch = apply_elastic_transform(
        text_patch, alpha=alpha, sigma=sigma)

    # 5. Calculate real-world coordinates and blend into global canvas image
    # Aligning the temporary patch center with intended global text position
    paste_x = target_x - render_x
    paste_y = target_y - render_y
    canvas.img.paste(warped_patch, (paste_x, paste_y), warped_patch)

    # 6. Extract ground truth labels from alpha channel array for accurate YOLO bounding boxes
    alpha_channel = np.array(warped_patch)[:, :, 3]
    nonzero_coords = np.argwhere(alpha_channel > 0)

    if nonzero_coords.size > 0:
        y_indices, x_indices = nonzero_coords[:, 0], nonzero_coords[:, 1]
        bbox_x_min = paste_x + np.min(x_indices)
        bbox_y_min = paste_y + np.min(y_indices)
        bbox_x_max = paste_x + np.max(x_indices)
        bbox_y_max = paste_y + np.max(y_indices)
    else:
        # Fallback to structural estimation if text collapses completely
        bbox_x_min, bbox_y_min = target_x, target_y - text_h
        bbox_x_max, bbox_y_max = target_x + text_w, target_y

    return bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max
