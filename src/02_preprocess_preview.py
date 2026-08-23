from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

def load_image(image_path: Path):
    """
    Load image using OpenCV.

    OpenCV loads images in BGR format by default.
    Most deep learning and visualization tools expect RGB format.
    """
    image_bgr = cv2.imread(str(image_path))

    if image_bgr is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    return image_bgr


def preprocess_image(image_bgr, target_size=(256, 256)):
    """
    Basic preprocessing step.

    1. Convert BGR to RGB
    2. Resize image to fixed size

    Fixed image size is important because deep learning models expect
    consistent input dimensions.
    """
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, target_size, interpolation=cv2.INTER_AREA)

    return image_rgb, image_resized


def get_first_png(folder_path: Path) -> Path:
    images = sorted(folder_path.glob("*.png"))

    if not images:
        raise FileNotFoundError(f"No PNG images found in: {folder_path}")

    return images[0]


def main():
    project_root = Path(__file__).resolve().parents[1]
    dataset_path = project_root / "datasets" / "MVTecAD" / "metal_nut"

    normal_image_path = get_first_png(dataset_path / "train" / "good")

    defect_folders = [
        folder for folder in (dataset_path / "test").iterdir()
        if folder.is_dir() and folder.name != "good"
    ]

    defect_folders = sorted(defect_folders)
    defect_image_path = get_first_png(defect_folders[0])

    normal_bgr = load_image(normal_image_path)
    defect_bgr = load_image(defect_image_path)

    normal_rgb, normal_resized = preprocess_image(normal_bgr)
    defect_rgb, defect_resized = preprocess_image(defect_bgr)

    print("Normal image:")
    print(f"  Path: {normal_image_path}")
    print(f"  Original shape: {normal_bgr.shape}")
    print(f"  Preprocessed shape: {normal_resized.shape}")

    print("\nDefect image:")
    print(f"  Path: {defect_image_path}")
    print(f"  Original shape: {defect_bgr.shape}")
    print(f"  Preprocessed shape: {defect_resized.shape}")

    output_dir = project_root / "outputs" / "predictions"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "preprocessing_preview.png"

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    axes[0, 0].imshow(normal_rgb)
    axes[0, 0].set_title("Normal image - original")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(normal_resized)
    axes[0, 1].set_title("Normal image - resized 256x256")
    axes[0, 1].axis("off")

    axes[1, 0].imshow(defect_rgb)
    axes[1, 0].set_title(f"Defect image - original ({defect_image_path.parent.name})")
    axes[1, 0].axis("off")

    axes[1, 1].imshow(defect_resized)
    axes[1, 1].set_title("Defect image - resized 256x256")
    axes[1, 1].axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"\nPreprocessing preview saved to: {output_path}")


if __name__ == "__main__":
    main()