import os
import time

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="AI Visual Quality Inspection",
    page_icon="🏭",
    layout="wide",
)


def get_api_data(api_url: str, endpoint: str, params=None):
    """Send a GET request to the FastAPI backend."""
    response = requests.get(
        f"{api_url}{endpoint}",
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def reset_api_data(api_url: str):
    """Reset counters and inspection history in FastAPI."""
    response = requests.post(
        f"{api_url}/reset",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


st.title("AI Visual Quality Inspection Dashboard")

st.caption(
    "Live production monitoring through the Dockerized "
    "FastAPI and PatchCore inspection service."
)

default_api_url = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)

st.sidebar.header("System Controls")

api_url = st.sidebar.text_input(
    "FastAPI address",
    value=default_api_url,
)

auto_refresh = st.sidebar.checkbox(
    "Automatic refresh",
    value=True,
)

refresh_interval = st.sidebar.slider(
    "Refresh interval in seconds",
    min_value=1,
    max_value=10,
    value=2,
)

if st.sidebar.button("Refresh now"):
    st.rerun()

if st.sidebar.button("Reset production counters"):
    try:
        reset_api_data(api_url)
        st.sidebar.success("Production counters reset.")
        time.sleep(0.5)
        st.rerun()
    except requests.RequestException as error:
        st.sidebar.error(f"Reset failed: {error}")


try:
    status = get_api_data(
        api_url=api_url,
        endpoint="/status",
    )

    history_response = get_api_data(
        api_url=api_url,
        endpoint="/history",
        params={"limit": 100},
    )

except requests.RequestException as error:
    st.error("Cannot connect to the FastAPI inspection service.")
    st.code(str(error))
    st.info(
        "Confirm that the FastAPI Docker container is running "
        "and that the API address is correct."
    )

    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

    st.stop()


status_column_1, status_column_2 = st.columns(2)

with status_column_1:
    if status.get("api_status") == "running":
        st.success("API Status: RUNNING")
    else:
        st.error("API Status: NOT AVAILABLE")

with status_column_2:
    if status.get("model_loaded"):
        st.success("PatchCore Model: LOADED")
    else:
        st.error("PatchCore Model: NOT LOADED")


st.subheader("Production Summary")

metric_1, metric_2, metric_3, metric_4, metric_5 = st.columns(5)

metric_1.metric(
    "Total Inspected",
    status.get("total_inspected", 0),
)

metric_2.metric(
    "OK",
    status.get("ok_count", 0),
    f'{status.get("ok_rate_percent", 0.0):.1f}%',
)

metric_3.metric(
    "Warning",
    status.get("warning_count", 0),
    f'{status.get("warning_rate_percent", 0.0):.1f}%',
)

metric_4.metric(
    "NG",
    status.get("ng_count", 0),
    f'{status.get("ng_rate_percent", 0.0):.1f}%',
)

metric_5.metric(
    "Average AI Time",
    f'{status.get("average_inference_time_seconds", 0.0):.3f} s',
)


st.subheader("Latest Inspection Result")

latest_result = status.get("latest_result")

if latest_result:
    decision = latest_result.get(
        "inspection_result",
        "Unknown",
    )

    if decision == "OK":
        st.success("LATEST PRODUCT: OK")
    elif decision == "Warning":
        st.warning("LATEST PRODUCT: WARNING")
    elif decision == "NG":
        st.error("LATEST PRODUCT: NG")
    else:
        st.info(f"LATEST PRODUCT: {decision}")

    latest_1, latest_2, latest_3, latest_4 = st.columns(4)

    latest_1.metric(
        "Filename",
        latest_result.get("uploaded_filename", "Unknown"),
    )

    latest_2.metric(
        "Anomaly Score",
        f'{latest_result.get("pred_score", 0.0):.4f}',
    )

    latest_3.metric(
        "AI Decision",
        decision,
    )

    latest_4.metric(
        "Inference Time",
        f'{latest_result.get("inference_time_seconds", 0.0):.3f} s',
    )

    st.write(
        "**Recommended action:**",
        latest_result.get("recommended_action", "Not available"),
    )

    st.write(
        "**Inspection timestamp:**",
        latest_result.get("timestamp", "Not available"),
    )

else:
    st.info(
        "No product has been inspected in the current production run."
    )


st.subheader("Recent Inspection History")

history_items = history_response.get("items", [])

if history_items:
    history_dataframe = pd.DataFrame(history_items)

    required_columns = [
        "timestamp",
        "uploaded_filename",
        "pred_score",
        "inspection_result",
        "recommended_action",
        "inference_time_seconds",
    ]

    for column in required_columns:
        if column not in history_dataframe.columns:
            history_dataframe[column] = None

    history_dataframe = history_dataframe[required_columns]

    history_dataframe["pred_score"] = (
        history_dataframe["pred_score"]
        .astype(float)
        .round(4)
    )

    history_dataframe["inference_time_seconds"] = (
        history_dataframe["inference_time_seconds"]
        .astype(float)
        .round(4)
    )

    history_dataframe = history_dataframe.rename(
        columns={
            "timestamp": "Timestamp",
            "uploaded_filename": "Product Image",
            "pred_score": "Anomaly Score",
            "inspection_result": "Decision",
            "recommended_action": "Recommended Action",
            "inference_time_seconds": "AI Time (s)",
        }
    )

    st.dataframe(
        history_dataframe,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("Inspection history is currently empty.")


st.caption(f"Dashboard API: {api_url}")

if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
