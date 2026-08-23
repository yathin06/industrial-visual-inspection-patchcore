from pathlib import Path
import json

from inspection_engine import InspectionEngine


def collect_test_images(project_root: Path):
    """
    Collect all test images from MVTec metal_nut.

    These images simulate products coming one by one
    on a production conveyor.
    """
    test_root = project_root / "datasets" / "MVTecAD" / "metal_nut" / "test"

    image_paths = []

    for defect_folder in sorted(test_root.iterdir()):
        if defect_folder.is_dir():
            for image_path in sorted(defect_folder.glob("*.png")):
                image_paths.append(image_path)

    return image_paths


def main():
    project_root = Path(__file__).resolve().parents[1]

    inspection_engine = InspectionEngine(project_root)

    image_paths = collect_test_images(project_root)

    total = 0
    ok_count = 0
    warning_count = 0
    ng_count = 0
    total_time = 0.0

    print(f"Total images found: {len(image_paths)}")
    print("\nStarting simulated production inspection...\n")

    for image_path in image_paths:
        result = inspection_engine.inspect_image(image_path)

        total += 1
        total_time += result["inference_time_seconds"]

        if result["inspection_result"] == "OK":
            ok_count += 1
        elif result["inspection_result"] == "Warning":
            warning_count += 1
        elif result["inspection_result"] == "NG":
            ng_count += 1

        print(
            f"[{total:03d}] "
            f"{image_path.parent.name}/{image_path.name} | "
            f"Score: {result['pred_score']:.4f} | "
            f"Result: {result['inspection_result']} | "
            f"Time: {result['inference_time_seconds']:.3f}s"
        )

    average_time = total_time / total if total > 0 else 0
    ok_rate = ok_count / total * 100 if total > 0 else 0
    ng_rate = ng_count / total * 100 if total > 0 else 0

    summary = {
        "total_inspected": total,
        "ok_count": ok_count,
        "warning_count": warning_count,
        "ng_count": ng_count,
        "ok_rate_percent": round(ok_rate, 2),
        "ng_rate_percent": round(ng_rate, 2),
        "average_time_per_part_seconds": round(average_time, 4),
    }

    print("\nProduction inspection summary:")
    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    main()