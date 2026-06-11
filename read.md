# Otimizacao_Avaliacao_Prompts

Guia completo para subir e executar o sistema do desafio de otimização e avaliação de prompts, com publicação no LangSmith Hub e avaliações automáticas.

## Escopo do sistema

O fluxo principal está na pasta `otimizacao_avaliacao_prompts/` e cobre:

- Pull de prompt base (`bug_to_user_story_v1`) do Hub.
- Edição/otimização do prompt (`bug_to_user_story_v2.yml`).
- Push do prompt otimizado para o LangSmith Hub.
- Avaliação automática com 5 métricas em dataset JSONL.
- Testes de validação do prompt com `pytest`.

## Estrutura relevante

```
otimizacao_avaliacao_prompts/
├── .env
├── .env.example
├── requirements.txt
├── prompts/
│   ├── bug_to_user_story_v1.yml
│   └── bug_to_user_story_v2.yml
├── datasets/
│   └── bug_to_user_story.jsonl
├── src/
│   ├── pull_prompts.py
│   ├── push_prompts.py
│   ├── evaluate.py
│   ├── metrics.py
│   └── utils.py
└── tests/
    └── test_prompts.py
```

## Pré-requisitos

- Windows PowerShell (comandos abaixo são para Windows).
- Python 3.11+ (recomendado 3.12+).
- Conta e chave de API do Gemini e/ou OpenAI.
- Conta LangSmith com API key.

## Subindo o sistema (passo a passo)

1. Entrar na pasta do projeto:

```powershell
Set-Location "c:\_node_sites\MBA_Engenharia de Software\Otimizacao_Avaliacao_Prompts\otimizacao_avaliacao_prompts"
```

2. Criar e ativar ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependências:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install python-dotenv pyyaml langchain-google-genai
```

4. Configurar `.env` (use `.env.example` como base):

```env
TZ="America/Sao_Paulo"
ambiente="local"
PROMPT_DIR="prompts"

OPENAI_API_KEY=""
GEMINI_API_KEY="SUA_CHAVE_GEMINI"

LANGSMITH_API_KEY="SUA_CHAVE_LANGSMITH"
LANGCHAIN_USERNAME="seu_handle_langsmith"

LLM_PROVIDER="gemini"
GEMINI_MODEL="gemini-flash-lite-latest"
LLM_TEMPERATURE="0"
```

## Execução operacional

### 1) Validar prompt com testes

```powershell
python -m pytest tests/test_prompts.py -v
```

### 2) Pull do prompt base (se necessário)

```powershell
python src/pull_prompts.py
```

### 3) Push do prompt otimizado

```powershell
python src/push_prompts.py
```

Observação:
- Se o handle público do Hub ainda não estiver configurado, o script faz fallback para push privado.
- Para liberar público, crie um prompt público uma vez em `https://smith.langchain.com/prompts`.

### 4) Rodar avaliação automática

```powershell
python -u src/evaluate.py
```

Saída:
- Arquivo JSON em `results/evaluation_YYYYMMDD_HHMMSS.json`.
- Resumo no console com `helpfulness`, `correctness`, `f1_score`, `clarity`, `precision`.

## Critério de aprovação usado no projeto

- Todas as 5 métricas devem ser `>= 0.9`.
- Média geral também deve ser `>= 0.9`.

## Troubleshooting rápido

1. Erro de cota/quota (`429 RESOURCE_EXHAUSTED` ou `insufficient_quota`):
- Verificar billing e cotas do provedor.
- Trocar modelo (`GEMINI_MODEL`) e manter `LLM_TEMPERATURE=0`.

2. Erro de modelo indisponível (`404 NOT_FOUND`):
- Atualizar `GEMINI_MODEL` para um modelo válido na conta.

3. Push com erro de handle público:
- Mensagem comum: `Cannot create a public prompt without first creating a LangChain Hub handle`.
- Solução: criar handle/prompt público no Hub e repetir o push.

4. Execução inconsistente:
- Confirmar ambiente virtual ativo.
- Reinstalar dependências do `requirements.txt`.

## Técnicas de prompt aplicadas

- Few-shot Learning.
- Role Prompting.
- Chain of Thought (CoT).

Essas técnicas estão implementadas no arquivo `prompts/bug_to_user_story_v2.yml`.
