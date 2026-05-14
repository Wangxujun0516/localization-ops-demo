"""
模块 7: 运营数据看板
模拟国际化产品运营的核心指标展示，使用 Plotly 图表。
不需要调用 LLM，使用模拟数据，适合展示数据意识。
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta


def generate_time_series(days: int = 90):
    """Generate mock daily metrics."""
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    dates.reverse()
    base = 80
    data = {
        "date": dates,
        "coverage_en": [100] * days,
        "coverage_zh": [random.randint(92, 100) for _ in range(days)],
        "coverage_ja": [random.randint(40, 65) for _ in range(days)],
        "coverage_ko": [random.randint(35, 60) for _ in range(days)],
        "coverage_es": [random.randint(45, 70) for _ in range(days)],
        "coverage_ar": [random.randint(20, 45) for _ in range(days)],
        "satisfaction": [min(100, base + i // 20 + random.randint(-5, 5)) for i in range(days)],
        "translation_quality": [random.randint(75, 92) for _ in range(days)],
        "issues_open": [max(0, 15 - i // 15 + random.randint(-3, 3)) for i in range(days)],
        "issues_closed": [max(0, i // 12 + random.randint(-2, 2)) for i in range(days)],
    }
    return pd.DataFrame(data)


LANGUAGES = {
    "zh": "中文", "ja": "日文", "ko": "韩文",
    "es": "西班牙文", "ar": "阿拉伯文", "pt": "葡萄牙文",
}


def run():
    st.subheader("📊 国际化产品运营数据看板")
    st.markdown("模拟一个国际化产品的运营数据看板，展示多语言覆盖、质量分、用户满意度等核心指标。")

    df = generate_time_series()

    # KPI cards
    latest = df.iloc[-1]
    prev = df.iloc[-8]  # ~1 week ago
    col1, col2, col3, col4 = st.columns(4)

    sat_delta = round(latest["satisfaction"] - prev["satisfaction"], 1)
    col1.metric("用户满意度", f"{latest['satisfaction']:.1f}%", f"{sat_delta:+.1f}pp")

    q_delta = round(latest["translation_quality"] - prev["translation_quality"], 1)
    col2.metric("翻译质量均分", f"{latest['translation_quality']:.1f}/100", f"{q_delta:+.1f}")

    issues_total = int(latest["issues_open"] + latest["issues_closed"])
    col3.metric("待处理问题", int(latest["issues_open"]), f"共{issues_total}个")

    avg_coverage = round((latest["coverage_zh"] + latest["coverage_ja"] + latest["coverage_ko"] +
                          latest["coverage_es"] + latest["coverage_ar"]) / 5, 1)
    col4.metric("语言平均覆盖", f"{avg_coverage}%", f"EN: 100%")

    st.divider()

    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs(["📈 满意度趋势", "🌐 语言覆盖", "🎯 翻译质量", "📋 问题追踪"])

    with tab1:
        fig = px.line(df, x="date", y="satisfaction", title="用户满意度趋势（90天）")
        fig.update_traces(line_color="#1E88E5", line_width=3)
        fig.update_layout(
            yaxis_title="满意度 (%)", xaxis_title="",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        fig.add_hline(y=78, line_dash="dash", line_color="orange",
                      annotation_text="改进前基线 (78%)")
        fig.add_hline(y=84.3, line_dash="dash", line_color="green",
                      annotation_text="当前 (84.3%)")
        st.plotly_chart(fig, use_container_width=True)

        st.info("💡 **产品运营解读**: 满意度从78%提升至84.3%，反映了文档架构改版和内容质量提升的成效。下一阶段目标：突破88%——需要重点解决日文和阿拉伯文用户反馈的问题。")

    with tab2:
        fig = go.Figure()
        for lang_code, lang_name in LANGUAGES.items():
            col_name = f"coverage_{lang_code}"
            if col_name in df.columns:
                fig.add_trace(go.Scatter(
                    x=df["date"], y=df[col_name],
                    mode="lines", name=lang_name,
                    line=dict(width=2),
                ))
        fig.update_layout(
            title="各语言内容覆盖率（90天）",
            yaxis_title="覆盖率 (%)", xaxis_title="",
            yaxis_range=[0, 110],
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info("💡 **产品运营解读**: 英文覆盖率100%，中文 >92%。日文和韩文覆盖率在40-65%之间，阿拉伯文最低（20-45%）。短期优先提升日文覆盖率至80%+，中长期攻克阿拉伯文。")

        # Language coverage table
        st.markdown("#### 当前各语言覆盖状态")
        latest_coverage = {k: v for k, v in latest.items() if k.startswith("coverage_")}
        lang_data = []
        for code, name in LANGUAGES.items():
            val = latest_coverage.get(f"coverage_{code}", 0)
            status = "🟢 完整" if val >= 95 else ("🟡 良好" if val >= 60 else ("🟠 待提升" if val >= 30 else "🔴 不足"))
            lang_data.append({"语言": name, "覆盖率": f"{val}%", "状态": status})
        st.dataframe(pd.DataFrame(lang_data), use_container_width=True, hide_index=True)

    with tab3:
        fig = px.line(df, x="date", y="translation_quality", title="翻译质量评分趋势（90天）")
        fig.update_traces(line_color="#7C4DFF", line_width=3)
        fig.update_layout(
            yaxis_title="质量分 (/100)", xaxis_title="",
            yaxis_range=[60, 100],
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 本周质量评分明细")
        quality_data = {
            "维度": ["术语准确度", "语法正确性", "风格一致性", "文化适配", "格式合规"],
            "评分": [88, 85, 82, 76, 91],
            "目标": [90, 88, 85, 80, 95],
        }
        qdf = pd.DataFrame(quality_data)
        st.dataframe(qdf, use_container_width=True, hide_index=True)

    with tab4:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["issues_open"],
            mode="lines", name="待处理",
            line=dict(color="#FF5252", width=2),
        ))
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["issues_closed"],
            mode="lines", name="已关闭",
            line=dict(color="#69F0AE", width=2),
        ))
        fig.update_layout(
            title="本地化问题追踪（90天）",
            yaxis_title="问题数", xaxis_title="",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 待处理问题 TOP 3")
        st.warning("1. [P0] 阿拉伯文 RTL 支持 — UI 在切换阿拉伯语时布局错乱 (影响市场: MENA)")
        st.warning("2. [P1] 日文翻译术语不一致 — 'Workflow' 在3个页面有3种不同译法 (影响市场: JP)")
        st.info("3. [P2] 葡萄牙文巴西变体 — 目前与葡萄牙共用翻译，部分用词在巴西不适用 (影响市场: BR)")
