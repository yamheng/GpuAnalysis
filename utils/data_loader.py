import pandas as pd
import numpy as np
import re
import streamlit as st

@st.cache_data
def load_and_clean_data():
    # ... (此处请完整粘贴你 test.py 中原有的 load_and_clean_data 函数内容) ...
    # 确保读取路径改为 'data/gpu_1986-2026.csv' 或者处理好相对路径
    try:
        df = pd.read_csv('data/gpu_1986-2026.csv') 
    except FileNotFoundError:
        st.error("File 'gpu_1986-2026.csv' not found.")
        return pd.DataFrame()
        

    df_clean = df.copy()

    # --- Helper Regex Functions ---
    def parse_transistors(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        val_str = str(val).lower().replace(',', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'billion' in val_str: return num * 1000
        elif 'million' in val_str: return num
        return np.nan

    def parse_memory_size(val):
        if pd.isna(val) or str(val).lower() in ['unknown', 'system shared']: return np.nan
        val_str = str(val).lower().strip()
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'gb' in val_str: return num * 1024
        elif 'mb' in val_str: return num
        elif 'kb' in val_str: return num / 1024
        return num

    def parse_tdp(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        match = re.search(r"(\d+)", str(val))
        return float(match.group(1)) if match else np.nan

    def parse_process_size(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        match = re.search(r"(\d+)", str(val))
        return float(match.group(1)) if match else np.nan

    def parse_die_size(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        match = re.search(r"([\d\.]+)", str(val))
        return float(match.group(1)) if match else np.nan

    def parse_bandwidth(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        val_str = str(val).lower().replace(',', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'mb/s' in val_str: return num / 1024
        return num 

    # --- NEW FUNCTION FOR FP32 ---
    def parse_gflops(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        val_str = str(val).lower().replace(',', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        
        if 'tflops' in val_str:
            return num * 1000
        return num

    def parse_date(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return pd.NaT
        val_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(val))
        try:
            return pd.to_datetime(val_clean)
        except:
            return pd.NaT

    # --- Apply Cleaning ---
    df_clean['Transistors_Million'] = df_clean['Graphics Processor__Transistors'].apply(parse_transistors)
    df_clean['Memory_MB'] = df_clean['Memory__Memory Size'].apply(parse_memory_size)
    df_clean['TDP_Watts'] = df_clean['Board Design__TDP'].apply(parse_tdp)
    df_clean['Process_Size_nm'] = df_clean['Graphics Processor__Process Size'].apply(parse_process_size)
    df_clean['Die_Size_mm2'] = df_clean['Graphics Processor__Die Size'].apply(parse_die_size)
    df_clean['Bandwidth_GBs'] = df_clean['Memory__Bandwidth'].apply(parse_bandwidth)
    df_clean['Release_Date'] = df_clean['Graphics Card__Release Date'].apply(parse_date)
    df_clean['Release_Year'] = df_clean['Release_Date'].dt.year
    
    df_clean['Transistor_Density'] = df_clean['Transistors_Million'] / df_clean['Die_Size_mm2']

    # --- FIX HERE ---
    df_clean['FP32_GFLOPS'] = df_clean['Theoretical Performance__FP32 (float)'].apply(parse_gflops)
    
    df_clean['Perf_Per_Watt'] = df_clean['FP32_GFLOPS'] / df_clean['TDP_Watts']
    
    return df_clean