from langchain_community.llms import Ollama
import streamlit as st

@st.cache_resource(show_spinner=False)
def load_llm(model: str = "deepseek-r1"):
    """Load LLM with caching"""
    return Ollama(model=model)

def clean_llm_response(response: str) -> str:
    """Clean and format LLM response"""
    if "<think>" in response:
        response = response.split("</think>")[-1].strip()
    return response.replace("**", "").replace("```", "")