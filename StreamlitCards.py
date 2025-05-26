import streamlit as st
import pandas as pd
import matplotlib.colors as mcolors

st.set_page_config(layout="wide")
st.title("Player Pitch Metrics Dashboard")

# --- Inputs ---
uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])
headshot_url = st.text_input("Enter player headshot URL:")

metrics_list = [
    "ExitVel", "90thExitVel", "Air EV",
    "LaunchAng", "HHLaunchAng", "xSLG"
]
contact_cols = [
    "Z-Contact%", "O-Contact%", "Contact%",
    "InZoneSwing%", "Chase%", "Zone%-Chase%",
    "InZoneSLG", "ChaseSLG"
]
pitch_col = "Pitch Type"
pitch_order = [
    "Fastball (4S)",
    "Fastball (2S) / Sinker",
    "Cutter",
    "Slider",
    "Soft (chg/splt)",
    "Breaking (cv/sld/sw)"
]

# Softer red→white→blue map
cmap_sum = mcolors.LinearSegmentedColormap.from_list(
    "", ["#7AB1EE", "#0F1116", "#D45F6A"]
)

# Per‑pitch/stat ranges for contact_cols
stat_ranges = {pt: {stat: {"min": None, "mid": None, "max": None} for stat in contact_cols} for pt in pitch_order}

# Fastball (4S)
stat_ranges["Fastball (4S)"]["Z-Contact%"]    = {"min": 75, "mid": 86, "max": 94.5}
stat_ranges["Fastball (4S)"]["O-Contact%"]    = {"min": 50, "mid": 71.2, "max": 90}
stat_ranges["Fastball (4S)"]["Contact%"]      = {"min": 66, "mid": 82.5, "max": 92}
stat_ranges["Fastball (4S)"]["InZoneSwing%"]  = {"min": 57, "mid": 65, "max": 82}
stat_ranges["Fastball (4S)"]["Chase%"]        = {"min": 33, "mid": 21.9, "max": 12.5}
stat_ranges["Fastball (4S)"]["Zone%-Chase%"]  = {"min": 32.2, "mid": 45.9, "max": 58.2}
stat_ranges["Fastball (4S)"]["InZoneSLG"]     = {"min": .270, "mid": .555, "max": .870}
stat_ranges["Fastball (4S)"]["ChaseSLG"]      = {"min": .150, "mid": .310, "max": .667}

# Fastball (2S) / Sinker
stat_ranges["Fastball (2S) / Sinker"]["Z-Contact%"]    = {"min": 66, "mid": 89, "max": 98}
stat_ranges["Fastball (2S) / Sinker"]["O-Contact%"]    = {"min": 50, "mid": 73.2, "max": 95}
stat_ranges["Fastball (2S) / Sinker"]["Contact%"]      = {"min": 69, "mid": 84.9, "max": 94}
stat_ranges["Fastball (2S) / Sinker"]["InZoneSwing%"]  = {"min": 44.7, "mid": 65.3, "max": 83}
stat_ranges["Fastball (2S) / Sinker"]["Chase%"]        = {"min": 43, "mid": 22.5, "max": 8}
stat_ranges["Fastball (2S) / Sinker"]["Zone%-Chase%"]  = {"min": 22, "mid": 42.8, "max": 66}
stat_ranges["Fastball (2S) / Sinker"]["InZoneSLG"]     = {"min": .100, "mid": .517, "max": .850}
stat_ranges["Fastball (2S) / Sinker"]["ChaseSLG"]      = {"min": .100, "mid": .312, "max": .800}

# Cutter
stat_ranges["Cutter"]["Z-Contact%"]    = {"min": 65, "mid": 82.3, "max": 98}
stat_ranges["Cutter"]["O-Contact%"]    = {"min": 25, "mid": 53, "max": 95}
stat_ranges["Cutter"]["Contact%"]      = {"min": 55, "mid": 73, "max": 90}
stat_ranges["Cutter"]["InZoneSwing%"]  = {"min": 46, "mid": 69.8, "max": 89}
stat_ranges["Cutter"]["Chase%"]        = {"min": 43, "mid": 27.2, "max": 10.5}
stat_ranges["Cutter"]["Zone%-Chase%"]  = {"min": 20.5, "mid": 42.6, "max": 61.5}
stat_ranges["Cutter"]["InZoneSLG"]     = {"min": .100, "mid": .581, "max": .950}
stat_ranges["Cutter"]["ChaseSLG"]      = {"min": .100, "mid": .229, "max": .667}

# Slider
stat_ranges["Slider"]["Z-Contact%"]    = {"min": 67, "mid": 82.2, "max": 95}
stat_ranges["Slider"]["O-Contact%"]    = {"min": 21, "mid": 47.8, "max": 75}
stat_ranges["Slider"]["Contact%"]      = {"min": 51, "mid": 69, "max": 84}
stat_ranges["Slider"]["InZoneSwing%"]  = {"min": 44, "mid": 61.7, "max": 78}
stat_ranges["Slider"]["Chase%"]        = {"min": 39.8, "mid": 26.7, "max": 14.4}
stat_ranges["Slider"]["Zone%-Chase%"]  = {"min": 16, "mid": 35.1, "max": 54}
stat_ranges["Slider"]["InZoneSLG"]     = {"min": .133, "mid": .522, "max": .790}
stat_ranges["Slider"]["ChaseSLG"]      = {"min": 0, "mid": .202, "max": .579}

# Soft (chg/splt)
stat_ranges["Soft (chg/splt)"]["Z-Contact%"]    = {"min": 63, "mid": 78.3, "max": 93}
stat_ranges["Soft (chg/splt)"]["O-Contact%"]    = {"min": 31, "mid": 55.2, "max": 81.8}
stat_ranges["Soft (chg/splt)"]["Contact%"]      = {"min": 51, "mid": 68.8, "max": 86}
stat_ranges["Soft (chg/splt)"]["InZoneSwing%"]  = {"min": 58, "mid": 73.5, "max": 87}
stat_ranges["Soft (chg/splt)"]["Chase%"]        = {"min": 41, "mid": 29.6, "max": 16.4}
stat_ranges["Soft (chg/splt)"]["Zone%-Chase%"]  = {"min": 19, "mid": 43.9, "max": 60}
stat_ranges["Soft (chg/splt)"]["InZoneSLG"]     = {"min": .170, "mid": .573, "max": 1.000}
stat_ranges["Soft (chg/splt)"]["ChaseSLG"]      = {"min": 0, "mid": .271, "max": .800}

# Breaking (cv/sld/sw)
stat_ranges["Breaking (cv/sld/sw)"]["Z-Contact%"]    = {"min": 69, "mid": 82.5, "max": 94.9}
stat_ranges["Breaking (cv/sld/sw)"]["O-Contact%"]    = {"min": 18, "mid": 48.4, "max": 72}
stat_ranges["Breaking (cv/sld/sw)"]["Contact%"]      = {"min": 48, "mid": 69.3, "max": 84.5}
stat_ranges["Breaking (cv/sld/sw)"]["InZoneSwing%"]  = {"min": 45, "mid": 59.5, "max": 79}
stat_ranges["Breaking (cv/sld/sw)"]["Chase%"]        = {"min": 39, "mid": 25.7, "max": 15}
stat_ranges["Breaking (cv/sld/sw)"]["Zone%-Chase%"]  = {"min": 17.5, "mid": 33.8, "max": 50}
stat_ranges["Breaking (cv/sld/sw)"]["InZoneSLG"]     = {"min": .120, "mid": .506, "max": .820}
stat_ranges["Breaking (cv/sld/sw)"]["ChaseSLG"]      = {"min": 0, "mid": .198, "max": .500}

# Header metric thresholds
header_ranges = {
    "ExitVel":      {"min": 82.0, "mid": 86.8, "max":100},
    "90thExitVel":  {"min": 101.5, "mid": 103.7, "max": 108},
    "Air EV":       {"min": 83,   "mid": 87.8, "max": 100},
    "LaunchAng":    {"min": 0.0,  "mid": 10.3, "max": 22.0},
    "HHLaunchAng":  {"min": 0.0,  "mid": 12.8, "max": 22.0},
    "xSLG":         {"min": 0.190,"mid": 0.388,"max": 1.000}
}

def style_contact_row(r: pd.Series):
    pitch = r.name
    styles = []
    for stat, v in r.items():
        if pitch == "Fastball (2S) / Sinker" and stat in ["InZoneSLG", "ChaseSLG"]:
            styles.append("background-color: #D45F6A")
            continue
        lo, mid, hi = stat_ranges[pitch][stat].values()
        if pd.isna(v): styles.append("")
        else:
            frac = (v - lo) / (hi - lo) if hi != lo else 0.5
            frac = max(0, min(1, frac))
            styles.append(f"background-color: {mcolors.to_hex(cmap_sum(frac))}")
    return styles

def style_header_row(r: pd.Series):
    styles = []
    for stat, v in r.items():
        lo, mid, hi = header_ranges[stat].values()
        if pd.isna(v): styles.append("")
        else:
            frac = (v - lo) / (hi - lo) if hi != lo else 0.5
            frac = max(0, min(1, frac))
            styles.append(f"background-color: {mcolors.to_hex(cmap_sum(frac))}")
    return styles

if uploaded_file:
    usecols = ["SplitBy", pitch_col, "P", "SLG"] + metrics_list + contact_cols
    df = pd.read_csv(uploaded_file, engine="python", usecols=usecols, on_bad_lines="skip")
    if missing := [c for c in usecols if c not in df.columns]:
        st.error(f"Missing columns: {missing}")
        st.stop()
    total = df[df["SplitBy"] == "TOTAL"].iloc[0] if not df[df["SplitBy"] == "TOTAL"].empty else None
    if total is None:
        st.error("No TOTAL row found.")
        st.stop()
    header_values = pd.Series({
        "ExitVel":      total["ExitVel"],
        "90thExitVel":  total["90thExitVel"],
        "Air EV":       total["Air EV"],
        "LaunchAng":    total["LaunchAng"],
        "HHLaunchAng":  total["HHLaunchAng"],
        "xSLG":         total["SLG"]
    }).apply(pd.to_numeric, errors="coerce")
    df = df[df["SplitBy"] != "TOTAL"].copy()
    df = df[df[pitch_col].isin(pitch_order)]
    df[["P"] + metrics_list] = df[["P"] + metrics_list].apply(pd.to_numeric, errors="coerce")
    df[contact_cols] = df[contact_cols].apply(lambda c: pd.to_numeric(c.astype(str).str.rstrip("%"), errors="coerce"))

    left, right = st.columns([1, 5])
    with left:
        if headshot_url and headshot_url.strip():
            try:
                st.image(headshot_url, use_container_width=True)
            except Exception as e:
                st.error(f"Unable to load headshot image: {e}")
        else:
            st.write("_No headshot URL provided_")
    header_df = pd.DataFrame([header_values], index=["Overall"]).loc[:, metrics_list]
    styled_header = header_df.style.apply(style_header_row, axis=1).format({**{m:"{:.1f}" for m in metrics_list if not m.endswith("SLG")}, **{m:"{:.3f}" for m in metrics_list if m.endswith("SLG")}}).set_properties(**{"text-align":"center"})
    with right:
        st.dataframe(styled_header, use_container_width=True)
    st.markdown("---")
    agg = {"P":"sum", **{c:"mean" for c in contact_cols}}
    grp = df.groupby(pitch_col).agg(agg).reindex(pitch_order)
    grp["P%"] = (grp["P"]/grp["P"].sum()*100).round(1)
    styled_contacts = grp[contact_cols].style.apply(style_contact_row, axis=1).format({**{c:"{:.1f}%" for c in contact_cols if not c.endswith("SLG")}, **{c:"{:.3f}" for c in contact_cols if c.endswith("SLG")}}).set_properties(**{"text-align":"center"})
    st.dataframe(styled_contacts, use_container_width=True)
else:
    st.info("Upload a CSV and enter a headshot URL to see the dashboard.")
