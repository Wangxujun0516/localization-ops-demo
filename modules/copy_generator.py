"""
模块 4: AI 双语产品文案生成
生成英文产品文案，同时附带中文本地化备注。
"""

import streamlit as st
from utils.llm_client import ask_deepseek

CONTENT_TYPES = [
    "产品发布公告 (Product Launch)",
    "功能更新说明 (Release Notes)",
    "新用户引导文案 (Onboarding Copy)",
    "营销落地页文案 (Landing Page Copy)",
    "产品帮助中心说明 (Help Center Article)",
    "App Store / Google Play 描述",
    "社交媒体推广文案 (Social Media Post)",
]

TONE_OPTIONS = ["专业正式 (Professional)", "亲切友好 (Friendly)", "简洁直接 (Concise)", "热情鼓励 (Enthusiastic)"]


SYSTEM_PROMPT = """你是一位双语产品文案专家。根据用户输入的产品信息和文案类型，生成英文文案同时附带中文备注。

格式要求：
- 英文文案是最终的、可直接使用的产品文案
- 中文备注放在【】内，说明翻译时的注意事项、文化适配建议、术语统一建议等

输出格式（严格 JSON）：
{
  "english_copy": "生成的英文文案全文",
  "localization_notes": [
    {"note_type": "术语/格式/文化/风格", "note": "中文说明，比如：'此处xx术语建议统一为xx'，或'英文使用了简洁风格，中文版可适当扩展'"}
  ],
  "seo_keywords": ["keyword1", "keyword2"],
  "character_count": N,
  "readability_level": "grade level (e.g., Grade 8)"
}"""


def run():
    st.subheader("✍️ AI 双语产品文案生成")
    st.markdown("输入产品信息和文案类型，AI 生成英文文案 + 中文本地化备注，展示跨语言内容运营能力。")

    col1, col2 = st.columns(2)
    with col1:
        content_type = st.selectbox("文案类型", CONTENT_TYPES)
    with col2:
        tone = st.selectbox("语气风格", TONE_OPTIONS)

    product_info = st.text_area("产品信息", height=120,
                                placeholder="描述产品/功能是什么，目标用户是谁，核心卖点是什么...")

    key_points = st.text_area("关键信息（可选）", height=80,
                              placeholder="必须包含的信息点，如：上线时间、价格、核心功能名称等")

    if st.button("生成文案", type="primary", use_container_width=True):
        if not product_info:
            st.warning("请至少填写产品信息。")
            return

        with st.spinner("AI 正在生成双语文案..."):
            user_prompt = f"文案类型：{content_type}\n语气：{tone}\n产品信息：{product_info}\n关键信息：{key_points or '(无额外要求)'}"
            result = ask_deepseek(SYSTEM_PROMPT, user_prompt, temperature=0.7)

        try:
            import json
            data = json.loads(result)

            st.markdown("### 📝 英文文案")
            st.markdown(f"""
            <div style="background:#1E1E2E; padding:20px; border-radius:10px; border-left:4px solid #1E88E5;">
              {data.get('english_copy', '')}
            </div>
            """, unsafe_allow_html=True)

            st.caption(f"字符数: {data.get('character_count', 'N/A')}  |  可读性: {data.get('readability_level', 'N/A')}")

            if data.get("localization_notes"):
                st.markdown("---")
                st.markdown("### 🗺️ 本地化备注")
                for note in data["localization_notes"]:
                    note_type = note.get("note_type", "通用")
                    icon = {"术语": "📖", "格式": "🔤", "文化": "🌍", "风格": "🎨"}.get(note_type, "💡")
                    st.info(f"{icon} **[{note_type}]** {note['note']}")

            if data.get("seo_keywords"):
                st.markdown("---")
                st.markdown("### 🔑 推荐 SEO 关键词")
                st.markdown(" ".join([f"`{kw}`" for kw in data["seo_keywords"]]))

        except (json.JSONDecodeError, KeyError) as e:
            st.error(f"AI 返回格式异常: {e}")
            st.code(result)
