import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

with st.sidebar:
    #st.image("data/image_abstract.png")
    st.title("A Renal Cell Carcinoma Biomarker Study Web App :hospital:")
    choice = st.radio("Navigation", ["Introduction", "App"])
    st.info("App by [Olatomiwa Bifarin](https://www.linkedin.com/in/obifarin/)")
    # Add patient ID search input
    patient_search = st.text_input("Search for Patient ID")

if choice == 'Introduction':
    st.subheader("Machine Learning-Enabled Renal Cell Carcinoma Status Prediction Using Urine-Based Metabolomics")
    
    st.info("""This is an interactive portal accompanying the paper on kidney cancer biomarker discovery,
    navigate to the App section for details.
    """)

    st.write("Click here to read the [paper](https://pubs.acs.org/doi/10.1021/acs.jproteome.1c00213)")
    with st.expander("Read full paper abstract"):
        st.write("Renal cell carcinoma (RCC) is diagnosed through expensive cross-sectional imaging, frequently followed by renal mass biopsy, which is not only invasive but also prone to sampling errors. Hence, there is a critical need for a noninvasive diagnostic assay. RCC exhibits altered cellular metabolism combined with the close proximity of the tumor(s) to the urine in the kidney, suggesting that urine metabolomic profiling is an excellent choice for assay development. Here, we acquired liquid chromatography–mass spectrometry (LC–MS) and nuclear magnetic resonance (NMR) data followed by the use of machine learning (ML) to discover candidate metabolomic panels for RCC. The study cohort consisted of 105 RCC patients and 179 controls separated into two subcohorts: the model cohort and the test cohort. Univariate, wrapper, and embedded methods were used to select discriminatory features using the model cohort. Three ML techniques, each with different induction biases, were used for training and hyperparameter tuning. Assessment of RCC status prediction was evaluated using the test cohort with the selected biomarkers and the optimally tuned ML algorithms. A seven-metabolite panel predicted RCC in the test cohort with 88% accuracy, 94% sensitivity, 85% specificity, and 0.98 AUC. Metabolomics Workbench Study IDs are ST001705 and ST001706.")
    
    
    
    st.image("data/image_abstract.png")

if choice == "App":
    st.subheader("""This graph shows the seven biomarkers discovered in our published work with selected metadata.""")
    with st.expander("How to use"):
        st.write("""On your sidebar, type the Patient ID you are searching for, use the dropdown to select relevant RCC meta-data of your interest and the urine biomarkers. 
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
        RCCdf_filtered = RCCdf[RCCdf["Patient ID"].astype(str).str.strip().str.lower() == patient_search.lower()]
        RCCdf_unselected = RCCdf[RCCdf["Patient ID"].astype(str).str.strip().str.lower() != patient_search.lower()]
    else:
        RCCdf_filtered = pd.DataFrame(columns=RCCdf.columns)  # Empty if no search
        RCCdf_unselected = RCCdf  # All data if no search

    # Create a Plotly Graph Object Figure
    fig = go.Figure()

    # Function to generate hover text
    def generate_hover_text(df, marker):
        return df.apply(lambda row: f"ID: {row['Patient ID']}<br>{marker}: {row[marker]}", axis=1)

    # Add unselected (greyed out) data points
    for cat in RCCdf_unselected[selected_metadata].unique():
        category_df = RCCdf_unselected[RCCdf_unselected[selected_metadata] == cat]
        hover_text = generate_hover_text(category_df, selected_marker)
        fig.add_trace(go.Violin(x=category_df[selected_metadata],
                                y=category_df[selected_marker],
                                name=cat,
                                box_visible=True,
                                meanline_visible=True,
                                opacity=0.6,  # Greyed out
                                points='all',
                                hoverinfo='text',
                                text=hover_text,
                                showlegend=False))

    # Add selected (highlighted) data points, if any
    if not RCCdf_filtered.empty:
        for cat in RCCdf_filtered[selected_metadata].unique():
            category_df = RCCdf_filtered[RCCdf_filtered[selected_metadata] == cat]
            hover_text = generate_hover_text(category_df, selected_marker)
            fig.add_trace(go.Violin(x=category_df[selected_metadata],
                                    y=category_df[selected_marker],
                                    name=cat,
                                    box_visible=True,
                                    meanline_visible=True,
                                    opacity=1,  # Highlight
                                    points='all',
                                    hoverinfo='text',
                                    text=hover_text,
                                    showlegend=False))

    # Update the layout if needed
    fig.update_layout(title_text=f"Distribution of {selected_marker} by {selected_metadata}",
                      violingap=0, violinmode='overlay')

    st.plotly_chart(fig)

