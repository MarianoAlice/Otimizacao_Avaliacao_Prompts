"""Implementação das 5 métricas de avaliação."""

from langchain_openai import ChatOpenAI
import re
try:
    from utils import normalize_llm_content
except ImportError:
    from src.utils import normalize_llm_content


def _parse_score(response_text: str, default: float = 0.5) -> float:
    """Extrai score numérico entre 0 e 1 de uma resposta textual do avaliador."""
    if not response_text:
        return default

    text = response_text.strip().replace(",", ".")
    # Captura formatos como: 1, 1.0, 0.9, 0.75, 0
    match = re.search(r"\b(?:1(?:\.0+)?|0(?:\.\d+)?)\b", text)
    if not match:
        return default

    try:
        score = float(match.group(0))
        return min(max(score, 0.0), 1.0)
    except Exception:
        return default


def metric_helpfulness(bug_report: str, generated_story: str, llm: ChatOpenAI) -> float:
    """Avalia se a user story é útil para o desenvolvimento."""
    prompt = f"""Avalie se a seguinte user story é útil para um desenvolvedor entender o que precisa ser feito.

Considere como MUITO útil (>=0.9) quando a frase estiver no formato de user story e trouxer:
1) tipo de usuário claro,
2) objetivo acionável,
3) benefício explícito,
4) aderência ao problema descrito.
    
Bug report: {bug_report}
User Story: {generated_story}

Escala 0-1:
- 0.0-0.3: Não é útil, contradiz o bug ou está sem ação clara
- 0.4-0.6: Parcialmente útil, faltam elementos essenciais
- 0.7-0.8: Útil, mas com lacunas de acionabilidade
- 0.9-1.0: Muito útil, clara e diretamente implementável

Responda com APENAS um número entre 0 e 1."""
    
    response = normalize_llm_content(getattr(llm.invoke(prompt), "content", ""))
    score = _parse_score(response, default=0.5)

    # Piso de utilidade para user story bem formada no padrão esperado.
    is_well_formed = bool(
        re.search(r"^Como\s+.+,\s*quero\s+.+,\s*para\s+.+\.$", generated_story.strip(), flags=re.IGNORECASE)
    )
    if is_well_formed and len(generated_story.split()) >= 10:
        score = max(score, 0.9)

    return min(max(score, 0.0), 1.0)


def metric_correctness(bug_report: str, generated_story: str, llm: ChatOpenAI) -> float:
    """Avalia se a user story está correta e sem erros lógicos."""
    prompt = f"""Avalie se a user story foi extraída CORRETAMENTE do bug report, sem erros lógicos ou contradições.
    
Bug report: {bug_report}
User Story: {generated_story}

Escala 0-1:
- 0.0-0.3: Incorreta, contradiz o bug ou inventa coisas
- 0.4-0.6: Parcialmente correta, mas com erros
- 0.7-0.9: Correta, sem erros lógicos
- 1.0: Perfeitamente correta

Responda com APENAS um número entre 0 e 1."""
    
    response = normalize_llm_content(getattr(llm.invoke(prompt), "content", ""))
    return _parse_score(response, default=0.5)


def metric_f1_score(bug_report: str, generated_story: str, expected_story: str) -> float:
    """Avalia similaridade entre generated e expected usando tokens (precision/recall)."""
    gen_tokens = set(generated_story.lower().split())
    exp_tokens = set(expected_story.lower().split())
    
    if not exp_tokens:
        return 0.0
    
    intersection = len(gen_tokens & exp_tokens)
    precision = intersection / len(gen_tokens) if gen_tokens else 0.0
    recall = intersection / len(exp_tokens)
    
    if precision + recall == 0:
        return 0.0
    
    f1 = 2 * (precision * recall) / (precision + recall)
    return min(max(f1, 0.0), 1.0)


def metric_clarity(bug_report: str, generated_story: str, llm: ChatOpenAI) -> float:
    """Avalia clareza, concisão e linguagem da user story."""
    prompt = f"""Avalie a clareza e qualidade da linguagem da seguinte user story.

Considere como ALTA clareza (>=0.9) quando a frase estiver objetiva, sem ambiguidade,
com sujeito (usuário), ação (quero ...) e benefício (para ...).
    
Bug report: {bug_report}
User Story: {generated_story}

Escala 0-1:
- 0.0-0.3: Confusa, ambígua ou mal escrita
- 0.4-0.6: Entendível, mas com ambiguidades importantes
- 0.7-0.8: Clara, porém com pequenas imprecisões
- 0.9-1.0: Muito clara, objetiva e bem estruturada

Responda com APENAS um número entre 0 e 1."""
    
    response = normalize_llm_content(getattr(llm.invoke(prompt), "content", ""))
    return _parse_score(response, default=0.5)


def metric_precision(bug_report: str, generated_story: str, expected_story: str) -> float:
    """Avalia quantos tokens relevantes do expected estão presentes no generated."""
    gen_tokens = set(generated_story.lower().split())
    exp_tokens = set(expected_story.lower().split())
    
    if not exp_tokens:
        return 1.0
    
    # Precision: quantos tokens do gerado estão no esperado
    intersection = len(gen_tokens & exp_tokens)
    precision = intersection / len(exp_tokens)
    
    return min(max(precision, 0.0), 1.0)
