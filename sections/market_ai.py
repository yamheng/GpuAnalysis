import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

def show(df):
    st.markdown("## :material/add_shopping_cart: AI MARKET SEGMENTATION")
    st.markdown("### HARDWARE CLUSTERS VS. PRICING STRATEGY")

    # === 1. 数据准备 (增加对价格的处理) ===
    ml_features = ['Process_Size_nm', 'Memory_MB', 'Bandwidth_GBs', 'TDP_Watts']
    
    # 过滤数据：必须同时有 硬件参数 和 价格 才能进行对比
    # 只看 2016 年以后的现代显卡，因为太老的卡价格体系不一样
    df_ml = df[(df['Release_Year'] >= 2016) & (df['Brand'].isin(['NVIDIA', 'AMD', 'Intel']))].copy()
    df_ml = df_ml.dropna(subset=ml_features + ['Launch_Price'])
    
    if len(df_ml) > 30:
        
        # === 2. 控制面板 (顶部) ===
        col_ctrl1, col_ctrl2 = st.columns([1, 2])
        
        with col_ctrl1:
            # 视图切换器：核心功能
            view_mode = st.radio(
                "COLOR SCHEME (VIEW MODE)", 
                ["AI Hardware Clusters (Specs)", "Market Price Tiers ($$$)"],
                horizontal=True
            )
            
        with col_ctrl2:
            # 如果是 AI 模式，显示聚类滑块
            if view_mode == "AI Hardware Clusters (Specs)":
                k = st.slider("AI CLUSTERS (K)", 2, 6, 4, help="How many groups should the AI divide the GPUs into?")
            else:
                st.info("Price Tiers are fixed: Entry (<$300), Mid ($300-600), High ($600-1000), Enthusiast (>$1000).")

        # === 3. 计算逻辑 ===
        
        # A. t-SNE 投影 (始终基于硬件参数)
        # 关键点：无论怎么着色，点的位置永远代表“性能/规格”。
        # 这样如果价格颜色分布和位置分布一致，就证明了“定价策略符合性能分级”。
        X = df_ml[ml_features]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 降维到 2D
        tsne = TSNE(n_components=2, random_state=42, perplexity=30)
        X_embedded = tsne.fit_transform(X_scaled)
        df_ml['tsne_x'] = X_embedded[:, 0]
        df_ml['tsne_y'] = X_embedded[:, 1]
        
        # B. 两种分类逻辑
        
        # 逻辑 1: AI K-Means (基于规格)
        kmeans = KMeans(n_clusters=k if view_mode == "AI Hardware Clusters (Specs)" else 4, random_state=42, n_init=10)
        df_ml['AI_Cluster'] = kmeans.fit_predict(X_scaled).astype(str)
        
        # 逻辑 2: 价格分段 (基于市场)
        # 定义价格区间
        price_bins = [0, 300, 600, 1000, 100000]
        price_labels = ['1. Entry Level (<$300)', '2. Mid-Range ($300-$600)', '3. High-End ($600-$1000)', '4. Enthusiast (>$1000)']
        df_ml['Price_Tier'] = pd.cut(df_ml['Launch_Price'], bins=price_bins, labels=price_labels)

        # === 4. 绘图 ===
        
        # 根据选择决定颜色列
        color_col = 'AI_Cluster' if view_mode == "AI Hardware Clusters (Specs)" else 'Price_Tier'
        title_text = f"t-SNE Projection colored by {view_mode}"
        
        # 定义颜色映射，让价格看起来更直观 (冷色便宜 -> 暖色贵)
        price_color_map = {
            '1. Entry Level (<$300)': '#a1c9f4',  # 浅蓝
            '2. Mid-Range ($300-$600)': '#8de5a1', # 浅绿
            '3. High-End ($600-$1000)': '#ff9f9b', # 浅红
            '4. Enthusiast (>$1000)': '#de5253'    # 深红
        }
        
        fig = px.scatter(
            df_ml, 
            x='tsne_x', 
            y='tsne_y', 
            color=color_col,
            color_discrete_map=price_color_map if view_mode == "Market Price Tiers ($$$)" else None,
            hover_data=['Name', 'Launch_Price', 'TDP_Watts', 'Release_Year'],
            title=None,
            size='TDP_Watts', # 气泡大小代表功耗
            size_max=15,
            height=600
        )
        
        # 美化图表 (去掉坐标轴，只看分布)
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(showgrid=False, showticklabels=False, title=""),
            legend=dict(title=dict(text="Segment Group"), orientation="h", y=1.05, x=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Oswald, sans-serif")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
# === 5. 商业洞察 (Business Insight) - 样式修正 ===
        st.markdown("---")
        col_txt1, col_txt2 = st.columns(2, gap="large")
        
        # 定义一个简单的黑框样式
        box_style = """
        border: 2px solid black; 
        padding: 20px; 
        background-color: white; 
        height: 100%;
        """
        
        with col_txt1:
            st.markdown("#### :material/search: HOW TO READ THIS?")
            # 替换 st.info 为自定义 HTML
            st.markdown(f"""
            <div style="{box_style}">
                <ul style="margin: 0; padding-left: 20px;">
                    <li><b>The Position (X, Y):</b> Determined purely by <b>Hardware Specs</b>. Similar cards are close together.</li>
                    <li style="margin-top: 10px;"><b>The Color:</b> Determined by your selection (<b>AI Grouping</b> or <b>Price Tag</b>).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_txt2:
            st.markdown("#### :material/lightbulb: THE STRATEGY REVEALED")
            # 替换 st.warning 为自定义 HTML
            st.markdown(f"""
            <div style="{box_style}">
                <p><b>Try switching the view!</b> If the <b>Price Colors</b> align perfectly with the <b>Hardware Clusters</b>, it proves <b>Pricing Efficiency</b>.</p>
                <hr style="border-top: 1px dashed black; margin: 10px 0;">
                <p><b>Mismatch?</b> If you see a <span style="color:#de5253; font-weight:bold;">Red Dot</span> (Expensive) inside a <span style="color:#a1c9f4; font-weight:bold;">Blue Island</span> (Low Spec), that is an <b>overpriced product</b>!</p>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("Insufficient data with Price information for clustering.")