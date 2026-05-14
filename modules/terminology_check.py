"""
模块 2: 术语一致性检查
用户上传术语表（CSV/JSON）和待审文本，AI 检查术语翻译是否一致。
"""

import streamlit as st
from utils.llm_client import ask_deepseek

SYSTEM_PROMPT = """你是一位本地化术语管理专家。检查下面待审文本中的术语是否与术语表一致。

输出格式（严格 JSON）：
{
  "total_terms_in_use": N,
  "consistent_count": N,
  "inconsistent_terms": [
    {"term": "源文术语", "expected": "术语表规定译文", "found": "文本中实际使用的译文", "location_start": "在文本中的位置（前10个字符）", "suggestion": "更正建议"}
  ],
  "mis_translations": [
    {"term": "术语", "issue": "翻译错误或不准确", "suggestion": "建议修正"}
  ],
  "summary": "总体评价和建议"
}
"""


def run():
    st.subheader("📖 术语一致性检查")
    st.markdown("上传术语表（每行 `源文术语,译文`）和待审文本，AI 帮你检查术语翻译是否一致。")

    tab1, tab2 = st.tabs(["📋 粘贴模式", "📂 文件上传"])

    term_base = ""
    text_to_check = ""

    with tab1:
        term_base = st.text_area("术语表（每行一条：源文术语,译文）", height=150,
                                 placeholder="例如：\n自然语言处理,Natural Language Processing\n机器学习,Machine Learning\n用户增长,User Growth")
        text_to_check = st.text_area("待审文本", height=200,
                                     placeholder="粘贴需要检查术语一致性的文本...")

    with tab2:
        uploaded_terms = st.file_uploader("上传术语表（CSV 或 TXT）", type=["csv", "txt"],
                                          help="CSV 格式：第一列源文术语，第二列译文")
        uploaded_text = st.file_uploader("上传待审文本（TXT）", type=["txt"])
        if uploaded_terms:
            term_base = uploaded_terms.read().decode("utf-8")
        if uploaded_text:
            text_to_check = uploaded_text.read().decode("utf-8")

    if st.button("检查术语一致性", type="primary", use_container_width=True):
        if not term_base or not text_to_check:
            st.warning("请提供术语表和待审文本。")
            return

        with st.spinner("AI 正在分析术语一致性..."):
            user_prompt = f"术语表：\n{term_base}\n\n待审文本：\n{text_to_check}"
            result = ask_deepseek(SYSTEM_PROMPT, user_prompt)

        try:
            import json
            data = json.loads(result)

            st.markdown(f"**检查的术语数量：** {data.get('total_terms_in_use', 'N/A')}")
            consistent = data.get("consistent_count", 0)
            total = data.get("total_terms_in_use", 1) or 1
            rate = int(consistent / total * 100)
            st.metric("术语一致性", f"{rate}%", f"{consistent}/{total} 条一致")

            if data.get("inconsistent_terms"):
                st.markdown("#### ❌ 不一致的术语")
                for t in data["inconsistent_terms"]:
                    st.markdown(f"- **{t['term']}**: 应译作 `{t['expected']}`，实际为 `{t['found']}`")
                    st.markdown(f"  → *建议：* {t.get('suggestion', '')}")

            if data.get("mis_translations"):
                st.markdown("#### ⚠️ 翻译不准确")
                for t in data["mis_translations"]:
                    st.markdown(f"- **{t['term']}**: {t['issue']}")
                    st.markdown(f"  → *建议：* {t.get('suggestion', '')}")

            st.divider()
            st.markdown(f"**总结：** {data.get('summary', '')}")

        except (json.JSONDecodeError, KeyError) as e:
            st.error(f"AI 返回格式异常: {e}")
            st.code(result)
