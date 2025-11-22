# 文件路径: sections/contact.py
import streamlit as st
import urllib.parse # 用于处理 URL 编码

def show():
    st.markdown("## CONTACT & SUPPORT")
    st.markdown("### GET IN TOUCH OR BROWSE DOCUMENTATION")
    st.markdown("---")

    # 使用两列布局：左边是表单，右边是文档
    col1, col2 = st.columns([1, 1], gap="large")

    # === 左栏：联系表单 (GitHub 集成版) ===
    with col1:
        st.markdown("#### :material/attach_email: SEND A MESSAGE")
        st.caption("Submit bugs or feature requests directly to our GitHub Repository.")
        
        # 创建一个表单
        with st.form("contact_form"):
            st.caption("Fill in the details below to generate a pre-filled GitHub Issue.")
            
            # 输入框
            name = st.text_input("YOUR NAME")
            email = st.text_input("YOUR EMAIL (Optional)")
            topic = st.selectbox("TOPIC", ["Report Data Error", "Feature Request", "Academic Inquiry", "General Feedback"])
            message = st.text_area("MESSAGE", height=150, placeholder="Describe your issue or suggestion...")
            
            # 提交按钮：现在的作用是“生成链接”
            submitted = st.form_submit_button("PREPARE GITHUB ISSUE", use_container_width=True)
        
        # 表单提交后的逻辑
        if submitted:
            if not name or not message:
                st.error("Please fill in at least your NAME and MESSAGE.")
            else:
                # 1. 构建 GitHub Issue 的标题和正文
                issue_title = f"[{topic}] Feedback from {name}"
                issue_body = f"""**User:** {name}
**Email:** {email}
**Topic:** {topic}

**Message:**
{message}

*(Auto-generated from GPU-FINDER Dashboard)*"""
                
                # 2. URL 编码 (处理空格、换行符等)
                params = urllib.parse.urlencode({'title': issue_title, 'body': issue_body})
                github_url = f"https://github.com/yamheng/GpuAnalysis/issues/new?{params}"
                
                # 3. 显示跳转按钮
                st.success("Draft created! Click the button below to submit on GitHub:")
                st.link_button("OPEN GITHUB & SUBMIT", github_url, type="primary", use_container_width=True)

        st.markdown("---")
        st.markdown("#### :material/location_on: LAB LOCATION")
        st.markdown("""
        **Wuhan University of Technology** *Junshan Campus* 16 Hannan Avenue  
        Wuhan, China  
        *(EFREI Paris Joint Program)*
        """)

    # === 右栏：FAQ 和 引用 ===
    with col2:
        st.markdown("#### :material/help: FREQUENTLY ASKED QUESTIONS")
        
        with st.expander("WHERE DOES THE DATA COME FROM?"):
            st.markdown("""
            The dataset is scraped from **TechPowerUp GPU Specs Database**. 
            It covers over 3000 distinct SKUs released between 1986 and 2026. 
            We performed rigorous cleaning to standardize units (e.g., converting '4GB' and '512MB' to MB).
            """)
            
        with st.expander("HOW IS 'EFFICIENCY' CALCULATED?"):
            st.markdown("""
            Efficiency is defined as **GFLOPS per Watt**. 
            $$ Efficiency = \\frac{\\text{FP32 Performance (GFLOPS)}}{\\text{TDP (Watts)}} $$
            *Note: This metric uses 'Theoretical' performance, which may differ from real-world gaming benchmarks.*
            """)
            
        with st.expander("WHY IS THE 'ECONOMIC WALL' CURVE RISING?"):
            st.markdown("""
            Historically, cost per transistor dropped exponentially. 
            However, with the advent of **EUV Lithography** (7nm, 5nm, 3nm), the manufacturing cost per wafer has skyrocketed, offsetting the density gains.
            """)

        st.markdown("---")
        st.markdown("#### :material/library_books: CITATION")
        st.caption("If you use this tool for your research, please cite:")
        
        st.code("""
@misc{gpu_finder_2025,
  author = {Ruichen Liu},
  title = {GPU-FINDER: A Data Storytelling Dashboard},
  year = {2025},
  institution = {EFREI Paris / WUT},
  url = {https://github.com/yamheng/GpuAnalysis}
}
        """, language="bibtex")