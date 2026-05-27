# O que deve ser entregue:

1. Faz pull do seguinte prompt: leonanluppi/bug_to_user_story_v1

2. Salva o prompt localmente em prompts/bug_to_user_story_v1.yml

3. Otimização do Prompt
Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

Tarefas:

Analisar o prompt em prompts/bug_to_user_story_v1.yml
Criar um novo arquivo prompts/bug_to_user_story_v2.yml com suas versões otimizadas
Aplicar obrigatoriamente Few-shot Learning (exemplos claros de entrada/saída) e pelo menos uma das seguintes técnicas adicionais:
Chain of Thought (CoT): Instruir o modelo a "pensar passo a passo"
Tree of Thought: Explorar múltiplos caminhos de raciocínio
Skeleton of Thought: Estruturar a resposta em etapas claras
ReAct: Raciocínio + Ação para tarefas complexas
Role Prompting: Definir persona e contexto detalhado
Documentar no README.md quais técnicas você escolheu e por quê
Requisitos do prompt otimizado:

Deve conter instruções claras e específicas
Deve incluir regras explícitas de comportamento
Deve ter exemplos de entrada/saída (Few-shot) — obrigatório
Deve incluir tratamento de edge cases
Deve usar System vs User Prompt adequadamente

4. Push e Avaliação
Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

Tarefas:

Implementar o script src/push_prompts.py (esqueleto já existe) que:
Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
Faz push para o LangSmith com nomes versionados: {seu_username}/bug_to_user_story_v2
Adiciona metadados (tags, descrição, técnicas utilizadas)
Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
Deixá-lo público