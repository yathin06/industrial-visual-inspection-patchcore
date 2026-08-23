from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
import shutil
import sys
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile


# --------------------------------------------------
# Project paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.append(str(SRC_PATH))

from inspection_engine import InspectionEngine


# --------------------------------------------------
# Shared model and production state
# --------------------------------------------------
inspection_engine = None
state_lock = Lock()

production_state = {
    "total_inspected": 0,
    "ok_count": 0,
    "warning_count": 0,
    "ng_count": 0,
    "total_inference_time": 0.0,
    "latest_result": None,
}

inspection_history = deque(maxlen=500)


# --------------------------------------------------
# Load PatchCore once when the API starts
# --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global inspection_engine

    print("Loading PatchCore inspection engine...")

    inspection_engine = InspectionEngine(PROJECT_ROOT)

    print("PatchCore inspection engine loaded.")

    yield

    inspection_engine = None


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------
app = FastAPI(
    title="AI Visual Quality Inspection API",
    description=(
        "Dockerized API for real-time OK, Warning and NG "
        "visual quality inspection."
    ),
    version="2.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# Production-state functions
# --------------------------------------------------
def update_production_state(result: dict) -> None:
    """
    Update production counters after one product inspection.
    """
    with state_lock:
        production_state["total_inspected"] += 1

        production_state["total_inference_time"] += result[
            "inference_time_seconds"
        ]

        decision = result["inspection_result"]

        if decision == "OK":
            production_state["ok_count"] += 1

        elif decision == "Warning":
            production_state["warning_count"] += 1

        elif decision == "NG":
            production_state["ng_count"] += 1

        production_state["latest_result"] = result

        inspection_history.appendleft(result)


def create_status_response() -> dict:
    """
    Create the current production summary.
    """
    with state_lock:
        total = production_state["total_inspected"]
        ok_count = production_state["ok_count"]
        warning_count = production_state["warning_count"]
        ng_count = production_state["ng_count"]
        total_time = production_state["total_inference_time"]
        latest_result = production_state["latest_result"]

    average_time = total_time / total if total > 0 else 0.0

    ok_rate = ok_count / total * 100 if total > 0 else 0.0

    warning_rate = (
        warning_count / total * 100
        if total > 0
        else 0.0
    )

    ng_rate = ng_count / total * 100 if total > 0 else 0.0

    return {
        "api_status": "running",
        "model_loaded": inspection_engine is not None,
        "total_inspected": total,
        "ok_count": ok_count,
        "warning_count": warning_count,
        "ng_count": ng_count,
        "ok_rate_percent": round(ok_rate, 2),
        "warning_rate_percent": round(warning_rate, 2),
        "ng_rate_percent": round(ng_rate, 2),
        "average_inference_time_seconds": round(
            average_time,
            4,
        ),
        "latest_result": latest_result,
    }


# --------------------------------------------------
# API endpoints
# --------------------------------------------------
@app.get("/")
def root():
    """
    Return basic API information.
    """
    return {
        "service": "AI Visual Quality Inspection API",
        "version": "2.0.0",
        "documentation": "/docs",
    }


@app.get("/health")
def health_check():
    """
    Check whether the API and model are available.
    """
    return {
        "status": "running",
        "model_loaded": inspection_engine is not None,
    }


@app.get("/status")
def production_status():
    """
    Return production counters and the latest result.
    """
    return create_status_response()


@app.get("/history")
def production_history(limit: int = 50):
    """
    Return recent inspection results.
    """
    safe_limit = max(1, min(limit, 500))

    with state_lock:
        items = list(inspection_history)[:safe_limit]

    return {
        "count": len(items),
        "items": items,
    }


@app.post("/reset")
def reset_production():
    """
    Reset production counters and inspection history.
    """
    with state_lock:
        production_state["total_inspected"] = 0
        production_state["ok_count"] = 0
        production_state["warning_count"] = 0
        production_state["ng_count"] = 0
        production_state["total_inference_time"] = 0.0
        production_state["latest_result"] = None

        inspection_history.clear()

    return {
        "message": "Production counters reset successfully."
    }


@app.post("/inspect")
async def inspect_product_image(
    file: UploadFile = File(...),
):
    """
    Receive one product image, inspect it and update counters.
    """
    if inspection_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Inspection model is not loaded.",
        )

    original_filename = (
        file.filename or "uploaded_image.png"
    )

    file_extension = Path(
        original_filename
    ).suffix.lower()

    allowed_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
    }

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {file_extension}"
            ),
        )

    upload_dir = (
        PROJECT_ROOT
        / "outputs"
        / "api_uploads"
    )

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    saved_filename = (
        f"{uuid.uuid4().hex}{file_extension}"
    )

    saved_image_path = (
        upload_dir / saved_filename
    )

    try:
        with saved_image_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        prediction = inspection_engine.inspect_image(
            saved_image_path
        )

        result = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "uploaded_filename": original_filename,
            "saved_image_path": str(
                saved_image_path
            ),
            "pred_score": prediction[
                "pred_score"
            ],
            "pred_label": prediction[
                "pred_label"
            ],
            "pred_label_meaning": prediction[
                "pred_label_meaning"
            ],
            "inspection_result": prediction[
                "inspection_result"
            ],
            "recommended_action": prediction[
                "recommended_action"
            ],
            "inference_time_seconds": prediction[
                "inference_time_seconds"
            ],
        }

        update_production_state(result)

        return result

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

    finally:
        await file.close()
