from pathlib import Path
import json

from inspection_engine import InspectionEngine


def main():
    project_root = Path(__file__).resolve().parents[1]

    inspection_engine = InspectionEngine(project_root)

    test_images = [
        project_root / "datasets" / "MVTecAD" / "metal_nut" / "test" / "good" / "000.png",
        project_root / "datasets" / "MVTecAD" / "metal_nut" / "test" / "bent" / "000.png",
    ]

    for image_path in test_images:
        result = inspection_engine.inspect_image(image_path)

        print("\nInspection result:")
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()