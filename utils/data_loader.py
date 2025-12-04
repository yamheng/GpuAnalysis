import pandas as pd
import numpy as np
import re
import streamlit as st
import os

@st.cache_data
def load_and_clean_data():
    # Read data correctly
    file_path = 'gpu_1986-2026.csv' if os.path.exists('gpu_1986-2026.csv') else 'data/gpu_1986-2026.csv'
    try:
        df = pd.read_csv(file_path, dtype=str).applymap(lambda x: x.strip() if isinstance(x, str) else x)
    except:
        return pd.DataFrame()

    # 2. Delete old 5090 data (The data of 5090 graphics cards delivered on the market has been slightly adjusted. To ensure accuracy, I will use the data I found on the market below)
    df = df[~df['Name'].str.contains('GeForce RTX 5090', case=False, na=False)].copy()

    # 3. Universal Parsing Tool (Solves All Number Extraction)
    def extract_num(val, scale=1):
        if pd.isna(val) or str(val).lower() in ['unknown', 'system shared']: return np.nan
        s = str(val).lower().replace(',', '').replace('"', '')
        matches = re.findall(r"[\d\.]+", s)
        if not matches: return np.nan
        num = float(matches[0]) * scale
        # Unit conversion
        if 'billion' in s or 'ghz' in s or 'tflops' in s or 'gb' in s: return num * 1000
        if 'kb' in s or 'mb/s' in s: return num / 1024
        return num

    # 4. Apply cleaning rules in batches
    clean_map = {
        'Transistors_Million': ('Graphics Processor__Transistors', 1),
        'Die_Size_mm2': ('Graphics Processor__Die Size', 1),
        'Memory_MB': ('Memory__Memory Size', 1),
        'TDP_Watts': ('Board Design__TDP', 1),
        'Process_Size_nm': ('Graphics Processor__Process Size', 1),
        'Bandwidth_GBs': ('Memory__Bandwidth', 1),
        'FP32_GFLOPS': ('Theoretical Performance__FP32 (float)', 1),
        'GPU_Clock_MHz': ('Clock Speeds__GPU Clock', 1),
        'Launch_Price': ('Graphics Card__Launch Price', 1)
    }

    for new_col, (old_col, scale) in clean_map.items():
        df[new_col] = df[old_col].apply(lambda x: extract_num(x, scale))

    # Dates are handled separately
    df['Release_Date'] = pd.to_datetime(df['Graphics Card__Release Date'].apply(
        lambda x: re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(x)) if pd.notna(x) else pd.NaT
    ), errors='coerce')
    df['Release_Year'] = df['Release_Date'].dt.year.astype(float)

    # 5. Manually inject the latest 5090 data
    future_specs = [
        ('GeForce RTX 5090', 2025.05, 1999.0),
        ('GeForce RTX 5090 D', 2025.20, 2299.0),
        ('GeForce RTX 5090 D V2', 2025.65, 2299.0)
    ]
    
    new_rows = []
    for name, year, price in future_specs:
        mem = 24576.0 if 'V2' in name else 32768.0
        bw = 1340.0 if 'V2' in name else 1790.0
        new_rows.append({
            'Name': name, 'Brand': 'NVIDIA', 'Graphics Processor__Architecture': 'Blackwell',
            'Graphics Processor__Foundry': 'TSMC', 'Release_Year': year, 'Launch_Price': price,
            'Transistors_Million': 92200.0, 'Die_Size_mm2': 750.0, 'Process_Size_nm': 5.0,
            'TDP_Watts': 575.0, 'FP32_GFLOPS': 104800.0, 'Memory_MB': mem, 
            'Bandwidth_GBs': bw, 'GPU_Clock_MHz': 2235.0
        })
    
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    # 6. Imputing missing values and calculating derived indicators
    df['Graphics Processor__Foundry'] = df['Graphics Processor__Foundry'].fillna('Unknown')
    
    # 2023+ Frequency Completion
    avg_clocks = df.groupby(df['Release_Year'].fillna(0).astype(int))['GPU_Clock_MHz'].mean()
    df['GPU_Clock_MHz'] = df.apply(
        lambda r: avg_clocks.get(int(r['Release_Year']), 2000) if pd.isna(r['GPU_Clock_MHz']) and r['Release_Year'] >= 2020 else r['GPU_Clock_MHz'], 
        axis=1
    )

    df['Transistor_Density'] = df['Transistors_Million'] / df['Die_Size_mm2']
    df['Perf_Per_Watt'] = df['FP32_GFLOPS'] / df['TDP_Watts']
    df['Cost_Per_Transistor'] = df['Launch_Price'] / df['Transistors_Million']

    return df