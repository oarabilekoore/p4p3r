from synthetic_data_renderers.text_renderer import Writer, Font, renderText
from synthetic_data_renderers.page_renderer import PageSize, Page, createPage, PageCanvas
import sys
from pathlib import Path
from PIL import ImageDraw

# Ensure the project root 'src' is in the python path
sys.path.append(str(Path(__file__).resolve().parent))

# Import your core layout structures
# Import your newly refactored elastic rendering structures


def run_irl_test_pipeline():
    print("Initializing Page Canvas (A4 Feint & Margin)...")
    # 1. Initialize a clean A4 ruled page with lines and margins
    canvas: PageCanvas = createPage(PageSize.A4, Page.FeintAndMargin4Quire)

    # 2. Define diverse sample payloads to test across different lines and columns
    test_lines = [
        Writer(row=2, col=0.05, text="Hello World! This is an elastic font test.",
               font=Font.PatrickHand, fontSizePx=65),
        Writer(row=5, col=0.10, text="Mathematical Formula: E = mc²",
               font=Font.CaveatMedium, fontSizePx=60, color="#2E1A47"),
        Writer(row=8, col=0.02, text="Skeletal Structure / Organic Chem Notes",
               font=Font.Pacifico, fontSizePx=55, color="#1A3E2E"),
        Writer(row=12, col=0.20, text="Table 1.1: Un-constructed matrix data structure",
               font=Font.JustAnotherHand, fontSizePx=80, color="#4A1A1A"),
        Writer(row=18, col=0.05, text="Testing edge-case alpha parameters for structural limits.",
               font=Font.CaveatBold, fontSizePx=58)
    ]

    print("Rendering and distorting fonts elastically...")
    # Create a separate draw object to overlay the validation bounding boxes
    box_draw = ImageDraw.Draw(canvas.img)

    for idx, ink in enumerate(test_lines):
        # Apply varying warp parameters to test limits
        # Higher alpha = more wobble. Higher sigma = smoother curves.
        alpha_val = 15.0 + (idx * 3.0)
        sigma_val = 4.0 + (idx * 0.5)

        # Render the warped text and extract the exact post-warp bounding box
        x_min, y_min, x_max, y_max = renderText(
            canvas=canvas,
            ink=ink,
            alpha=alpha_val,
            sigma=sigma_val
        )

        # 3. Draw verification bounding box (Simulates YOLO ground-truth confirmation)
        # This draws a bright green boundary showing exactly where the model thinks the text is
        box_draw.rectangle([x_min, y_min, x_max, y_max],
                           outline="#00FF00", width=3)
        print(f"   ↳ Rendered Line {ink.row} | Box: [{x_min}, {
              y_min}, {x_max}, {y_max}] (Alpha={alpha_val})")

    # 4. Save the generated evaluation output
    output_dir = Path("output_tests")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "synthetic_irl_test_result.png"
    canvas.img.save(output_path)
    print(f"Success! Diagnostic image saved to: {output_path.resolve()}")


run_irl_test_pipeline()
