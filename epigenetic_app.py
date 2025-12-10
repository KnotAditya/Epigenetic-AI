import streamlit as st
import os
from PIL import Image
import importlib
import numpy as np
import plotly.graph_objs as go

# Set page configuration FIRST
st.set_page_config(page_title="Epigenetic Cancer Detection AI", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #0e0f11;
        color: #f5f5f5;
    }
    section[data-testid="stSidebar"] {
        width: 40% !important;
        min-width: 380px;
        background-color: #1e1f25;
    }
    .title-header {
        font-size: 3em;
        font-weight: bold;
        color: #00d4ff;
        margin-bottom: 20px;
        text-align: center;
    }
    .css-1aumxhk {
        background-color: #1e1f25;
    }
    button[kind="primary"] {
        background-color: #00c9ff !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# DNA animation
def generate_professional_dna_helix():
    z = np.linspace(-6, 6, 300)
    x1 = np.cos(z)
    y1 = np.sin(z)
    x2 = -np.cos(z)
    y2 = -np.sin(z)

    # Base-pair connectors
    connectors = []
    for i in range(0, len(z), 15):
        connectors.append(go.Scatter3d(
            x=[x1[i], x2[i]],
            y=[y1[i], y2[i]],
            z=[z[i], z[i]],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.5)', width=2),
            showlegend=False
        ))

    # Animation frames
    frames = []
    for phase in np.linspace(0, 2 * np.pi, 60):
        x1_phase = np.cos(z + phase)
        y1_phase = np.sin(z + phase)
        x2_phase = -np.cos(z + phase)
        y2_phase = -np.sin(z + phase)
        connector_frame = [
            go.Scatter3d(
                x=[x1_phase[i], x2_phase[i]],
                y=[y1_phase[i], y2_phase[i]],
                z=[z[i], z[i]],
                mode='lines',
                line=dict(color='rgba(255,255,255,0.5)', width=2),
                showlegend=False
            ) for i in range(0, len(z), 15)
        ]
        frames.append(go.Frame(
            data=[
                go.Scatter3d(x=x1_phase, y=y1_phase, z=z, mode='lines', line=dict(color='cyan', width=5)),
                go.Scatter3d(x=x2_phase, y=y2_phase, z=z, mode='lines', line=dict(color='magenta', width=5))
            ] + connector_frame
        ))

    layout = go.Layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgb(10,10,20)'
        ),
        paper_bgcolor='rgb(10,10,20)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {
                    'frame': {'duration': 60, 'redraw': True},
                    'fromcurrent': True,
                    'transition': {'duration': 0}
                }]
            }]
        }]
    )

    return go.Figure(
        data=[
            go.Scatter3d(x=x1, y=y1, z=z, mode='lines', line=dict(color='cyan', width=5)),
            go.Scatter3d(x=x2, y=y2, z=z, mode='lines', line=dict(color='magenta', width=5))
        ] + connectors,
        layout=layout,
        frames=frames
    )
# Main title
st.markdown('<div class="title-header">🧬 Epigenetic Cancer Detection AI</div>', unsafe_allow_html=True)

# Layout columns
col1, col2 = st.columns([3, 4])
fig = generate_professional_dna_helix()

with col2:
    fig = generate_professional_dna_helix()
    st.plotly_chart(fig, use_container_width=True)


# Sidebar content
st.sidebar.title("Upload & Select")

def get_cancer_types():
    try:
        folder = os.path.join(os.path.dirname(__file__), "Types_Experiment")
        return sorted([f[:-3] for f in os.listdir(folder) if f.endswith(".py") and not f.startswith("__")])
    except Exception:
        st.sidebar.warning("Could not load cancer types.")
        return []

uploaded_file = st.sidebar.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
cancer_types = get_cancer_types()
selected_cancer = st.sidebar.selectbox("Cancer Type", cancer_types)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Preview", use_column_width=True)

if st.sidebar.button("Run Detection"):
    if not uploaded_file:
        st.error("Please upload an image.")
    elif not selected_cancer:
        st.error("Please select a cancer type.")
    else:
        try:
            module = importlib.import_module(f"Types_Experiment.{selected_cancer}")
            if hasattr(module, 'predict'):
                with st.spinner("Detecting..."):
                    result = module.predict(uploaded_file)
                st.success(f"Prediction: {result}")
            else:
                st.error(f"The module '{selected_cancer}' lacks a 'predict' function.")
        except Exception as e:
            st.error(f"Error: {e}")
