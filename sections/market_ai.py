# 文件路径: sections/market_ai.py
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

def show(df):
    st.markdown("## 🤖 AI Market Segmentation")
    st.markdown("### Experiment: Can Unsupervised Learning identify market segments?")

    # 1. 准备数据
    ml_features = ['Process_Size_nm', 'Memory_MB', 'Bandwidth_GBs', 'TDP_Watts']
    df_ml = df[(df['Release_Year'] >= 2016) & (df['Brand'].isin(['NVIDIA', 'AMD']))].dropna(subset=ml_features).copy()
    
    if len(df_ml) > 50:
        # 2. 控件区 (放在顶部)
        col_ctrl, col_text = st.columns([1, 2])
        with col_ctrl:
            k = st.slider("Select Clusters (K)", 2, 6, 4)
        with col_text:
            st.info("The AI projects 4D hardware specs (Process, Memory, Bandwidth, TDP) into 2D space using t-SNE.")

        # 3. 计算
        X = df_ml[ml_features]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        df_ml['Cluster'] = kmeans.fit_predict(X_scaled).astype(str)
        
        tsne = TSNE(n_components=2, random_state=42, perplexity=30)
        X_embedded = tsne.fit_transform(X_scaled)
        df_ml['tsne_x'] = X_embedded[:, 0]
        df_ml['tsne_y'] = X_embedded[:, 1]
        
        # 4. 绘图
        fig = px.scatter(
            df_ml, x='tsne_x', y='tsne_y', color='Cluster',
            hover_data=['Name', 'Release_Year', 'TDP_Watts'],
            title=f"t-SNE Projection (K={k})",
            size='TDP_Watts', size_max=15,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Not enough data points for clustering.")