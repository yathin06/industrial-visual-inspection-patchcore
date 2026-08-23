from pathlib import Path


def check_mvtec_category(project_root: Path, category: str = "metal_nut") -> None:
    dataset_path = project_root / "datasets" / "MVTecAD" / category

    required_paths = [
        dataset_path / "train" / "good",
        dataset_path / "test" / "good",
        dataset_path / "ground_truth",
    ]

    print(f"Checking dataset path: {dataset_path}")

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset category folder not found:\n{dataset_path}\n\n"
            "Expected structure:\n"
            "datasets/MVTecAD/metal_nut/train/good\n"
            "datasets/MVTecAD/metal_nut/test/good\n"
            "datasets/MVTecAD/metal_nut/ground_truth\n"
        )

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(f"Missing required folder: {path}")

    train_good_count = len(list((dataset_path / "train" / "good").glob("*.png")))
    test_good_count = len(list((dataset_path / "test" / "good").glob("*.png")))

    defect_folders = [
        folder for folder in (dataset_path / "test").iterdir()
        if folder.is_dir() and folder.name != "good"
    ]

    print("\nDataset check passed.")
    print(f"Category: {category}")
    print(f"Normal training images: {train_good_count}")
    print(f"Normal test images: {test_good_count}")
    print("Defect types:")

    for folder in defect_folders:
        count = len(list(folder.glob("*.png")))
        print(f"  - {folder.name}: {count} images")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    check_mvtec_category(project_root, category="metal_nut")