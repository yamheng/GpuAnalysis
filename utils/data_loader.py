import pandas as pd
import numpy as np
import re
import streamlit as st

@st.cache_data
def load_and_clean_data():
    # 1. 读取数据 (兼容不同路径)
    try:
        df = pd.read_csv('data/gpu_1986-2026.csv')
    except FileNotFoundError:
        try:
            df = pd.read_csv('gpu_1986-2026.csv')
        except:
            st.error("Critical Error: 'gpu_1986-2026.csv' not found.")
            return pd.DataFrame()

    df_clean = df.copy()

    # ==========================================
    # 2. 定义所有的清洗函数 (Helper Functions)
    # ==========================================
    
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

    # --- 新增：解析价格 (Launch Price) ---
    def parse_price(val):
        if pd.isna(val): return np.nan
        val_str = str(val).replace(',', '').replace('$', '') # 去掉逗号和美元符
        match = re.search(r"(\d+\.?\d*)", val_str)
        return float(match.group(1)) if match else np.nan

    # --- 新增：解析频率 (GPU Clock) ---
    def parse_clock(val):
        if pd.isna(val): return np.nan
        val_str = str(val).lower().replace(',', '')
        match = re.search(r"(\d+)", val_str)
        if not match: return np.nan
        num = float(match.group(1))
        if 'mhz' in val_str: return num
        elif 'ghz' in val_str: return num * 1000 # 统一转换为 MHz
        return num

    # ==========================================
    # 3. 应用清洗 (注意顺序！)
    # ==========================================
    
    # 第一步：生成基础数值列 (Transistors_Million 必须在这里生成)
    df_clean['Transistors_Million'] = df_clean['Graphics Processor__Transistors'].apply(parse_transistors)
    df_clean['Memory_MB'] = df_clean['Memory__Memory Size'].apply(parse_memory_size)
    df_clean['TDP_Watts'] = df_clean['Board Design__TDP'].apply(parse_tdp)
    df_clean['Process_Size_nm'] = df_clean['Graphics Processor__Process Size'].apply(parse_process_size)
    df_clean['Die_Size_mm2'] = df_clean['Graphics Processor__Die Size'].apply(parse_die_size)
    df_clean['Bandwidth_GBs'] = df_clean['Memory__Bandwidth'].apply(parse_bandwidth)
    df_clean['Release_Date'] = df_clean['Graphics Card__Release Date'].apply(parse_date)
    df_clean['Release_Year'] = df_clean['Release_Date'].dt.year
    df_clean['FP32_GFLOPS'] = df_clean['Theoretical Performance__FP32 (float)'].apply(parse_gflops)
    
    # 第二步：生成新加入的列
    df_clean['Launch_Price'] = df_clean['Graphics Card__Launch Price'].apply(parse_price)
    df_clean['GPU_Clock_MHz'] = df_clean['Clock Speeds__GPU Clock'].apply(parse_clock)

    # 第三步：计算衍生指标 (依赖上面的列)
    # 1. 晶体管密度 (依赖 Transistors_Million 和 Die_Size_mm2)
    df_clean['Transistor_Density'] = df_clean['Transistors_Million'] / df_clean['Die_Size_mm2']

    # 2. 能效比 (依赖 FP32_GFLOPS 和 TDP_Watts)
    df_clean['Perf_Per_Watt'] = df_clean['FP32_GFLOPS'] / df_clean['TDP_Watts']
    
    # 3. 每晶体管成本 (依赖 Launch_Price 和 Transistors_Million)
    # 之前报错就是因为这行跑得太早了，现在把它放在最后，确保分母分子都存在
    df_clean['Cost_Per_Transistor'] = df_clean['Launch_Price'] / df_clean['Transistors_Million']

    return df_clean