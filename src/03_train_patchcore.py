from pathlib import Path

from anomalib.data import MVTecAD
from anomalib.engine import Engine
from anomalib.models import Patchcore


def main():
    """
    Train PatchCore on MVTec AD metal_nut.

    PatchCore is an anomaly detection model.
    It learns normal image features from train/good images.
    During testing, it compares test images against normal features
    and produces anomaly scores and anomaly maps.
    """

    project_root = Path(__file__).resolve().parents[1]

    dataset_root = project_root / "datasets" / "MVTecAD"
    model_output_dir = project_root / "models" / "patchcore_metal_nut"

    print(f"Dataset root: {dataset_root}")
    print(f"Model output directory: {model_output_dir}")

    datamodule = MVTecAD(
        root=dataset_root,
        category="metal_nut",
        train_batch_size=4,
        eval_batch_size=4,
        num_workers=0,
    )

    model = Patchcore(
        backbone="resnet18",
        layers=["layer2", "layer3"],
        coreset_sampling_ratio=0.01,
    )

    engine = Engine(
        default_root_dir=model_output_dir,
        accelerator="cpu",
        devices=1,
        max_epochs=1,
    )

    print("\nStarting PatchCore training...")
    engine.fit(
        model=model,
        datamodule=datamodule,
    )

    print("\nStarting PatchCore testing...")
    engine.test(
        model=model,
        datamodule=datamodule,
    )

    print("\nPatchCore training and testing completed.")
    print(f"Outputs saved in: {model_output_dir}")


if __name__ == "__main__":
    main()