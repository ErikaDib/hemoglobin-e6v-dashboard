import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import py3Dmol
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Hemoglobin E6V Dashboard",
    layout="wide"
)

# -----------------------------
# Fixed project data
# -----------------------------
PROTEIN_NAME = "Hemoglobin subunit beta"
GENE = "HBB"
UNIPROT_ID = "P68871"
ORGANISM = "Homo sapiens"
MUTATION = "E6V"
MUTATION_POSITION = 6
WILD_TYPE = "Glutamate (E)"
MUTANT = "Valine (V)"
SEQUENCE_LENGTH = 147
DISEASE = "Sickle cell disease"

SUMMARY_TEXT = """
The E6V mutation replaces glutamate with valine at position 6 of the hemoglobin beta chain.
Glutamate is negatively charged and hydrophilic, while valine is more hydrophobic. This substitution
changes the surface chemistry of hemoglobin and helps explain the abnormal intermolecular interactions
associated with sickle cell disease.
"""

PDB_PATH = Path("data/AF-P68871-F1-model_v6.pdb")
RBC_IMAGE_PATH = Path("red-blood-cell.jpg") 

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0,255,255,0.10), transparent 18%),
        radial-gradient(circle at 88% 12%, rgba(255,0,220,0.08), transparent 18%),
        radial-gradient(circle at 50% 90%, rgba(0,120,255,0.08), transparent 24%),
        linear-gradient(135deg, #07111d 0%, #081728 45%, #040913 100%);
    color: #ecfbff;
}

.block-container {
    max-width: 1480px;
    padding-top: 3rem;
    padding-bottom: 2rem;
}

.hero {
    border-radius: 24px;
    padding: 1.25rem 1.5rem 1.15rem 1.5rem;
    margin-bottom: 1.1rem;
    background: linear-gradient(135deg, rgba(9,24,43,0.96), rgba(7,15,29,0.97));
    border: 1px solid rgba(110,230,255,0.20);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 0 20px rgba(0,255,255,0.06),
        0 0 38px rgba(0,120,255,0.05);
}

.hero-title {
    text-align: center;
    font-size: 2.25rem;
    font-weight: 800;
    color: #f7fdff;
    margin-bottom: 0.2rem;
    line-height: 1.08;
}

.hero-subtitle {
    text-align: center;
    color: #8de7ff;
    font-size: 1rem;
    letter-spacing: 0.05em;
    margin-bottom: 0.7rem;
}

.hero-desc {
    text-align: center;
    color: #d9f6ff;
    line-height: 1.65;
    max-width: 980px;
    margin: 0 auto;
}

.side-panel {
    border-radius: 22px;
    padding: 1rem;
    min-height: 760px;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 0 18px rgba(0,255,255,0.04);
}

.left-panel {
    background: linear-gradient(180deg, rgba(224,246,255,0.10), rgba(182,229,255,0.07));
    border: 1px solid rgba(125,230,255,0.28);
}

.right-panel {
    background: linear-gradient(180deg, rgba(255,220,252,0.09), rgba(245,184,255,0.06));
    border: 1px solid rgba(255,138,240,0.24);
}

.main-panel {
    border-radius: 22px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    background: linear-gradient(180deg, rgba(11,21,37,0.96), rgba(7,14,25,0.97));
    border: 1px solid rgba(116,233,255,0.20);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03) inset,
        0 0 24px rgba(0,255,255,0.05),
        0 0 36px rgba(0,90,255,0.04);
}

.bottom-panel-left {
    border-radius: 22px;
    padding: 1rem;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    background: linear-gradient(180deg, rgba(202,255,247,0.08), rgba(132,255,235,0.05));
    border: 1px solid rgba(124,255,222,0.22);
    box-shadow: 0 0 18px rgba(0,255,255,0.04);
}

.bottom-panel-right {
    border-radius: 22px;
    padding: 1rem;
    margin-top: 1.5rem;
    background: linear-gradient(180deg, rgba(245,226,255,0.09), rgba(214,174,255,0.06));
    border: 1px solid rgba(212,160,255,0.22);
    box-shadow: 0 0 18px rgba(0,255,255,0.04);
}

.panel-title {
    font-size: 1.02rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.85rem;
}

.left-title { color: #8ff7ff; }
.right-title { color: #ffa3f5; }
.center-title { color: #8ff7ff; text-align: center; }
.bottom-left-title { color: #8cffde; }
.bottom-right-title { color: #ddb4ff; }

.info-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.75rem;
}

.info-card {
    border-radius: 16px;
    padding: 0.8rem 0.9rem;
    min-height: 86px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
}

.left-panel .info-card {
    background: rgba(185,236,255,0.08);
    border: 1px solid rgba(125,230,255,0.16);
}

.right-panel .info-card {
    background: rgba(255,194,249,0.07);
    border: 1px solid rgba(255,138,240,0.15);
}

.label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.22rem;
}

.left-panel .label { color: #90efff; }
.right-panel .label { color: #ffadf5; }

.value {
    font-size: 1rem;
    font-weight: 600;
    color: #f2fcff;
    line-height: 1.45;
}

.metric-pill {
    display: inline-block;
    margin: 0.18rem 0.35rem 0.38rem 0;
    padding: 0.44rem 0.8rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 600;
}

.metric-cyan {
    background: rgba(125,230,255,0.10);
    border: 1px solid rgba(125,230,255,0.22);
    color: #e9fcff;
}

.metric-pink {
    background: rgba(255,138,240,0.09);
    border: 1px solid rgba(255,138,240,0.18);
    color: #ffeafc;
}

.metric-green {
    background: rgba(124,255,222,0.09);
    border: 1px solid rgba(124,255,222,0.18);
    color: #eafff9;
}

.center-caption {
    text-align: center;
    color: #a7d3e3;
    font-size: 0.92rem;
    margin-top: 0.7rem;
}

.note-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1rem;
    color: #eefbff;
    line-height: 1.75;
    font-size: 1rem;
}

.small-muted {
    color: #a7cbd8;
    font-size: 0.92rem;
    line-height: 1.55;
    margin-top: 0.6rem;
}

.rbc-image-wrap {
    margin-bottom: 0.9rem;
}

.rbc-image-wrap img {
    border-radius: 20px;
    border: 1px solid rgba(126,249,255,0.18);
    box-shadow:
        inset 0 0 0 1px rgba(255,255,255,0.03),
        0 0 22px rgba(0,255,255,0.06);
}

/* Frame the 3D iframe itself instead of wrapping it with extra HTML */
div[data-testid="stIFrame"] iframe {
    border-radius: 20px !important;
    border: 1px solid rgba(126,249,255,0.18) !important;
    background: #030712 !important;
    box-shadow:
        inset 0 0 0 1px rgba(255,255,255,0.03),
        0 0 22px rgba(0,255,255,0.06) !important;
}

/* Plotly section stays clean */
div[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def load_pdb_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text()

def extract_plddt_from_pdb(pdb_text: str) -> pd.DataFrame:
    rows = []
    seen = set()

    for line in pdb_text.splitlines():
        if not line.startswith("ATOM"):
            continue

        chain_id = line[21].strip()
        resi = line[22:26].strip()
        atom_name = line[12:16].strip()

        key = (chain_id, resi)
        if atom_name == "CA" and key not in seen:
            try:
                bfactor = float(line[60:66].strip())
            except ValueError:
                continue

            rows.append({
                "chain": chain_id if chain_id else "A",
                "resi": int(resi),
                "plddt": bfactor
            })
            seen.add(key)

    return pd.DataFrame(rows)

def make_confidence_plot(df: pd.DataFrame, mutation_pos: int) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["resi"],
        y=df["plddt"],
        mode="lines+markers",
        name="pLDDT",
        line=dict(color="#72f6ff", width=3),
        marker=dict(size=4, color="#72f6ff")
    ))

    mutation_row = df[df["resi"] == mutation_pos]
    if not mutation_row.empty:
        fig.add_trace(go.Scatter(
            x=mutation_row["resi"],
            y=mutation_row["plddt"],
            mode="markers+text",
            text=["E6V"],
            textposition="top center",
            marker=dict(size=14, color="#ff71f4", line=dict(color="#ffffff", width=1)),
            name="Mutation site"
        ))

    fig.update_layout(
        title="AlphaFold Confidence by Residue",
        title_font=dict(color="#ecfbff", size=19),
        xaxis_title="Residue position",
        yaxis_title="pLDDT",
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,12,22,0.86)",
        font=dict(color="#e3fbff"),
        xaxis=dict(gridcolor="rgba(126,249,255,0.08)", zeroline=False),
        yaxis=dict(gridcolor="rgba(126,249,255,0.08)", zeroline=False, range=[0, 100]),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e3fbff")),
        margin=dict(l=40, r=20, t=60, b=40)
    )
    return fig

def render_structure(pdb_text: str, mutation_pos: int, width: int = 500, height: int = 340) -> str:
    viewer = py3Dmol.view(width=width, height=height)
    viewer.addModel(pdb_text, "pdb")
    viewer.setStyle({"cartoon": {"colorscheme": "spectrum", "opacity": 0.96}})
    viewer.addStyle(
        {"resi": mutation_pos},
        {"stick": {"colorscheme": "magentaCarbon", "radius": 0.30}}
    )
    viewer.addStyle(
        {"resi": mutation_pos},
        {"sphere": {"color": "#ff4df0", "radius": 0.88}}
    )
    viewer.zoomTo()
    viewer.setBackgroundColor("#030712")

    inner = viewer._make_html()

    return f"""
    <html>
    <head>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background: #030712;
            }}
            body {{
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            #viewer-shell {{
                width: {width}px;
                height: {height}px;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                background: #030712;
            }}
        </style>
    </head>
    <body>
        <div id="viewer-shell">
            {inner}
        </div>
    </body>
    </html>
    """

# -----------------------------
# Load data
# -----------------------------
pdb_text = load_pdb_text(PDB_PATH)

if not pdb_text:
    st.error("PDB file not found. Put the file here: data/AF-P68871-F1-model_v6.pdb")
    st.stop()

# -----------------------------
# Header
# -----------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-title">AI Based Structural Analysis of the Hemoglobin E6V Mutation</div>
    <div class="hero-subtitle">Sickle Cell Disease • AlphaFold Structure</div>
    <div class="hero-desc">
        This dashboard explores the hemoglobin beta chain
        mutation E6V responsible for sickle cell disease. It contains protein visualization,
        mutation analysis, and the AlphaFold confidence data in one dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Top row
# -----------------------------
left_col, center_col, right_col = st.columns([1.05, 2.1, 1.05], gap="medium")

with left_col:
    st.markdown("""
    <div class="side-panel left-panel">
        <div class="panel-title left-title">Protein Information</div>
        <div class="info-grid">
            <div class="info-card"><div class="label">Protein</div><div class="value">Hemoglobin subunit beta</div></div>
            <div class="info-card"><div class="label">Gene</div><div class="value">HBB</div></div>
            <div class="info-card"><div class="label">UniProt ID</div><div class="value">P68871</div></div>
            <div class="info-card"><div class="label">Organism</div><div class="value">Homo sapiens</div></div>
            <div class="info-card"><div class="label">Sequence length</div><div class="value">147 amino acids</div></div>
            <div class="info-card"><div class="label">Biological role</div><div class="value">Beta chain of hemoglobin involved in oxygen transport</div></div>
        </div>
        <div style="margin-top:0.9rem;">
            <span class="metric-pill metric-cyan">Normal Levels:</span>
            <span class="metric-pill metric-green">Adult Males: 13.5–18 g/dL</span>
            <span class="metric-pill metric-cyan">Adult Females: 12–15 g/dL</span>
            <span class="metric-pill metric-cyan">Children: 11–16 g/dL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with center_col:

    if RBC_IMAGE_PATH.exists():
        st.markdown('<div class="rbc-image-wrap">', unsafe_allow_html=True)
        st.image(str(RBC_IMAGE_PATH), width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="main-panel">
        <div class="panel-title center-title">Predicted Hemoglobin Structure</div>
    </div>
    """, unsafe_allow_html=True)



    st.components.v1.html(
        render_structure(pdb_text, MUTATION_POSITION, width=500, height=340),
        height=360,
        scrolling=False
    )

    st.markdown("""
    <div class="center-caption">
        The mutation site at residue 6 is highlighted in magenta on the AlphaFold predicted structure.
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown(f"""
    <div class="side-panel right-panel">
        <div class="panel-title right-title">Mutation Analysis</div>
        <div class="info-grid">
            <div class="info-card"><div class="label">Disease</div><div class="value">{DISEASE}</div></div>
            <div class="info-card"><div class="label">Mutation</div><div class="value">{MUTATION}</div></div>
            <div class="info-card"><div class="label">Position</div><div class="value">{MUTATION_POSITION}</div></div>
            <div class="info-card"><div class="label">Wild type residue</div><div class="value">{WILD_TYPE}</div></div>
            <div class="info-card"><div class="label">Mutant residue</div><div class="value">{MUTANT}</div></div>
            <div class="info-card"><div class="label">Biochemical impact</div><div class="value">Loss of negative charge and increased hydrophobicity</div></div>
        </div>
        <div style="margin-top:0.9rem;">
            <span class="metric-pill metric-pink">Hydrophobic Patch Creation</span>
            <span class="metric-pill metric-pink">Abnormal Polymerization</span>
            <span class="metric-pill metric-pink">Formation of Rigid Fibers</span>
            <span class="metric-pill metric-pink">Reduced Solubility</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Bottom row (graph + interpretation side by side)
# -----------------------------
bottom_left, bottom_right = st.columns([2.0, 1.0], gap="medium")

with bottom_left:
    st.markdown("""
    <div class="bottom-panel-left">
        <div class="panel-title bottom-left-title">Confidence Score Plot</div>
    </div>
    """, unsafe_allow_html=True)

    confidence_df = extract_plddt_from_pdb(pdb_text)

    if not confidence_df.empty:
        fig = make_confidence_plot(confidence_df, MUTATION_POSITION)

        config = {
            "displayModeBar": False,
            "scrollZoom": False
        }

        st.plotly_chart(
            fig,
            width="stretch",
            config=config
        )
    else:
        st.warning("Could not extract pLDDT values from the PDB file.")

with bottom_right:
    st.markdown(f"""
    <div class="bottom-panel-right">
        <div class="panel-title bottom-right-title">Interpretation</div>
        <div class="note-box">
            {SUMMARY_TEXT}
    """, unsafe_allow_html=True)
