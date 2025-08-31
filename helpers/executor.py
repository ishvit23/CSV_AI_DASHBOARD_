# helpers/executor.py
from typing import Dict, Any, Tuple, Optional, List
import pandas as pd
import numpy as np
from helpers.visualizer import generate_chart

# Allowed ops / function map (keep it short)
AllowedOps = {">", ">=", "<", "<=", "==", "!=", "in", "not in", "contains"}
FUNC_MAP = {
    "avg": "mean", "average": "mean", "mean": "mean",
    "sum": "sum", "count": "count", "max": "max", "min": "min",
    "median": "median", "std": "std"
}


def _to_num(v):
    try:
        return float(v)
    except Exception:
        return np.nan


def apply_filters(df: pd.DataFrame, fltrs: List[Dict[str, Any]]) -> pd.DataFrame:
    if not fltrs:
        return df
    out = df.copy()
    for f in fltrs:
        col, op, val = f.get("column"), f.get("op"), f.get("value")
        if col not in df.columns or op not in AllowedOps:
            continue
        s = out[col]
        if op in {"in", "not in"} and not isinstance(val, (list, tuple, set)):
            val = [val]
        try:
            if op == "contains" and s.dtype == "O":
                out = out[s.astype(str).str.contains(str(val), case=False, na=False)]
            elif op == "in":
                out = out[s.isin(val)]
            elif op == "not in":
                out = out[~s.isin(val)]
            elif op == "==":
                out = out[s == val]
            elif op == "!=":
                out = out[s != val]
            elif op == ">":
                out = out[pd.to_numeric(s, errors="coerce") > _to_num(val)]
            elif op == ">=":
                out = out[pd.to_numeric(s, errors="coerce") >= _to_num(val)]
            elif op == "<":
                out = out[pd.to_numeric(s, errors="coerce") < _to_num(val)]
            elif op == "<=":
                out = out[pd.to_numeric(s, errors="coerce") <= _to_num(val)]
        except Exception:
            continue
    return out


def _normalize_metrics(raw_metrics):
    metrics = {}
    for col, func in (raw_metrics or {}).items():
        mapped = FUNC_MAP.get(str(func).lower())
        if mapped:
            metrics[col] = mapped
    return metrics


def _flatten_columns(df: pd.DataFrame, metrics: Dict[str, str]) -> pd.DataFrame:
    # flatten multiindex or rename columns like Profit_mean
    new_cols = []
    for c in df.columns:
        if isinstance(c, tuple):
            base, agg = c
            new_cols.append(f"{base}_{agg}")
        elif c in metrics:
            new_cols.append(f"{c}_{metrics[c]}")
        else:
            new_cols.append(c)
    df.columns = new_cols
    return df


def execute_plan(df: pd.DataFrame, plan: Dict[str, Any]) -> Tuple[str, Optional[pd.DataFrame], Optional[Dict[str, Any]]]:
    """
    Returns:
       text: str
       table: pd.DataFrame or None
       chart: dict like {"base64": "...", "data":{"type":"bar","x":[], "y":[], ...}} or None
    """
    intent = plan.get("intent", "summary")
    cols = [c for c in plan.get("columns", []) if c in df.columns]
    metrics = _normalize_metrics(plan.get("metrics", {}))
    fltrs = plan.get("filters", [])
    topk_cfg = plan.get("topk", {})

    w = apply_filters(df, fltrs)
    chart = None

    # SUMMARY
    if intent == "summary":
        txt = _summary_text(w)
        return txt, w.head(10), None

    # AGGREGATE
    if intent == "aggregate" and metrics:
        try:
            group_cols = [c for c in cols if c not in metrics]
            if group_cols:
                table = w.groupby(group_cols, dropna=False).agg(metrics).reset_index()
            else:
                table = w.agg(metrics).to_frame().T

            table = _flatten_columns(table, metrics)

            # Build visualization if requested
            viz = plan.get("visualization", {})
            if viz:
                # infer x/y
                xcol = viz.get("x") or (group_cols[0] if group_cols else None)
                ycol = viz.get("y") or [c for c in table.columns if c not in group_cols][0] if table.shape[1] > 0 else None
                chart = generate_chart(table, chart_type=viz.get("type", "bar"), x=xcol, y=ycol)

            return f"Aggregated using {metrics}.", table, chart
        except Exception as e:
            return f"Could not aggregate: {e}", None, None

    # FILTER
    if intent == "filter":
        return "Applied filters.", w.head(50), None

    # TOPK
    if intent == "topk":
        by = topk_cfg.get("by")
        k = topk_cfg.get("k", 10)
        order = topk_cfg.get("order", "desc")
        try:
            if by not in w.columns:
                return f"Column {by} not found.", None, None
            num = pd.to_numeric(w[by], errors="coerce")
            if order == "desc":
                topn = w.loc[num.nlargest(int(k)).index]
            else:
                topn = w.loc[num.nsmallest(int(k)).index]
            return f"Top {k} rows by {by} ({order}).", topn, None
        except Exception as e:
            return f"TopK failed: {e}", None, None

    # COMPARISON
    if intent == "comparison" and metrics and cols:
        try:
            table = w.groupby(cols, dropna=False).agg(metrics).reset_index()
            table = _flatten_columns(table, metrics)
            return f"Comparison on {cols} with {metrics}.", table, None
        except Exception as e:
            return f"Comparison failed: {e}", None, None

    # FALLBACK
    return "I produced a safe summary because the plan couldn’t be executed confidently.", w.head(10), None


def _summary_text(df):
    nrows, ncols = df.shape
    nulls = df.isnull().sum().sort_values(ascending=False).head(5).to_dict()
    nums = df.select_dtypes(include=["number"])
    basics = []
    if not nums.empty:
        basics.append(f"Numeric columns: {list(nums.columns)[:5]}")
        basics.append(f"Means (sample): {nums.mean(numeric_only=True).round(2).to_dict()}")
    return f"Rows: {nrows}, Cols: {ncols}. Top missing: {nulls}. " + (" ".join(basics) if basics else "")
