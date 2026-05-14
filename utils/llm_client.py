"""
DeepSeek LLM client — OpenAI-compatible wrapper.
"""

import os
from openai import OpenAI

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def get_client() -> OpenAI:
    """Get DeepSeek API client."""
    api_key = DEEPSEEK_API_KEY
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
        except Exception:
            pass
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY not found. Set it as an environment variable "
            "or in .streamlit/secrets.toml"
        )
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def ask_deepseek(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 2048,
) -> str:
    """Call DeepSeek Chat with system + user prompts."""
    client = get_client()
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content or ""
