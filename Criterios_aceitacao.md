# Para que a aplicação seja aceita:

1. Iteração
Espera-se 3-5 iterações.
Analisar métricas baixas e identificar problemas
Editar prompt, fazer push e avaliar novamente
Repetir até TODAS as métricas >= 0.9

Critério de Aprovação:
- Helpfulness >= 0.9
- Correctness >= 0.9
- F1-Score >= 0.9
- Clarity >= 0.9
- Precision >= 0.9

MÉDIA das 5 métricas >= 0.9

IMPORTANTE: TODAS as 5 métricas devem estar >= 0.9, não apenas a média!

2. Testes de Validação
O que você deve fazer: Edite o arquivo tests/test_prompts.py e implemente, no mínimo, os 6 testes abaixo usando pytest:

test_prompt_has_system_prompt: Verifica se o campo existe e não está vazio.
test_prompt_has_role_definition: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
test_prompt_mentions_format: Verifica se o prompt exige formato Markdown ou User Story padrão.
test_prompt_has_few_shot_examples: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
test_prompt_no_todos: Garante que você não esqueceu nenhum [TODO] no texto.
test_minimum_techniques: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.
Como validar:

pytest tests/test_prompts.py

3. Estutura obrigatória:
otimizacao_avaliacao_prompts/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)

4. NÃO DEVE SER ALTERADO:

src/evaluate.py — Script de avaliação completo
src/metrics.py — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
src/utils.py — Funções auxiliares
datasets/bug_to_user_story.jsonl — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
Suporte multi-provider (OpenAI e Gemini)

5. Garantir que:

prompts/bug_to_user_story_v2.yml — Criar do zero com seu prompt otimizado
src/pull_prompts.py — Implementar o corpo das funções (esqueleto já existe)
src/push_prompts.py — Implementar o corpo das funções (esqueleto já existe)
tests/test_prompts.py — Implementar os 6 testes de validação (esqueleto já existe)
README.md — Documentar seu processo de otimização

6. Readme.md com as seguintes seções:

- A. Seção "Técnicas Aplicadas (Fase 2)":
Quais técnicas avançadas você escolheu para refatorar os prompts
Justificativa de por que escolheu cada técnica
Exemplos práticos de como aplicou cada técnica

- B Seção "Resultados Finais":
Link público do seu dashboard do LangSmith mostrando as avaliações
Screenshots das avaliações com as notas mínimas de 0.9 atingidas
Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

- C Seção "Como Executar":
Instruções claras e detalhadas de como executar o projeto
Pré-requisitos e dependências
Comandos para cada fase do projeto


