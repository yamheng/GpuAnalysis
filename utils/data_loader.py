import pandas as pd
import numpy as np
import re
import streamlit as st
import os

@st.cache_data
def load_and_clean_data():
    # === 1. 读取原始数据 ===
    file_path = 'gpu_1986-2026.csv'
    if not os.path.exists(file_path):
        file_path = 'data/gpu_1986-2026.csv'
    
    try:
        df = pd.read_csv(file_path, dtype=str)
    except Exception as e:
        st.error(f"Critical Error: Could not read dataset. {e}")
        return pd.DataFrame()

    # === 2. “斩”：删除 CSV 中原有 5090 数据，防止干扰 ===
    df = df[~df['Name'].str.contains('GeForce RTX 5090', case=False, na=False)].copy()

    # ==========================================
    # 3. 清洗函数 (保持不变)
    # ==========================================
    def parse_transistors(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        val_str = str(val).lower().replace(',', '').replace('"', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'billion' in val_str: return num * 1000
        elif 'million' in val_str: return num
        return num

    def parse_die_size(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return np.nan
        match = re.search(r"([\d\.]+)", str(val))
        return float(match.group(1)) if match else np.nan

    def parse_price(val):
        if pd.isna(val): return np.nan
        val_str = str(val).replace(',', '').replace('$', '') 
        match = re.search(r"(\d+\.?\d*)", val_str)
        return float(match.group(1)) if match else np.nan
    
    def parse_date(val):
        if pd.isna(val) or str(val).lower() == 'unknown': return pd.NaT
        val_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(val))
        try:
            return pd.to_datetime(val_clean)
        except:
            return pd.NaT

    def parse_memory_size(val):
        if pd.isna(val): return np.nan
        val_str = str(val).lower()
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'gb' in val_str: return num * 1024
        elif 'mb' in val_str: return num
        return num

    def parse_tdp(val):
        if pd.isna(val): return np.nan
        match = re.search(r"(\d+)", str(val))
        return float(match.group(1)) if match else np.nan

    def parse_process_size(val):
        if pd.isna(val): return np.nan
        match = re.search(r"(\d+)", str(val))
        return float(match.group(1)) if match else np.nan

    def parse_bandwidth(val):
        if pd.isna(val): return np.nan
        val_str = str(val).lower().replace(',', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'mb/s' in val_str: return num / 1024
        return num 

    def parse_gflops(val):
        if pd.isna(val): return np.nan
        val_str = str(val).lower().replace(',', '')
        matches = re.findall(r"[\d\.]+", val_str)
        if not matches: return np.nan
        num = float(matches[0])
        if 'tflops' in val_str: return num * 1000
        return num

    def parse_clock(val):
        if pd.isna(val): return np.nan
        val_str = str(val).lower().replace(',', '')
        match = re.search(r"(\d+)", val_str)
        if not match: return np.nan
        num = float(match.group(1))
        if 'ghz' in val_str: return num * 1000 
        return num

    # ==========================================
    # 4. 应用清洗
    # ==========================================
    df_clean = df.copy()
    df_clean['Transistors_Million'] = df_clean['Graphics Processor__Transistors'].apply(parse_transistors)
    df_clean['Die_Size_mm2'] = df_clean['Graphics Processor__Die Size'].apply(parse_die_size)
    df_clean['Launch_Price'] = df_clean['Graphics Card__Launch Price'].apply(parse_price)
    df_clean['Release_Date'] = df_clean['Graphics Card__Release Date'].apply(parse_date)
    
    # 这里的 Year 默认为整数，后面我们会把它变成浮点数以支持微调
    df_clean['Release_Year'] = df_clean['Release_Date'].dt.year.astype(float)
    
    df_clean['Memory_MB'] = df_clean['Memory__Memory Size'].apply(parse_memory_size)
    df_clean['TDP_Watts'] = df_clean['Board Design__TDP'].apply(parse_tdp)
    df_clean['Process_Size_nm'] = df_clean['Graphics Processor__Process Size'].apply(parse_process_size)
    df_clean['Bandwidth_GBs'] = df_clean['Memory__Bandwidth'].apply(parse_bandwidth)
    df_clean['FP32_GFLOPS'] = df_clean['Theoretical Performance__FP32 (float)'].apply(parse_gflops)
    df_clean['GPU_Clock_MHz'] = df_clean['Clock Speeds__GPU Clock'].apply(parse_clock)

    # ==========================================
    # 5. “奏”：手动注入防重叠数据 (Jittered Data)
    # ==========================================
    # 关键修改：Release_Year 使用小数，让它们在图表X轴上错开！
    
    future_data = [
        {
            'Name': 'GeForce RTX 5090',
            'Brand': 'NVIDIA',
            'Graphics Processor__Architecture': 'Blackwell',
            'Graphics Processor__Foundry': 'TSMC',
            'Release_Year': 2025.05,         # ✅ 2025年初
            'Transistors_Million': 92200.0,
            'Die_Size_mm2': 750.0,
            'Process_Size_nm': 5.0,
            'TDP_Watts': 575.0,
            'FP32_GFLOPS': 104800.0,
            'Launch_Price': 1999.0,
            'Memory_MB': 32768.0,
            'Bandwidth_GBs': 1790.0,
            'GPU_Clock_MHz': 2017.0
        },
        {
            'Name': 'GeForce RTX 5090 D',
            'Brand': 'NVIDIA',
            'Graphics Processor__Architecture': 'Blackwell',
            'Graphics Processor__Foundry': 'TSMC',
            'Release_Year': 2025.20,         # ✅ 稍微往后一点，防止和标准版重叠
            'Transistors_Million': 92200.0,
            'Die_Size_mm2': 750.0,
            'Process_Size_nm': 5.0,
            'TDP_Watts': 575.0,
            'FP32_GFLOPS': 104800.0,
            'Launch_Price': 2299.0,          # 价格不同
            'Memory_MB': 32768.0,
            'Bandwidth_GBs': 1790.0,
            'GPU_Clock_MHz': 2017.0
        },
        {
            'Name': 'GeForce RTX 5090 D V2',
            'Brand': 'NVIDIA',
            'Graphics Processor__Architecture': 'Blackwell',
            'Graphics Processor__Foundry': 'TSMC',
            'Release_Year': 2025.65,         # ✅ 2025下半年 (V2版本)
            'Transistors_Million': 92200.0,
            'Die_Size_mm2': 750.0,
            'Process_Size_nm': 5.0,
            'TDP_Watts': 575.0,
            'FP32_GFLOPS': 104800.0,
            'Launch_Price': 2299.0,
            'Memory_MB': 24576.0,            # 24GB
            'Bandwidth_GBs': 1340.0,
            'GPU_Clock_MHz': 2017.0
        }
    ]
    
    df_future = pd.DataFrame(future_data)
    df_clean = pd.concat([df_clean, df_future], ignore_index=True)

    # ==========================================
    # 6. 计算衍生指标
    # ==========================================
    df_clean['Transistor_Density'] = df_clean['Transistors_Million'] / df_clean['Die_Size_mm2']
    df_clean['Perf_Per_Watt'] = df_clean['FP32_GFLOPS'] / df_clean['TDP_Watts']
    df_clean['Cost_Per_Transistor'] = df_clean['Launch_Price'] / df_clean['Transistors_Million']
    
    if 'Graphics Processor__Foundry' not in df_clean.columns:
        df_clean['Graphics Processor__Foundry'] = 'Unknown'
    df_clean['Graphics Processor__Foundry'] = df_clean['Graphics Processor__Foundry'].fillna('Unknown')

    return df_clean