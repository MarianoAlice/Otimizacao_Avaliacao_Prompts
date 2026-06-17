"""Funções auxiliares para o pipeline de avaliação."""

import json
import yaml
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


def normalize_llm_content(content) -> str:
    """Normaliza conteúdo de resposta do LLM para string simples."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                txt = item.get("text") or item.get("content") or ""
                if txt:
                    parts.append(str(txt))
            elif isinstance(item, str):
                parts.append(item)
            else:
                txt = getattr(item, "text", "")
                if txt:
                    parts.append(str(txt))
        return " ".join(parts).strip()
    return str(content).strip()


def load_dataset(dataset_path: str) -> list:
    """Carrega dataset JSONL com bugs e user stories esperadas."""
    data = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def load_prompt(prompt_path: str) -> ChatPromptTemplate:
    """Carrega prompt YAML e retorna ChatPromptTemplate."""
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_data = yaml.safe_load(f)
    
    system_template = prompt_data.get("system", "")
    user_template = prompt_data.get("user", "{bug_report}")
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(user_template)
    ])
    return prompt


def invoke_prompt(prompt: ChatPromptTemplate, llm: ChatOpenAI, bug_report: str) -> str:
    """Invoca o prompt com um bug report e retorna a user story gerada."""
    chain = prompt | llm
    response = chain.invoke({"bug_report": bug_report})
    return normalize_llm_content(getattr(response, "content", response))


def get_llm(provider: str = "openai") -> ChatOpenAI:
    """Retorna instância do LLM conforme provider."""
    temperature = float(os.getenv("LLM_TEMPERATURE", "0"))

    if provider == "openai":
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=temperature)
    elif provider == "gemini":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except Exception as e:
            raise ImportError(
                "Pacote langchain-google-genai não instalado. Rode: pip install langchain-google-genai"
            ) from e

        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
            temperature=temperature,
            google_api_key=os.getenv("GEMINI_API_KEY", ""),
        )
    else:
        raise ValueError(f"Provider '{provider}' não reconhecido. Use 'openai' ou 'gemini'.")


def save_results(results: list, output_path: str):
    """Salva resultados de avaliação em JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def calculate_average_metrics(results: list) -> dict:
    """Calcula média das 5 métricas a partir dos resultados."""
    if not results:
        return {}
    
    metrics_sum = {
        "helpfulness": 0.0,
        "correctness": 0.0,
        "f1_score": 0.0,
        "clarity": 0.0,
        "precision": 0.0
    }
    
    for result in results:
        for metric in metrics_sum.keys():
            metrics_sum[metric] += result.get(metric, 0.0)
    
    count = len(results)
    averages = {k: v / count for k, v in metrics_sum.items()}
    
    return averages
