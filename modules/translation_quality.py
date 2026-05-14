"""
模块 1: AI 翻译质量评估
输入源文+译文，AI 从准确度、风格、术语、文化适配多维度评分。
"""

import streamlit as st
from utils.llm_client import ask_deepseek

SYSTEM_PROMPT = """你是一位资深本地化质量评估专家 (LQA)。请根据以下维度评估翻译质量，并给出评分和改进建议：

评分维度（每项 1-10 分）：
1. 准确度 (Accuracy) — 源文信息是否完整、正确地传递
2. 风格与语气 (Style & Tone) — 是否符合作品/产品原文风格特征
3. 术语一致性 (Terminology) — 专业术语翻译是否准确且一致
4. 文化适配 (Cultural Adaptation) — 是否考虑了目标市场的文化习惯
5. 流畅度 (Fluency) — 目标语言读起来是否自然

输出格式（严格按 JSON）：
{
  "scores": { "accuracy": N, "style": N, "terminology": N, "cultural": N, "fluency": N },
  "overall_score": N,
  "strengths": ["1", "2", "3"],
  "issues": [
    {"severity": "critical/major/minor", "description": "问题描述", "suggestion": "改进建议"}
  ],
  "summary": "总体评价（2-3句中文）"
}"""


def run():
    st.subheader("🎯 AI 翻译质量评估")
    st.markdown("粘贴源文和译文，AI 自动从 **准确度、风格、术语、文化适配、流畅度** 五个维度评分，并给出改进建议。")

    col1, col2 = st.columns(2)
    with col1:
        source_text = st.text_area("源文 (Source)", height=200,
                                   placeholder="Paste the original text here...")
    with col2:
        target_text = st.text_area("译文 (Translation)", height=200,
                                   placeholder="Paste the translated text here...")

    if st.button("评估翻译质量", type="primary", use_container_width=True):
        if not source_text or not target_text:
            st.warning("请同时输入源文和译文。")
            return

        with st.spinner("AI 正在评估翻译质量..."):
            user_prompt = f"源文：\n{source_text}\n\n译文：\n{target_text}"
            result = ask_deepseek(SYSTEM_PROMPT, user_prompt)

        try:
            import json
            data = json.loads(result)
            scores = data["scores"]

            # Score display
            cols = st.columns(5)
            labels = {
                "accuracy": "准确度",
                "style": "风格语气",
                "terminology": "术语一致性",
                "cultural": "文化适配",
                "fluency": "流畅度",
            }
            for i, (key, label) in enumerate(labels.items()):
                score = scores.get(key, 0)
                color = "🟢" if score >= 8 else ("🟡" if score >= 5 else "🔴")
                cols[i].metric(f"{color} {label}", f"{score}/10")

            st.markdown(f"### 📊 总分: {data['overall_score']}/50")

            if data.get("strengths"):
                st.markdown("#### ✅ 优点")
                for s in data["strengths"]:
                    st.markdown(f"- {s}")

            if data.get("issues"):
                st.markdown("#### ⚠️ 需要改进的问题")
                for issue in data["issues"]:
                    severity = issue.get("severity", "minor")
                    icon = {"critical": "🚨", "major": "⚠️", "minor": "💡"}.get(severity, "💡")
                    st.markdown(f"{icon} **[{severity.upper()}]** {issue['description']}")
                    st.markdown(f"  → *建议：* {issue.get('suggestion', '')}")

            st.divider()
            st.markdown(f"**总结：** {data.get('summary', '')}")

        except (json.JSONDecodeError, KeyError):
            st.error("AI 返回格式异常，以下为原始结果：")
            st.code(result)
