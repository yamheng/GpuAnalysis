import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show(df):
    st.markdown("## :material/ssid_chart: Moore's Law (Physical Limits)")
    st.markdown("### Chapter 1: The Physical Wall")
    
    # 1. 过滤器
    with st.expander("Filter Settings", expanded=False, icon=":material/shield_locked:"):
        foundries = df['Graphics Processor__Foundry'].unique()
        sel_foundry = st.multiselect("FOUNDRY", foundries, default=['TSMC', 'Samsung', 'Intel', 'GlobalFoundries', 'UMC'])
        show_reg = st.checkbox("SHOW REGRESSION", True)

    df_sub = df[df['Graphics Processor__Foundry'].isin(sel_foundry) & (df['Release_Year'] > 1990)].copy()
    
    # 2. 绘图函数化 (减少代码重复)
    def plot_scatter(data, x, y, color_map, title, y_log=False):
        fig = go.Figure()
        for f in sel_foundry:
            d = data[data['Graphics Processor__Foundry'] == f]
            if d.empty: continue
            fig.add_trace(go.Scattergl(
                x=d[x], y=d[y], mode='markers', name=f,
                marker=dict(color=color_map.get(f, 'grey'), size=8, line=dict(width=1, color='white')),
                hovertemplate=f"<b>%{{text}}</b><br>{y}: %{{y}}<br>Year: %{{x}}<extra></extra>", text=d['Name']
            ))
        return fig

    # 图 1: 晶体管密度
    cmap = {'TSMC':'#FF6347', 'Samsung':'#32CD32', 'Intel':"#1D5DBC", 'GlobalFoundries':'#911EB4', 'UMC':"#EEF10F"}
    fig1 = plot_scatter(df_sub, 'Release_Year', 'Transistor_Density', cmap, "Density")
    
    # 添加工艺制程线 (右轴)
    trend = df_sub.groupby('Release_Year')['Process_Size_nm'].min().reset_index()
    fig1.add_trace(go.Scatter(x=trend['Release_Year'], y=trend['Process_Size_nm'], name='Process Node (nm)', 
                             line=dict(color='black', width=3, dash='dot'), yaxis='y2'))
    
    if show_reg:
        d_reg = df_sub.dropna(subset=['Transistor_Density'])
        if len(d_reg) > 10:
            m, b = np.polyfit(d_reg['Release_Year'], np.log10(d_reg['Transistor_Density']), 1)
            x_rng = np.linspace(d_reg['Release_Year'].min(), d_reg['Release_Year'].max(), 100)
            fig1.add_trace(go.Scatter(x=x_rng, y=10**(m*x_rng+b), name='Moore Law Fit', line=dict(color='grey')))

    fig1.update_layout(
        title="Transistor Density vs Process Node", 
        yaxis_type="log", 
        # ✅ 修复1: 添加坐标轴标签
        xaxis=dict(title="Release Year"),
        yaxis=dict(title="Transistor Density (M/mm²) - Log Scale"),
        yaxis2=dict(
            overlaying='y', 
            side='right', 
            autorange="reversed",
            title="Process Node (nm)" # 右轴标签
        ), 
        height=600, 
        font=dict(family="Oswald"),
        # ✅ 修复2: 减少上下留白 (t=top, b=bottom)
        margin=dict(t=50, b=50, l=60, r=60) 
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # 图 2: Die Size (Chiplet 标注)
    st.markdown("### :material/shield_locked: The Physical Wall: Reticle Limit vs. Chiplets")
    st.markdown("Standard chips hit the wall at ~858mm². Points above this line use **Chiplet (MCM)** technology.")
    fig2 = go.Figure()
    
    # 普通点
    d_die = df.dropna(subset=['Die_Size_mm2'])
    fig2.add_trace(go.Scatter(x=d_die['Release_Year'], y=d_die['Die_Size_mm2'], mode='markers', name='Single Die', 
                             marker=dict(color='black', opacity=0.3)))
    
    # Chiplet 点 (>858mm2)
    d_big = d_die[d_die['Die_Size_mm2'] > 858]
    fig2.add_trace(go.Scatter(x=d_big['Release_Year'], y=d_big['Die_Size_mm2'], mode='markers', name='Chiplet/MCM', 
                             marker=dict(color='red', symbol='star', size=10)))
    
    fig2.add_hline(y=858, line=dict(color='red', dash='dash'), annotation_text="Reticle Limit")
    
    fig2.update_layout(
        title="Die Size Evolution", 
        # ✅ 修复1: 添加坐标轴标签
        xaxis=dict(title="Release Year"),
        yaxis=dict(title="Die Size (mm²)"),
        height=500, 
        font=dict(family="Oswald"),
        # ✅ 修复2: 减少上下留白
        margin=dict(t=50, b=50, l=60, r=60)
    )
    st.plotly_chart(fig2, use_container_width=True)