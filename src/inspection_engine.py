from pathlib import Path
import time

import torch

from anomalib.data import PredictDataset
from anomalib.engine import Engine
from anomalib.models import Patchcore


def tensor_to_scalar(value):
    """
    Convert PyTorch tensor output to a normal Python number.
    """
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().flatten()[0].item()

    if isinstance(value, (list, tuple)):
        return tensor_to_scalar(value[0])

    return value


def make_inspection_decision(pred_score: float):
    """
    Convert anomaly score into factory-style decision.
    """
    ok_threshold =  
    ng_threshold = 0.75

    if pred_score < ok_threshold:
        return "OK", "Part accepted"

    if pred_score < ng_threshold:
        return "Warning", "Manual inspection required"

    return "NG", "Part rejected"


class InspectionEngine:
    """
    Real-time inspection engine.

    The model is loaded once when the class is created.
    Then inspect_image() can be called repeatedly for many images.
    """

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)

        self.checkpoint_path = (
            self.project_root
            / "models"
            / "patchcore_metal_nut"
            / "Patchcore"
            / "MVTecAD"
            / "metal_nut"
            / "v1"
            / "weights"
            / "lightning"
            / "model.ckpt"
        )

        if not self.checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {self.checkpoint_path}")

        self.model = Patchcore.load_from_checkpoint(
          checkpoint_path=str(self.checkpoint_path),
          backbone="resnet18",
          layers=["layer2", "layer3"],
          coreset_sampling_ratio=0.01,
          map_location="cpu",
          weights_only=False,
        )

        self.engine = Engine(
            accelerator="cpu",
            devices=1,
        )

    def inspect_image(self, image_path):
        """
        Inspect one image and return score, label, decision, and inference time.
        """
        image_path = Path(image_path)

        if not image_path.is_absolute():
            image_path = self.project_root / image_path

        if not image_path.exists():
            raise FileNotFoundError(f"Input image not found: {image_path}")

        dataset = PredictDataset(
            path=image_path,
            image_size=(256, 256),
        )

        start_time = time.perf_counter()

        predictions = self.engine.predict(
            model=self.model,
            dataset=dataset,
        )

        inference_time = time.perf_counter() - start_time

        if predictions is None or len(predictions) == 0:
            raise RuntimeError("No prediction returned by Anomalib.")

        prediction = predictions[0]

        pred_score = float(tensor_to_scalar(prediction.pred_score))
        pred_label = int(tensor_to_scalar(prediction.pred_label))
        pred_label_meaning = "anomalous" if pred_label == 1 else "normal"

        inspection_result, recommended_action = make_inspection_decision(pred_score)

        return {
            "image_path": str(image_path),
            "pred_score": pred_score,
            "pred_label": pred_label,
            "pred_label_meaning": pred_label_meaning,
            "inspection_result": inspection_result,
            "recommended_action": recommended_action,
            "inference_time_seconds": inference_time,
        }