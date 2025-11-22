# 文件路径: sections/memory_wall.py
import streamlit as st
import plotly.graph_objects as go

def show(df):
    st.markdown("## :material/shield_locked: The Memory Wall Analysis")
    st.markdown("### BANDWIDTH BOTTLENECKS & TECHNOLOGY FLOW")

# === PART 1: 交互式桑基图 ===
    st.markdown("#### 1. STRATEGY MAP: FROM CHAOS TO ORDER")
    st.caption("Toggle the switch below to filter out the noise and see the Big Three's strategy.")

    # 1. 控制开关 (Toggle Switch)
    # 默认 False (显示盘丝洞)，点击变为 True (显示清晰图)
    is_focus_mode = st.toggle("FOCUS MODE: FILTER NOISE & HIGHLIGHT BIG 3", value=False)

    # 2. 数据准备
    # 基础清洗
    df_sankey = df.dropna(subset=['Brand', 'Memory__Memory Type'])
    
    # 定义主要显存类型（用于清洗名字）
    target_mems = ['GDDR6X', 'GDDR6', 'HBM2', 'HBM2e', 'HBM3', 'GDDR5', 'GDDR5X', 'HBM', 'DDR3', 'DDR4', 'SDRAM', 'DDR']
    df_sankey['Clean_Mem'] = df_sankey['Memory__Memory Type'].apply(lambda x: next((m for m in target_mems if m in str(x)), "Other"))

    # === 分支逻辑：根据开关状态选择数据 ===
    if is_focus_mode:
        # --- 模式 A: 清晰模式 (你原来的图) ---
        # 只看 2015 年以后，只看三大家
        df_sankey = df_sankey[df_sankey['Release_Year'] >= 2015]
        df_sankey = df_sankey[df_sankey['Brand'].isin(['NVIDIA', 'AMD', 'Intel'])]
        df_sankey = df_sankey[df_sankey['Clean_Mem'] != "Other"] # 去掉杂项
        title_text = "Strategic Divergence (2015-2026): The Big Three"
    else:
        # --- 模式 B: 盘丝洞模式 (历史全貌) ---
        # 保留更多历史数据，保留更多小厂商 (ATI, 3dfx, Matrox...)
        # 为了防止浏览器崩溃，我们只保留出现频率前 15 的厂商
        top_brands = df_sankey['Brand'].value_counts().head(15).index
        df_sankey = df_sankey[df_sankey['Brand'].isin(top_brands)]
        title_text = "The Chaos of History (1986-2026): All Vendors"

    # 3. 计算流量
    flow = df_sankey.groupby(['Brand', 'Clean_Mem']).size().reset_index(name='Count')

    # 4. 定义节点
    brands = list(flow['Brand'].unique())
    mem_types = list(flow['Clean_Mem'].unique())
    all_nodes = brands + mem_types
    node_map = {name: i for i, name in enumerate(all_nodes)}

    # 5. 动态配色逻辑
    node_colors = []
    link_colors = []

    if is_focus_mode:
        # === 清晰模式配色：品牌色 ===
        for node in all_nodes:
            if "NVIDIA" in node: node_colors.append("#7DB816") # Nvidia Green
            elif "AMD" in node: node_colors.append("#ED1C24")    # AMD Red
            elif "Intel" in node: node_colors.append("#0071C5")  # Intel Blue
            else: node_colors.append("#333333")                  # Memory Black
        
        for b in flow['Brand']:
            if "NVIDIA" in b: link_colors.append("rgba(118, 185, 0, 0.4)")
            elif "AMD" in b: link_colors.append("rgba(237, 28, 36, 0.4)")
            elif "Intel" in b: link_colors.append("rgba(0, 113, 197, 0.4)")
            else: link_colors.append("rgba(0,0,0,0.2)")
            
    else:
        # === 盘丝洞模式配色：黑白工业风 (不同深浅的灰) ===
        # 让它们看起来复杂、交织，但不刺眼
        for node in all_nodes:
            node_colors.append("black") # 节点全黑
        
        # 连线使用半透明灰色，制造"网"的感觉
        link_colors = ["rgba(0, 0, 0, 0.15)"] * len(flow)

    # 6. 绘图
    fig_sankey = go.Figure(data=[go.Sankey(
        textfont=dict(color="black", size=12, family="Oswald"),
        node=dict(
            pad=15, thickness=15,
            line=dict(color="white", width=0.5),
            label=all_nodes,
            color=node_colors
        ),
        link=dict(
            source=[node_map[b] for b in flow['Brand']],
            target=[node_map[m] for m in flow['Clean_Mem']],
            value=flow['Count'],
            color=link_colors
        )
    )])
    
    fig_sankey.update_layout(
        title_text=title_text, 
        font_family="Oswald",
        height=600
    )
    st.plotly_chart(fig_sankey, use_container_width=True)

    st.divider()
# === 2. 原有的带宽趋势图 (保留) ===
    st.markdown("#### 2. THE BANDWIDTH GAP")
    # 1. 数据聚合
    df_trend = df[(df['Release_Year'] >= 2010) & (df['Release_Year'] <= 2024)].copy()
    annual_stats = df_trend.groupby('Release_Year')[['FP32_GFLOPS', 'Bandwidth_GBs']].mean().reset_index()
    
    # 2. 计算指数 (Base 2013 = 100)
    base_year = 2013
    base_row = annual_stats[annual_stats['Release_Year'] == base_year]
    
    if not base_row.empty:
        base_compute = base_row['FP32_GFLOPS'].values[0]
        base_bw = base_row['Bandwidth_GBs'].values[0]
        
        annual_stats['Compute_Index'] = (annual_stats['FP32_GFLOPS'] / base_compute) * 100
        annual_stats['Bandwidth_Index'] = (annual_stats['Bandwidth_GBs'] / base_bw) * 100
        
        # 3. 绘图
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=annual_stats['Release_Year'], y=annual_stats['Compute_Index'], name='Compute Growth', line=dict(color='#FF4B4B', width=4)))
        fig.add_trace(go.Scatter(x=annual_stats['Release_Year'], y=annual_stats['Bandwidth_Index'], name='Bandwidth Growth', line=dict(color='#1f77b4', width=4), fill='tonexty', fillcolor='rgba(255, 75, 75, 0.2)'))

        fig.update_layout(
            title="The Growing Gap: Compute vs Bandwidth (Index 100 = 2013)",
            yaxis_title="Growth Index",
            height=600,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The red shaded area represents the **Memory Wall**. Compute is growing much faster than bandwidth.")
    else:
        st.error("Insufficient data for base year 2013.")