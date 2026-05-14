"""
LocalizationOps AI — 国际化产品运营 Demo 平台
=============================================
展示 国际化产品运营 / AI 内容本地化 核心能力的交互式 Web 应用。

功能模块：
1. 🎯 AI 翻译质量评估
2. 📖 术语一致性检查
3. 🌍 国际化就绪度评分
4. ✍️ AI 双语产品文案生成
5. 🕌 文化敏感度检测
6. 💬 用户反馈分析器
7. 📊 国际化产品运营数据看板
"""

import streamlit as st
from utils.llm_client import ask_deepseek

# ── Page config ──
st.set_page_config(
    page_title="LocalizationOps AI — 国际化产品运营 Demo",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ──
st.sidebar.markdown("# 🌐 LocalizationOps AI")
st.sidebar.markdown("国际化产品运营 · AI 内容本地化 · Demo 平台")
st.sidebar.divider()

# Module list with descriptions
MODULES = {
    "🏠 首页介绍": "home",
    "🎯 翻译质量评估": "translation_quality",
    "📖 术语一致性检查": "terminology_check",
    "🌍 国际化就绪度评分": "readiness_score",
    "✍️ 双语文案生成": "copy_generator",
    "🕌 文化敏感度检测": "cultural_check",
    "💬 用户反馈分析器": "feedback_analyzer",
    "📊 运营数据看板": "operations_dashboard",
}

selected_module = st.sidebar.radio(
    "功能模块导航",
    list(MODULES.keys()),
    label_visibility="collapsed",
)
module_key = MODULES[selected_module]

st.sidebar.divider()
st.sidebar.markdown("**关于这个 Demo**")
st.sidebar.markdown("""
这是一个展示 **国际化产品运营** 和 **AI 内容本地化** 核心能力的交互式平台。

由 Xujun Wang 构建，用于展示在 AI 内容运营、本地化质量管理和国际化产品策略方面的实战能力。

🔗 [Portfolio](https://wangxujun0516.github.io/portfolio-site/)
""")

# Footer
st.sidebar.divider()
st.sidebar.caption("Powered by DeepSeek API · Streamlit")


# ── Home page ──
def show_home():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("# 🌐 LocalizationOps AI")
        st.markdown("## 国际化产品运营 · AI 内容本地化 · Demo 平台")

        st.markdown("""
        这个平台展示了一个国际化产品运营从业者的核心能力：
        """)

        features = [
            ("🎯", "翻译质量评估", "从准确度、风格、术语、文化适配等多维度评估 AI 翻译质量"),
            ("📖", "术语一致性检查", "确保产品多语言内容中的术语翻译一致、专业"),
            ("🌍", "国际化就绪度评分", "评估产品内容在不同目标市场的国际化就绪程度"),
            ("✍️", "双语产品文案生成", "AI 辅助创作英文产品文案，附带中文本地化备注"),
            ("🕌", "文化敏感度检测", "检测内容在特定海外市场是否存在文化敏感问题"),
            ("💬", "用户反馈分析器", "自动分类海外用户评价，识别关键问题并排优先级"),
            ("📊", "运营数据看板", "模拟国际化产品运营的核心指标追踪与可视化"),
        ]
        for icon, title, desc in features:
            st.markdown(f"### {icon} **{title}**")
            st.markdown(f"{desc}")

    with col2:
        st.markdown("### 关于我")
        st.info("""
        **Xujun Wang**
        
        6年+ 国际化产品运营与 AI 内容本地化经验
        
        曾服务于：
        - ByteDance (Coze AI)
        - NetEase RTC
        - Alibaba Cloud
        """)
        st.markdown("### 如何使用")
        st.markdown("左侧导航栏选择功能模块，每个模块都有输入框和示例数据按钮，可以快速体验。")
        st.markdown("所有功能都基于 DeepSeek API，实时调用 AI 分析。")

    # Quick demo
    st.divider()
    st.markdown("### 💡 快速体验 — 试试翻译质量评估")
    col1, col2 = st.columns(2)
    with col1:
        demo_source = "Our AI agent platform empowers developers to build custom assistants with just a few lines of code."
    with col2:
        demo_target = "我们的 AI 智能体平台让开发者只需几行代码就能构建自定义助手。"

    st.markdown(f"""
    **源文：** {demo_source}
    **译文：** {demo_target}
    """)

    if st.button("👉 跳转到翻译质量评估试试看", type="primary"):
        st.switch_page("app.py")  # fallback — just hint


# ── Route modules ──
def main():
    if module_key == "home":
        show_home()
    elif module_key == "translation_quality":
        from modules.translation_quality import run
        run()
    elif module_key == "terminology_check":
        from modules.terminology_check import run
        run()
    elif module_key == "readiness_score":
        from modules.readiness_score import run
        run()
    elif module_key == "copy_generator":
        from modules.copy_generator import run
        run()
    elif module_key == "cultural_check":
        from modules.cultural_check import run
        run()
    elif module_key == "feedback_analyzer":
        from modules.feedback_analyzer import run
        run()
    elif module_key == "operations_dashboard":
        from modules.operations_dashboard import run
        run()


if __name__ == "__main__":
    main()
