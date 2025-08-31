# helpers/visualizer.py
import io
import base64
from typing import Optional, Dict, Any
import matplotlib.pyplot as plt
import pandas as pd


def generate_chart(
    df: pd.DataFrame,
    chart_type: str = "bar",
    x: Optional[str] = None,
    y: Optional[str] = None,
    figsize=(8, 4),
) -> Dict[str, Any]:
    """
    Generate a chart and return:
      {
        "base64": "<png base64 string>",
        "data": {"type":"bar","x":[...],"y":[...], "x_label": ..., "y_label": ...}
      }

    df: the dataframe to plot (should have columns x and y)
    chart_type: "bar" | "line" | "pie"
    x: column to use for x-axis
    y: column to use for y-axis
    """
    if x is None and chart_type != "pie":
        # try to pick a reasonable x
        x = df.columns[0] if len(df.columns) > 0 else None
    if y is None and chart_type != "pie":
        # pick last column if not specified
        y = df.columns[-1] if len(df.columns) > 0 else None

    # Prepare chart_data to return (frontend can use this for interactive plotting)
    chart_data = {"type": chart_type, "x": None, "y": None, "x_label": x, "y_label": y}

    # Create figure using matplotlib
    fig, ax = plt.subplots(figsize=figsize)

    try:
        if chart_type == "bar":
            ax.bar(df[x].astype(str), pd.to_numeric(df[y], errors="coerce"))
        elif chart_type == "line":
            ax.plot(df[x], pd.to_numeric(df[y], errors="coerce"), marker="o")
        elif chart_type == "pie":
            # For pie we only need y and labels from x
            ax.pie(pd.to_numeric(df[y], errors="coerce"), labels=df[x].astype(str), autopct="%1.1f%%")
        else:
            # default to bar
            ax.bar(df[x].astype(str), pd.to_numeric(df[y], errors="coerce"))

        ax.set_xlabel(x if x else "")
        ax.set_ylabel(y if y else "")
        ax.set_title(f"{chart_type.title()} of {y} by {x}" if x and y else f"{chart_type.title()} chart")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
    except Exception:
        # If plotting fails, create a blank figure with a message
        fig.clf()
        fig.text(0.5, 0.5, "Could not render chart", ha="center", va="center")

    # Convert fig to base64 PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = buf.getvalue()
    base64_png = base64.b64encode(img_bytes).decode("utf-8")
    plt.close(fig)

    # Prepare chart_data values (x,y arrays) safely
    try:
        chart_data["x"] = df[x].astype(str).tolist() if x in df.columns else None
        chart_data["y"] = pd.to_numeric(df[y], errors="coerce").fillna(0).tolist() if y in df.columns else None
    except Exception:
        chart_data["x"] = None
        chart_data["y"] = None

    return {"base64": base64_png, "data": chart_data}
