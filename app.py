import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

with st.sidebar:
    #st.image("data/image_abstract.png")
    st.title("A Renal Cell Carcinoma Biomarker Study Web App :hospital:")
    choice = st.radio("Navigation", ["Introduction", "App"])
    st.info("App by Olatomiwa Bifarin, Ph.D. :male-scientist:")
    # Add patient ID search input
    patient_search = st.text_input("Search for Patient ID")

if choice == 'Introduction':
    st.subheader("Machine Learning-Enabled Renal Cell Carcinoma Status Prediction Using Urine-Based Metabolomics")
    ...
    # Introduction content remains the same
    ...

if choice == "App":
    st.subheader("""This graph shows the seven biomarkers discovered in our published work with selected metadata.""")
    with st.expander("How to use"):
        st.write("""On your sidebar, use the dropdown to select relevant RCC meta-data of your interest and the urine biomarkers. 
                 The Graph is interactive, hover your mouse on data points to see Patient ID. Metabolites abundances were log-transformed.""")

    # Import cleaned up logtransformed data
    RCCdf = pd.read_excel('data/RCCdataframe_clean.xlsx')

    # Metadata and biomarker selections
    rcc_metadata = ['Metastatic', 'SubTypes', 'Stage']
    marker_data = ["N-acetyl-glucosaminic acid", "2-mercaptobenzothiazole", "hippurate-mannitol derivative",
                   "hippuric acid", "dibutylamine", "Lys-Ile", "2-phenylacetamide"]
    selected_metadata = st.sidebar.selectbox("Select an RCC metadata", rcc_metadata)
    selected_marker = st.sidebar.selectbox("Select a metabolite", marker_data)

    # Filter DataFrame based on patient ID search
    if patient_search:
        RCCdf_filtered = RCCdf[RCCdf["Patient ID"].astype(str) == patient_search]
        RCCdf_unselected = RCCdf[RCCdf["Patient ID"].astype(str) != patient_search]
    else:
        RCCdf_filtered = RCCdf
        RCCdf_unselected = pd.DataFrame(columns=RCCdf.columns)

    # Create a Plotly Graph Object Figure
    fig = go.Figure()

    # Add unselected (greyed out) data
    if not RCCdf_unselected.empty:
        for cat in RCCdf_unselected[selected_metadata].unique():
            fig.add_trace(go.Violin(x=RCCdf_unselected[RCCdf_unselected[selected_metadata] == cat][selected_metadata],
                                    y=RCCdf_unselected[RCCdf_unselected[selected_metadata] == cat][selected_marker],
                                    name=cat,
                                    box_visible=True,
                                    meanline_visible=True,
                                    opacity=0.3,  # Greyed out
                                    points='all',
                                    hoverinfo='skip',  # Optionally disable hover for unselected data
                                    showlegend=False))

    # Add selected data
    if not RCCdf_filtered.empty:
        for cat in RCCdf_filtered[selected_metadata].unique():
            fig.add_trace(go.Violin(x=RCCdf_filtered[RCCdf_filtered[selected_metadata] == cat][selected_metadata],
                                    y=RCCdf_filtered[RCCdf_filtered[selected_metadata] == cat][selected_marker],
                                    name=cat,
                                    box_visible=True,
                                    meanline_visible=True,
                                    opacity=1,  # Emphasize
                                    points='all',
                                    hoverinfo='all',
                                    showlegend=False))

    # Update the layout if needed
    fig.update_layout(title_text=f"Distribution of {selected_marker} by {selected_metadata}",
                      violingap=0, violinmode='overlay')

    st.plotly_chart(fig)
