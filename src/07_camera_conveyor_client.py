from pathlib import Path
import argparse
import time
import requests


def collect_conveyor_images(project_root: Path):
    """
    Collect all metal_nut test images.

    These images simulate nuts arriving one-by-one
    on a conveyor under a vision camera.
    """
    test_root = project_root / "datasets" / "MVTecAD" / "metal_nut" / "test"

    image_paths = []

    for folder in sorted(test_root.iterdir()):
        if folder.is_dir():
            for image_path in sorted(folder.glob("*.png")):
                image_paths.append(image_path)

    return image_paths


def check_api_health(api_url: str):
    """
    Check whether the FastAPI server is running.
    """
    health_url = f"{api_url}/health"

    try:
        response = requests.get(health_url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Could not connect to API server at {health_url}\n"
            "Make sure FastAPI is running with:\n"
            "uvicorn api.inspection_api:app --reload\n\n"
            f"Original error: {error}"
        )


def send_image_to_api(api_url: str, image_path: Path):
    """
    Send one product image to the FastAPI inspection endpoint.
    """
    inspect_url = f"{api_url}/inspect"

    with open(image_path, "rb") as image_file:
        files = {
            "file": (
                image_path.name,
                image_file,
                "image/png",
            )
        }

        response = requests.post(inspect_url, files=files, timeout=60)
        response.raise_for_status()

    return response.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-url",
        type=str,
        default="http://127.0.0.1:8000",
        help="FastAPI server URL",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between conveyor images in seconds",
    )
    parser.add_argument(
        "--max-products",
        type=int,
        default=0,
        help="Maximum number of products to inspect. Use 0 for all images.",
    )

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]

    print("Checking FastAPI server...")
    health = check_api_health(args.api_url)
    print(f"API health: {health}")

    image_paths = collect_conveyor_images(project_root)

    if args.max_products > 0:
        image_paths = image_paths[: args.max_products]

    total = 0
    ok_count = 0
    warning_count = 0
    ng_count = 0

    print(f"\nTotal conveyor images available: {len(image_paths)}")
    print("Starting simulated camera/conveyor inspection...\n")

    for image_path in image_paths:
        result = send_image_to_api(args.api_url, image_path)

        total += 1

        inspection_result = result["inspection_result"]

        if inspection_result == "OK":
            ok_count += 1
        elif inspection_result == "Warning":
            warning_count += 1
        elif inspection_result == "NG":
            ng_count += 1

        print(
            f"[{total:03d}] "
            f"{image_path.parent.name}/{image_path.name} | "
            f"Score: {result['pred_score']:.4f} | "
            f"Result: {inspection_result} | "
            f"Action: {result['recommended_action']} | "
            f"API Time: {result['inference_time_seconds']:.3f}s"
        )

        time.sleep(args.delay)

    ok_rate = ok_count / total * 100 if total > 0 else 0
    warning_rate = warning_count / total * 100 if total > 0 else 0
    ng_rate = ng_count / total * 100 if total > 0 else 0

    print("\nFinal conveyor inspection summary:")
    print(f"Total inspected : {total}")
    print(f"OK              : {ok_count} ({ok_rate:.1f}%)")
    print(f"Warning         : {warning_count} ({warning_rate:.1f}%)")
    print(f"NG              : {ng_count} ({ng_rate:.1f}%)")


if __name__ == "__main__":
    main()