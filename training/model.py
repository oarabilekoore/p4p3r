from ultralytics import YOLO
from label_studio_ml.utils import get_local_path
from label_studio_ml.model import LabelStudioMLBase
import os
:  # This file is used by the annotation-helper.sh script
    # it is used by Label-Studio to help me whilst i label
    # elements in notes so that i move faster..


LABEL_MAP = {
    0: "Abandon",
    1: "Plain_Text",
    2: "Formula",
    3: "Figure",
    4: "Table",
    5: "Link",
}


class YOLOv11Backend(LabelStudioMLBase):
    def setup(self):
        self.set_model_loaded("YOLOv11")
        self.model_path = os.path.join(os.path.dirname(__file__), "latest.pt")

        if not os.path.exists(self.model_path):
            print(f"ERROR: Model weights not found at {self.model_path}")

        self.model = YOLO(self.model_path)

        if not hasattr(self.model.model, "_original_forward"):
            self.model.model._original_forward = self.model.model.forward

            def custom_forward(x, *args, **kwargs):
                out = self.model.model._original_forward(x, *args, **kwargs)
                return (
                    out.get("one2one", list(out.values())[0])
                    if isinstance(out, dict)
                    else out
                )

            self.model.model.forward = custom_forward

    def predict(self, tasks, **kwargs):
        predictions = []
        for task in tasks:
            image_url = task["data"]["image"]
            image_path = get_local_path(image_url)

            results = self.model.predict(image_path, conf=0.45, imgsz=320)[0]
            result_list = []
            img_width, img_height = results.orig_shape

            for box in results.boxes:
                xyxy = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])

                if cls_id not in LABEL_MAP:
                    continue

                x = (xyxy[0] / img_width) * 100
                y = (xyxy[1] / img_height) * 100
                w = ((xyxy[2] - xyxy[0]) / img_width) * 100
                h = ((xyxy[3] - xyxy[1]) / img_height) * 100

                result_list.append(
                    {
                        "from_name": "label",
                        "to_name": "image",
                        "type": "rectanglelabels",
                        "score": conf,
                        "value": {
                            "rectanglelabels": [LABEL_MAP[cls_id]],
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h,
                            "rotation": 0,
                        },
                    }
                )

            predictions.append({"result": result_list})
        return predictions
