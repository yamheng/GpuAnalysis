# for data clean
import streamlit as st
import pandas as pd

def show(df):
    st.markdown("## :material/data_info_alert: Data Engineering Info")
    st.markdown("To ensure high-quality analysis, we performed rigorous cleaning on the raw dataset, handling inconsistent units (MB/GB), date formats, and dirty strings.")
    
    st.markdown("### 1. Handling Missing Data (The 'Unknown' Problem)")
    st.markdown("The first few rows (1986 era) contain many 'unknown' values. Our cleaning logic correctly converts them to `NaN` (None) to prevent errors.")

    # Read the original data for comparison (try to read from the data folder or root directory)
    try:
        df_raw = pd.read_csv('data/gpu_1986-2026.csv')
    except FileNotFoundError:
        try:
            df_raw = pd.read_csv('gpu_1986-2026.csv')
        except:
            st.error("Raw CSV file not found for comparison.")
            return

    # Show the first 5 lines (to verify if the cleaning logic works)
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Raw Data (Head): Note the 'unknown' strings")
        st.dataframe(df_raw.head(5)[['Graphics Processor__Transistors', 'Board Design__TDP']])
    with col2:
        st.caption("Cleaned Data (Head): Successfully converted to None")
        st.dataframe(df[['Transistors_Million', 'TDP_Watts']].head(5))

    st.markdown("---")
    st.markdown("### 2. Verifying Modern Data (It Works!)")
    
    # Show 5 rows of data from 2023 onwards
    df_modern = df[df['Release_Year'] > 2023].head(5)
    # Corresponding original data index
    if not df_modern.empty:
        df_raw_modern = df_raw.iloc[df_modern.index]
        
        col3, col4 = st.columns(2)
        with col3:
            st.caption("Raw Data (Modern Era): Strings with units")
            st.dataframe(df_raw_modern[['Graphics Processor__Transistors', 'Board Design__TDP']])
        with col4:
            st.caption("Cleaned Data (Modern Era): Pure Numbers")
            st.dataframe(df_modern[['Transistors_Million', 'TDP_Watts']])
    
    st.markdown("---")
    
    with st.expander("Domain Knowledge: Why is data missing?", expanded=False, icon=":material/help:"):
        st.markdown("""
        **1. The Concept of TDP:** In the 80s/90s, cards consumed negligible power (< 5 Watts), so TDP wasn't a tracked metric until the GeForce 256 (1999).
        
        **2. Transistor Counts:** Early manufacturers focused on features (Color Support) rather than silicon complexity. It became a marketing metric only later.
        
        **Strategy:** We treat 'unknown' as `NaN` rather than `0` to avoid skewing averages.
        """)