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

# Per-pitch/stat ranges for contact_cols
stat_ranges = {pt: {stat: {"min": None, "mid": None, "max": None} for stat in contact_cols} for pt in pitch_order}

# Fastball (4S)
stat_ranges["Fastball (4S)"]["Z-Contact%"] = {"min": 75, "mid": 86, "max": 94.5}
stat_ranges["Fastball (4S)"]["O-Contact%"] = {"min": 50, "mid": 71.2, "max": 90}
stat_ranges["Fastball (4S)"]["Contact%"] = {"min": 66, "mid": 82.5, "max": 92}
stat_ranges["Fastball (4S)"]["InZoneSwing%"] = {"min": 57, "mid": 65, "max": 82}
stat_ranges["Fastball (4S)"]["Chase%"] = {"min": 33, "mid": 21.9, "max": 12.5}
stat_ranges["Fastball (4S)"]["Zone%-Chase%"] = {"min": 32.2, "mid": 45.9, "max": 58.2}
stat_ranges["Fastball (4S)"]["InZoneSLG"] = {"min": .270, "mid": .555, "max": .870}
stat_ranges["Fastball (4S)"]["ChaseSLG"] = {"min": .150, "mid": .310, "max": .667}

# Fastball (2S) / Sinker
stat_ranges["Fastball (2S) / Sinker"]["Z-Contact%"] = {"min": 66, "mid": 89, "max": 98}
stat_ranges["Fastball (2S) / Sinker"]["O-Contact%"] = {"min": 50, "mid": 73.2, "max": 95}
stat_ranges["Fastball (2S) / Sinker"]["Contact%"] = {"min": 69, "mid": 84.9, "max": 94}
stat_ranges["Fastball (2S) / Sinker"]["InZoneSwing%"] = {"min": 44.7, "mid": 65.3, "max": 83}
stat_ranges["Fastball (2S) / Sinker"]["Chase%"] = {"min": 43, "mid": 22.5, "max": 8}
stat_ranges["Fastball (2S) / Sinker"]["Zone%-Chase%"] = {"min": 22, "mid": 42.8, "max": 66}
stat_ranges["Fastball (2S) / Sinker"]["InZoneSLG"] = {"min": .100, "mid": .517, "max": .850}
stat_ranges["Fastball (2S) / Sinker"]["ChaseSLG"] = {"min": .100, "mid": .312, "max": .800}

# Cutter
stat_ranges["Cutter"]["Z-Contact%"] = {"min": 65, "mid": 82.3, "max": 98}
stat_ranges["Cutter"]["O-Contact%"] = {"min": 25, "mid": 53, "max": 95}
stat_ranges["Cutter"]["Contact%"] = {"min": 55, "mid": 73, "max": 90}
stat_ranges["Cutter"]["InZoneSwing%"] = {"min": 46, "mid": 69.8, "max": 89}
stat_ranges["Cutter"]["Chase%"] = {"min": 43, "mid": 27.2, "max": 10.5}
stat_ranges["Cutter"]["Zone%-Chase%"] = {"min": 20.5, "mid": 42.6, "max": 61.5}
stat_ranges["Cutter"]["InZoneSLG"] = {"min": .100, "mid": .581, "max": .950}
stat_ranges["Cutter"]["ChaseSLG"] = {"min": .100, "mid": .229, "max": .667}

# Slider
stat_ranges["Slider"]["Z-Contact%"] = {"min": 67, "mid": 82.2, "max": 95}
stat_ranges["Slider"]["O-Contact%"] = {"min": 21, "mid": 47.8, "max": 75}
stat_ranges["Slider"]["Contact%"] = {"min": 51, "mid": 69, "max": 84}
stat_ranges["Slider"]["InZoneSwing%"] = {"min": 44, "mid": 61.7, "max": 78}
stat_ranges["Slider"]["Chase%"] = {"min": 39.8, "mid": 26.7, "max": 14.4}
stat_ranges["Slider"]["Zone%-Chase%"] = {"min": 16, "mid": 35.1, "max": 54}
stat_ranges["Slider"]["InZoneSLG"] = {"min": .133, "mid": .522, "max": .790}
stat_ranges["Slider"]["ChaseSLG"] = {"min": 0, "mid": .202, "max": .579}

# Soft (chg/splt)
stat_ranges["Soft (chg/splt)"]["Z-Contact%"] = {"min": 63, "mid": 78.3, "max": 93}
stat_ranges["Soft (chg/splt)"]["O-Contact%"] = {"min": 31, "mid": 55.2, "max": 81.8}
stat_ranges["Soft (chg/splt)"]["Contact%"] = {"min": 51, "mid": 68.8, "max": 86}
stat_ranges["Soft (chg/splt)"]["InZoneSwing%"] = {"min": 58, "mid": 73.5, "max": 87}
stat_ranges["Soft (chg/splt)"]["Chase%"] = {"min": 41, "mid": 29.6, "max": 16.4}
stat_ranges["Soft (chg/splt)"]["Zone%-Chase%"] = {"min": 19, "mid": 43.9, "max": 60}
stat_ranges["Soft (chg/splt)"]["InZoneSLG"] = {"min": .170, "mid": .573, "max": 1.000}
stat_ranges["Soft (chg/splt)"]["ChaseSLG"] = {"min": 0, "mid": .271, "max": .800}

# Breaking (cv/sld/sw)
stat_ranges["Breaking (cv/sld/sw)"]["Z-Contact%"] = {"min": 69, "mid": 82.5, "max": 94.9}
stat_ranges["Breaking (cv/sld/sw)"]["O-Contact%"] = {"min": 18, "mid": 48.4, "max": 72}
stat_ranges["Breaking (cv/sld/sw)"]["Contact%"] = {"min": 48, "mid": 69.3, "max": 84.5}
stat_ranges["Breaking (cv/sld/sw)"]["InZoneSwing%"] = {"min": 45, "mid": 59.5, "max": 79}
stat_ranges["Breaking (cv/sld/sw)"]["Chase%"] = {"min": 39, "mid": 25.7, "max": 15}
stat_ranges["Breaking (cv/sld/sw)"]["Zone%-Chase%"] = {"min": 17.5, "mid": 33.8, "max": 50}
stat_ranges["Breaking (cv/sld/sw)"]["InZoneSLG"] = {"min": .120, "mid": .506, "max": .820}
stat_ranges["Breaking (cv/sld/sw)"]["ChaseSLG"] = {"min": 0, "mid": .198, "max": .500}

# TOTAL row ranges (using overall league averages as a rough estimate)
total_ranges = {
    "Z-Contact%": {"min": 70, "mid": 83, "max": 95},
    "O-Contact%": {"min": 30, "mid": 48, "max": 70},
    "Contact%": {"min": 60, "mid": 71, "max": 85},
    "InZoneSwing%": {"min": 60, "mid": 72, "max": 85},
    "Chase%": {"min": 35, "mid": 28.5, "max": 20},
    "Zone%-Chase%": {"min": 30, "mid": 43.4, "max": 55},
    "InZoneSLG": {"min": 0.400, "mid": 0.600, "max": 0.800},
    "ChaseSLG": {"min": 0.200, "mid": 0.302, "max": 0.450}
}

# Header metric thresholds
header_ranges = {
    "ExitVel": {"min": 82.0, "mid": 86.8, "max": 96},
    "90thExitVel": {"min": 100.0, "mid": 102.5, "max": 105.0},
    "Air EV": {"min": 83, "mid": 89.5, "max": 99},
    "LaunchAng": {"min": 0.0, "mid": 10.3, "max": 22.0},
    "HHLaunchAng": {"min": 0.0, "mid": 12.8, "max": 22.0},
    "xSLG": {"min": 0.190, "mid": 0.388, "max": 1.000}
}


def get_color_for_value(value, stat_name, is_header=False, pitch_type=None, is_total=False):
    """Get background color for a value based on its performance range"""
    if pd.isna(value):
        return "#f0f0f0"

    if is_header:
        ranges = header_ranges[stat_name]
    elif is_total:
        ranges = total_ranges[stat_name]
    else:
        ranges = stat_ranges[pitch_type][stat_name]

    lo, mid, hi = ranges["min"], ranges["mid"], ranges["max"]

    # Special handling for Chase% (lower is better)
    if stat_name == "Chase%":
        frac = (value - lo) / (hi - lo) if hi != lo else 0.5
    else:
        # Clamp between 0 and 1
        if value >= hi:
            frac = 1.0
        elif value <= lo:
            frac = 0.0
        else:
            frac = (value - lo) / (hi - lo)

    return mcolors.to_hex(cmap_sum(frac))


def create_header_html(header_values):
    """Create HTML table for header metrics"""
    html = """
    <style>
    .header-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 8px;
        margin: 20px 0;
    }
    .header-cell {
        padding: 20px 15px;
        font-size: 18px;
        font-weight: bold;
        border: 2px solid #ddd;
        border-radius: 8px;
        text-align: center;
        min-width: 120px;
        height: 60px;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    .header-label {
        padding: 15px 10px;
        font-size: 16px;
        font-weight: bold;
        background-color: transparent;
        border: 2px solid #ddd;
        border-radius: 8px 8px 0 0;
        text-align: center;
        color: white;
    }
    </style>
    <table class="header-table">
        <tr>
    """

    for metric in metrics_list:
        html += f'<th class="header-label">{metric}</th>'
    html += '</tr><tr>'

    for metric in metrics_list:
        value = header_values[metric]
        bg_color = get_color_for_value(value, metric, is_header=True)

        if metric.endswith("SLG"):
            formatted_value = f"{value:.3f}" if not pd.isna(value) else "N/A"
        else:
            formatted_value = f"{value:.1f}" if not pd.isna(value) else "N/A"

        html += f'<td class="header-cell" style="background-color: {bg_color};">{formatted_value}</td>'

    html += '</tr></table>'
    return html


def create_contact_html(grp_data, total_row=None):
    """Create HTML table for contact metrics"""
    html = """
    <style>
    .contact-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 14px;
    }
    .contact-header {
        background-color: transparent;
        padding: 12px 8px;
        border: 1px solid #ddd;
        font-weight: bold;
        text-align: center;
        color: white;
    }
    .contact-cell {
        padding: 12px 8px;
        border: 1px solid #ddd;
        text-align: center;
        color: white;
        font-weight: 500;
        text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
        font-size: 20px;
    }
    .pitch-name {
        background-color: transparent;
        color: white;
        font-weight: bold;
        text-align: left;
        padding-left: 15px;
        font-size: 20px;
        padding: 12px 8px 12px 15px;
        border: 1px solid #ddd;
    }
    .total-row {
        border-top: 3px solid #ddd;
    }
    .total-name {
        background-color: transparent;
        color: white;
        font-weight: bold;
        text-align: left;
        padding-left: 15px;
        font-size: 20px;
        padding: 12px 8px 12px 15px;
        border: 1px solid #ddd;
        border-top: 3px solid #ddd;
    }
    </style>
    <table class="contact-table">
        <tr>
            <th class="contact-header">Pitch Type</th>
    """

    for col in contact_cols:
        html += f'<th class="contact-header">{col}</th>'
    html += '</tr>'

    # Add pitch type rows
    for pitch_type in pitch_order:
        if pitch_type in grp_data.index:
            html += f'<tr><td class="pitch-name">{pitch_type}</td>'

            for col in contact_cols:
                value = grp_data.loc[pitch_type, col]
                bg_color = get_color_for_value(value, col, is_header=False, pitch_type=pitch_type)

                if col.endswith("SLG"):
                    formatted_value = f"{value:.3f}" if not pd.isna(value) else "N/A"
                else:
                    formatted_value = f"{value:.1f}%" if not pd.isna(value) else "N/A"

                html += f'<td class="contact-cell" style="background-color: {bg_color};">{formatted_value}</td>'
            html += '</tr>'

    # Add TOTAL row if provided
    if total_row is not None:
        html += f'<tr class="total-row"><td class="total-name">TOTAL</td>'
        
        for col in contact_cols:
            value = total_row[col]
            bg_color = get_color_for_value(value, col, is_total=True)

            if col.endswith("SLG"):
                formatted_value = f"{value:.3f}" if not pd.isna(value) else "N/A"
            else:
                formatted_value = f"{value:.1f}%" if not pd.isna(value) else "N/A"

            html += f'<td class="contact-cell" style="background-color: {bg_color};">{formatted_value}</td>'
        html += '</tr>'

    html += '</table>'
    return html


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

    # build header_values Series from TOTAL row
    header_values = pd.Series({
        "ExitVel": total["ExitVel"],
        "90thExitVel": total["90thExitVel"],
        "Air EV": total["Air EV"],
        "LaunchAng": total["LaunchAng"],
        "HHLaunchAng": total["HHLaunchAng"],
        "xSLG": total["xSLG"]
    }).apply(pd.to_numeric, errors="coerce")

    # Process TOTAL row for contact metrics
    total_contact = pd.Series({col: total[col] for col in contact_cols})
    # Convert percentage strings to numeric values
    for col in contact_cols:
        if isinstance(total_contact[col], str) and total_contact[col].endswith('%'):
            total_contact[col] = float(total_contact[col].rstrip('%'))
        else:
            total_contact[col] = pd.to_numeric(total_contact[col], errors='coerce')

    df = df[df["SplitBy"] != "TOTAL"].copy()
    df = df[df[pitch_col].isin(pitch_order)]
    df[["P"] + metrics_list] = df[["P"] + metrics_list].apply(pd.to_numeric, errors="coerce")
    df[contact_cols] = df[contact_cols].apply(lambda c: pd.to_numeric(c.astype(str).str.rstrip("%"), errors="coerce"))

    # Layout with headshot and header metrics
    left, right = st.columns([1, 5])

    with left:
        if headshot_url and headshot_url.strip():
            try:
                st.image(headshot_url, use_column_width=True)  # Changed from use_container_width
            except Exception as e:
                st.error(f"Unable to load headshot image: {e}")
        else:
            st.write("_No headshot URL provided_")

    with right:
        # Create and display header metrics using HTML
        header_html = create_header_html(header_values)
        st.markdown(header_html, unsafe_allow_html=True)

    st.markdown("---")

    # Process contact data
    agg = {"P": "sum", **{c: "mean" for c in contact_cols}}
    grp = df.groupby(pitch_col).agg(agg).reindex(pitch_order)
    grp["P%"] = (grp["P"] / grp["P"].sum() * 100).round(1)

    # Create and display contact metrics using HTML with TOTAL row
    contact_html = create_contact_html(grp, total_contact)
    st.markdown(contact_html, unsafe_allow_html=True)

else:
    st.info("Upload a CSV and enter a headshot URL to see the dashboard.")

# --- Footer ---
st.markdown(
    """
    <div style='text-align: center; margin-top: 20px; font-size: 14px; color: grey;'>
        Data: TruMedia
    </div>
    """,
    unsafe_allow_html=True
)
