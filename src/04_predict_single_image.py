from pathlib import Path
import argparse
import json

import cv2
import numpy as np
import torch

from anomalib.data import PredictDataset
from anomalib.engine import Engine
from anomalib.models import Patchcore


def tensor_to_scalar(value):
    """
    Convert Anomalib tensor output to a normal Python number.
    """
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().flatten()[0].item()

    if isinstance(value, (list, tuple)):
        return tensor_to_scalar(value[0])

    return value


def get_anomaly_map(prediction):
    """
    Extract anomaly map from Anomalib prediction output.
    """
    anomaly_map = prediction.anomaly_map

    if isinstance(anomaly_map, torch.Tensor):
        anomaly_map = anomaly_map.detach().cpu().numpy()

    anomaly_map = np.asarray(anomaly_map)

    # Handle possible shapes:
    # (1, 1, H, W), (1, H, W), or (H, W)
    if anomaly_map.ndim == 4:
        anomaly_map = anomaly_map[0, 0]
    elif anomaly_map.ndim == 3:
        anomaly_map = anomaly_map[0]

    return anomaly_map


def save_heatmap_overlay(image_path: Path, anomaly_map: np.ndarray, output_path: Path):
    """
    Save a side-by-side image:
    original image + anomaly heatmap overlay.
    """
    image_bgr = cv2.imread(str(image_path))

    if image_bgr is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    height, width = image_bgr.shape[:2]

    anomaly_map_resized = cv2.resize(anomaly_map, (width, height))

    anomaly_map_normalized = cv2.normalize(
        anomaly_map_resized,
        None,
        alpha=0,
        beta=255,
        norm_type=cv2.NORM_MINMAX,
    ).astype(np.uint8)

    heatmap_bgr = cv2.applyColorMap(anomaly_map_normalized, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(image_bgr, 0.6, heatmap_bgr, 0.4, 0)

    combined = np.hstack([image_bgr, overlay])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), combined)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        type=str,
        default=r"datasets\MVTecAD\metal_nut\test\bent\000.png",
        help="Path to image for inspection",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]

    image_path = project_root / args.image

    checkpoint_path = (
        project_root
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

    output_path = (
        project_root
        / "outputs"
        / "heatmaps"
        / f"{image_path.parent.name}_{image_path.stem}_patchcore_heatmap.png"
    )

    if not image_path.exists():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    print(f"Input image: {image_path}")
    print(f"Checkpoint: {checkpoint_path}")

    dataset = PredictDataset(
        path=image_path,
        image_size=(256, 256),
    )

    model = Patchcore(
        backbone="resnet18",
        layers=["layer2", "layer3"],
        coreset_sampling_ratio=0.1,
    )

    engine = Engine(
        accelerator="cpu",
        devices=1,
    )

    predictions = engine.predict(
        model=model,
        dataset=dataset,
        ckpt_path=str(checkpoint_path),
    )

    if predictions is None or len(predictions) == 0:
        raise RuntimeError("No prediction returned by Anomalib.")

    prediction = predictions[0]

    pred_score = float(tensor_to_scalar(prediction.pred_score))
    pred_label = int(tensor_to_scalar(prediction.pred_label))

    anomaly_map = get_anomaly_map(prediction)
    save_heatmap_overlay(image_path, anomaly_map, output_path)

    inspection_result, action = make_inspection_decision(pred_score)

    result = {
    	"image_path": str(image_path),
    	"pred_score": pred_score,
    	"pred_label": pred_label,
    	"pred_label_meaning": "anomalous" if pred_label == 1 else "normal",
    	"inspection_result": inspection_result,
    	"recommended_action": action,
   	"heatmap_path": str(output_path),
     }

    print("\nPrediction result:")
    print(json.dumps(result, indent=4))
def make_inspection_decision(pred_score: float):
    """
    Convert anomaly score into industrial inspection decision.

    OK:
        Part is accepted.

    Warning:
        Part is suspicious and should be reviewed manually.

    NG:
        Part is rejected.
    """
    ok_threshold = 0.50
    ng_threshold = 0.75

    if pred_score < ok_threshold:
        return "OK", "Part accepted"

    if pred_score < ng_threshold:
        return "Warning", "Manual inspection required"

    return "NG", "Part rejected"


if __name__ == "__main__":
    main()