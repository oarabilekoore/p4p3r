import os
import shutil
from pathlib import Path
import sqlite3
import torch
from ultralytics import YOLO

MODEL_PATH = Path("./models/0610_0832_n30.pt")
DATASET_IMAGES = Path("../dataset/images/training")
DATASET_LABELS = Path("../dataset/labels")
TEST_IMAGES_DIR = Path("./test_images")
MODELS_OUTPUT_DIR = Path("../models")


def get_model_name() -> str:
    return input("Enter the name of the model: ")


def check_paths():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model weights not found at {MODEL_PATH}")
    if not DATASET_IMAGES.exists():
        raise FileNotFoundError(
            f"Dataset images not found at {DATASET_IMAGES}")
    if not DATASET_LABELS.exists():
        raise FileNotFoundError(
            f"Dataset labels not found at {DATASET_LABELS}")


def log_model_run(model_nmae: str):
    db = sqlite3.connect("../dataset/dataset.db")


def get_test_images() -> list[Path]:
    labeled_stems = {p.stem for p in DATASET_LABELS.glob("*.json")}
    return [
        img
        for img in DATASET_IMAGES.glob("*")
        if img.suffix in [".jpg", ".jpeg", ".png", ".webp"]
        and img.stem not in labeled_stems
    ]


def create_test_images_dir(images: list[Path]) -> Path:
    TEST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for img in images:
        shutil.copy(img, TEST_IMAGES_DIR / img.name)
    return TEST_IMAGES_DIR


def run_model(model_name: str):
    model = YOLO(MODEL_PATH)

    def custom_forward(x, *args, **kwargs):
        out = model.model._original_forward(x, *args, **kwargs)
        if isinstance(out, dict):
            return out.get("one2one", list(out.values())[0])
        return out

    if not hasattr(model.model, "_original_forward"):
        model.model._original_forward = model.model.forward
        model.model.forward = custom_forward

    test_images = get_test_images()
    test_image_dir = create_test_images_dir(test_images)

    results = model.predict(
        source=test_image_dir,
        conf=0.25,
        save=True,
        project="research",
        name=model_name,
        exist_ok=True,
    )
    return results, test_image_dir


def process_results(results, model_name: str):
    output_dir = MODELS_OUTPUT_DIR / model_name
    output_dir.mkdir(parents=True, exist_ok=True)

    image_perf = []
    for res in results:
        avg_conf = res.boxes.conf.mean().item() if len(res.boxes.conf) > 0 else 0.0
        image_perf.append(
            {
                "path": res.path,
                "conf": avg_conf,
                "saved_path": os.path.join(res.save_dir, os.path.basename(res.path)),
            }
        )

    image_perf.sort(key=lambda x: x["conf"], reverse=True)

    high_acc = image_perf[:5]
    low_acc = [img for img in image_perf if img["conf"] > 0][-5:]

    eval_dir = output_dir / "eval_samples"
    eval_dir.mkdir(parents=True, exist_ok=True)

    def copy_samples(samples, folder_name):
        target = eval_dir / folder_name
        target.mkdir(parents=True, exist_ok=True)
        for img in samples:
            if os.path.exists(img["saved_path"]):
                shutil.copy(img["saved_path"], target)

    copy_samples(high_acc, "high_accuracy")
    copy_samples(low_acc, "low_accuracy")

    all_confs = [img["conf"] for img in image_perf if img["conf"] > 0]
    avg_total_conf = sum(all_confs) / len(all_confs) if all_confs else 0

    readme_content = f"""# Model Performance Report: {model_name}
## Metadata
- **Model Path:** `{MODEL_PATH}`
- **Total Images Tested:** {len(results)}
- **Images with Detections:** {len(all_confs)}
## Performance Metrics
- **Mean Confidence (mConf):** {avg_total_conf:.4f}
- **Highest Confidence Image:** {f"{high_acc[0]["conf"]:.4f}" if high_acc else "N/A"}
- **Lowest Confidence Image (non-zero):** {f"{low_acc[-1]["conf"]:.4f}" if low_acc else "N/A"}
## Observations
- High accuracy samples are located in `./eval_samples/high_accuracy/`
- Low accuracy samples are located in `./eval_samples/low_accuracy/`
- Results generated on hardware: Intel Celeron N4020 (NNPACK Disabled)
"""

    readme_path = output_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write(readme_content)

    print(f"Evaluation complete. Files saved to {output_dir}")
    print(f"README created at {readme_path}")


check_paths()
model_name = get_model_name()
results, test_image_dir = run_model(model_name)
process_results(results, model_name)
