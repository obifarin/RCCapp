import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

with st.sidebar: 
    #st.image("data/image_abstract.png")
    st.title("A Renal Cell Carcinoma Biomarker Study Web App :hospital:")
    choice = st.radio("Navigation", ["Introduction", "App"])
    st.info("App by Olatomiwa Bifarin, Ph.D. :male-scientist:")
    
if choice ==  'Introduction': 
    st.subheader("Machine Learning-Enabled Renal Cell Carcinoma Status Prediction Using Urine-Based Metabolomics")
    
    st.info("""This is an interactive portal accompanying the paper on kidney cancer biomarker discovery,
    navigate to the App section for details.
    """)

    st.write("Click here to read the [paper](https://pubs.acs.org/doi/10.1021/acs.jproteome.1c00213)")
    with st.expander("Read full paper abstract"):
        st.write("Renal cell carcinoma (RCC) is diagnosed through expensive cross-sectional imaging, frequently followed by renal mass biopsy, which is not only invasive but also prone to sampling errors. Hence, there is a critical need for a noninvasive diagnostic assay. RCC exhibits altered cellular metabolism combined with the close proximity of the tumor(s) to the urine in the kidney, suggesting that urine metabolomic profiling is an excellent choice for assay development. Here, we acquired liquid chromatography–mass spectrometry (LC–MS) and nuclear magnetic resonance (NMR) data followed by the use of machine learning (ML) to discover candidate metabolomic panels for RCC. The study cohort consisted of 105 RCC patients and 179 controls separated into two subcohorts: the model cohort and the test cohort. Univariate, wrapper, and embedded methods were used to select discriminatory features using the model cohort. Three ML techniques, each with different induction biases, were used for training and hyperparameter tuning. Assessment of RCC status prediction was evaluated using the test cohort with the selected biomarkers and the optimally tuned ML algorithms. A seven-metabolite panel predicted RCC in the test cohort with 88% accuracy, 94% sensitivity, 85% specificity, and 0.98 AUC. Metabolomics Workbench Study IDs are ST001705 and ST001706.")
    
    
    
    st.image("data/image_abstract.png")

    
if choice == "App":
    st.subheader("""This graph show the seven biomarker discovered in our published work with selected metadata.""")
    with st.expander("How to use"):
        st.write(" On your sidebar , use the dropdown to select relevant RCC meta-data of your interest and the urine biomarkers. The Graph is interactive, hover your mouse on data points to see Patient ID. Metabolites abundances were log-transformed.")

    #Import cleaned up logtransformed data, see the script for pre-processing
    RCCdf = pd.read_excel('data/RCCdataframe_clean.xlsx')

    #Disease metadata
    rcc_metadata = ['Metastatic', 'SubTypes', 'Stage']

    #Metabolic biomarker
    marker_data = ["N-acetyl-glucosaminic acid", "2-mercaptobenzothiazole", "hippurate-mannitol derivative",
                    "hippuric acid", "dibutylamine", "Lys-Ile", "2-phenylacetamide"]


    #Selected metadata
    selected_metadata = st.sidebar.selectbox("Select an RCC metadata", rcc_metadata)

    #Selected marker
    selected_marker = st.sidebar.selectbox("Select a metabolite", marker_data)

    #Plot graph
    fig = px.violin(RCCdf, x=selected_metadata,
    y=selected_marker,
    box=True,
    points='all',
    hover_data=["Patient ID"]
    # animation_frame="Metastatic"
    )
    st.plotly_chart(fig)
    