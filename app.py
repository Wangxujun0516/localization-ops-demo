"""
LocalizationOps AI — 国际化产品运营 Demo 平台
=============================================
展示 国际化产品运营 / AI 内容本地化 核心能力的交互式 Web 应用。

核心功能：一键本地化审计 → 输入产品内容，AI 自动输出完整的国际化运营评估报告。
进阶工具：独立功能模块供深度分析和日常使用。
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
st.sidebar.markdown("""
# 🌐 LocalizationOps AI
#### 国际化产品运营 · AI 内容本地化
""")
st.sidebar.divider()

# Main workflow + advanced tools
MENU_ITEMS = {
    "🚀 一键本地化审计": "audit",
    "─── 进阶工具 ───": None,
    "🎯 翻译质量评估": "translation_quality",
    "📖 术语一致性检查": "terminology_check",
    "🌍 国际化就绪度评分": "readiness_score",
    "✍️ 双语文案生成": "copy_generator",
    "🕌 文化敏感度检测": "cultural_check",
    "💬 用户反馈分析器": "feedback_analyzer",
    "📊 运营数据看板": "operations_dashboard",
}

selected_label = st.sidebar.radio(
    "导航",
    [k for k in MENU_ITEMS if MENU_ITEMS[k] is not None],
    label_visibility="collapsed",
)
module_key = MENU_ITEMS[selected_label]

st.sidebar.divider()
st.sidebar.markdown("**关于**")
st.sidebar.markdown("""
展示 **国际化产品运营** 和 **AI 内容本地化** 的实战能力。

[Xujun Wang](https://wangxujun0516.github.io/portfolio-site/)
""")
st.sidebar.caption("Powered by DeepSeek API · Streamlit")


# ── One-Click Localization Audit ──
AUDIT_SYSTEM_PROMPT = """你是一位资深国际化产品运营专家。请对以下产品内容进行全面的"本地化审计"(Localization Audit)。

你需要从以下维度进行全面评估，输出一份结构化的审计报告。

输出格式（严格 JSON，中文回答）：
{
  "report_title": "审计报告标题",
  "overall_score": <1-100的整数>,
  "summary": "总体评价（3-5句）",
  "sections": [
    {
      "title": "维度名称",
      "icon": "表情符号",
      "score": <1-100>,
      "findings": [
        {"severity": "high/medium/low/info", "finding": "发现的问题", "recommendation": "改进建议"}
      ],
      "strengths": ["优点1", "优点2"],
      "action_items": [
        {"priority": "P0/P1/P2", "action": "具体行动项"}
      ]
    }
  ],
  "quick_wins": ["可以快速改进的 3 个点"],
  "priority_matrix": {
    "immediate": ["必须马上处理的"},
    "this_quarter": ["本季度内完成"],
    "next_phase": ["下阶段优化"]
  },
  "market_readiness": "一句话结论"
}

审计维度（每个维度的评估要求）：
1. 文化适配 (Cultural Fit) — 检查是否存在宗教、颜色、符号、幽默、性别等文化敏感问题
2. 本地化质量 (L10n Quality) — 评估翻译准确性、术语一致性、风格适配度
3. 产品就绪度 (Product Readiness) — 检查日期/货币/单位格式、UI空间、RTL支持等
4. 合规与隐私 (Compliance) — GDPR、CCPA、数据跨境等潜在风险
5. 市场竞争力 (Market Fit) — 内容是否符合当地用户习惯、竞品对比
"""

TARGET_MARKETS = [
    "东南亚 (SEA) — 印尼、泰国、越南、菲律宾、马来西亚",
    "中东 (MENA) — 沙特、阿联酋、埃及等",
    "拉丁美洲 — 巴西、墨西哥、阿根廷等",
    "日本",
    "韩国",
    "印度",
    "欧洲 — 德法英意西等",
    "北美 — 美国、加拿大",
]

AUDIT_SAMPLE = """Coze AI Agent Platform — 扣子国际版

Product Description:
Coze is an AI agent development platform that allows developers and businesses to build, customize, and deploy AI agents and assistants. Users can create agents using natural language configuration, connect them to external tools and APIs, and publish across multiple channels including web, messaging apps, and APIs.

Key Features:
• Natural language agent configuration — build assistants without coding
• Plugin marketplace — 100+ pre-built tools (search, image generation, data analysis)
• Knowledge base integration — connect to your documents, databases, and APIs
• Multi-channel deployment — publish to web, Telegram, Discord, Slack
• Workflow editor — visual drag-and-drop for complex agent behaviors
• Analytics dashboard — track agent usage, user engagement, and performance

Target Users:
• Developers (primary): engineers building AI-powered products
• Business users (secondary): product managers, growth teams, customer support

Current Languages:
• English (primary), Chinese, Japanese, Korean, Spanish (partial), Arabic (partial)

Current Coverage Gaps:
• Arabic: RTL support is incomplete, UI breaks in some pages
• Japanese/Korean: terminology inconsistency across different modules
• Spanish: only covers 60% of the platform UI
• Portuguese: not yet supported (Brazil market demand)
"""


def show_audit():
    st.markdown("# 🚀 一键本地化审计")
    st.markdown("""
    输入你的产品内容（文案、功能描述、UI字符串），选择目标市场，AI 自动从 **文化适配、本地化质量、合规、市场竞争力** 等多个维度进行完整评估，输出一份可落地的运营报告。
    """)

    col1, col2 = st.columns([2, 1])
    with col1:
        target_market = st.selectbox("选择目标市场", TARGET_MARKETS, index=0)
    with col2:
        sample_btn = st.button("📥 加载示例产品数据（扣子国际版）")

    content = st.text_area("产品内容", height=250,
                           placeholder=("粘贴你的产品文案、功能描述、UI 字符串、或产品说明...\n\n"
                                        "内容越详细，审计报告越精准。"))

    if sample_btn:
        content = AUDIT_SAMPLE
        st.rerun()

    # Run audit
    audit_col1, audit_col2, _ = st.columns([1, 1, 3])
    with audit_col1:
        run_audit = st.button("🚀 运行完整审计", type="primary", use_container_width=True)
    with audit_col2:
        pass

    if run_audit:
        if not content:
            st.warning("请先输入产品内容，或点击「加载示例数据」。")
            return

        with st.spinner(f"AI 正在对 {target_market.split('—')[0].strip()} 市场进行本地化审计..."):
            user_prompt = f"目标市场：{target_market}\n\n产品内容：\n{content}"
            result = ask_deepseek(AUDIT_SYSTEM_PROMPT, user_prompt, temperature=0.3, max_tokens=4096)

        try:
            import json
            data = json.loads(result)

            # ── Report Header ──
            st.markdown("---")
            st.markdown(f"## 📋 {data.get('report_title', '本地化审计报告')}")
            st.markdown(f"**目标市场：** {data.get('market_readiness', target_market)}")

            # Overall score with gauge
            total = data.get("overall_score", 0)
            bar_color = "green" if total >= 70 else ("orange" if total >= 40 else "red")
            st.markdown(f"### 综合评分: {total}/100")
            st.markdown(f"""
            <div style="background:#262730; border-radius:10px; padding:3px; margin-bottom:20px;">
              <div style="background:{bar_color}; width:{total}%; border-radius:10px; padding:8px; text-align:center; color:white; font-weight:bold;">
                {total}%
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.info(data.get("summary", ""))

            # ── Section By Section ──
            sections = data.get("sections", [])
            for sec in sections:
                with st.expander(f"{sec.get('icon', '📋')} **{sec.get('title', '')}** — 评分: {sec.get('score', 'N/A')}/100", expanded=True):
                    score = sec.get("score", 0)
                    color = "🟢" if score >= 70 else ("🟡" if score >= 40 else "🔴")
                    st.markdown(f"{color} **评分: {score}/100**")

                    if sec.get("findings"):
                        for f in sec["findings"]:
                            sev = f.get("severity", "info")
                            icon = {"high": "🔴", "medium": "🟡", "low": "💡", "info": "📌"}.get(sev, "📌")
                            st.markdown(f"{icon} **{f.get('finding', '')}**")
                            st.markdown(f"  → *建议：* {f.get('recommendation', '')}")

                    if sec.get("strengths"):
                        st.markdown("✅ **优势：**")
                        for s in sec["strengths"]:
                            st.markdown(f"- {s}")

                    if sec.get("action_items"):
                        st.markdown("📋 **行动项：**")
                        for item in sec["action_items"]:
                            p = item.get("priority", "P2")
                            st.markdown(f"  **{p}** — {item.get('action', '')}")

            # ── Quick Wins ──
            if data.get("quick_wins"):
                st.markdown("---")
                st.markdown("### ⚡ 快速优化建议（Quick Wins）")
                cols = st.columns(len(data["quick_wins"]))
                for i, qw in enumerate(data["quick_wins"]):
                    cols[i].success(qw)

            # ── Priority Matrix ──
            pm = data.get("priority_matrix", {})
            if pm:
                st.markdown("---")
                st.markdown("### 📅 优先级矩阵")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.error("🔴 **立即处理**")
                    for item in pm.get("immediate", []):
                        st.markdown(f"- {item}")
                with col2:
                    st.warning("🟡 **本季度**")
                    for item in pm.get("this_quarter", []):
                        st.markdown(f"- {item}")
                with col3:
                    st.info("🔵 **下阶段**")
                    for item in pm.get("next_phase", []):
                        st.markdown(f"- {item}")

            # ── Export hint ──
            st.markdown("---")
            st.caption("💡 这份报告可以截图或复制到你的面试作品集里。左侧导航栏有 7 个进阶工具，可以对每个维度做更深入的分析。")

        except (json.JSONDecodeError, KeyError) as e:
            st.error("AI 返回格式异常，以下为原始结果：")
            st.code(result)


# ── Route modules ──
def main():
    if module_key == "audit":
        show_audit()
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
