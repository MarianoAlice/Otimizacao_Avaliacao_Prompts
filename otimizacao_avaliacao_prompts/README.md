# Otimização e Avaliação de Prompts

## Técnicas Aplicadas (Fase 2)

Nesta fase, apliquei três técnicas principais: Few-shot Learning, Role Prompting e Chain of Thought (CoT). O Few-shot foi usado para reduzir ambiguidade de saída e aumentar consistência de formato, com exemplos explícitos de "Relato de Bug" e "User Story gerada" (por exemplo, casos de logout, permissões de perfil, desconto com casas decimais e link com erro 404), o que ajudou o modelo a reproduzir padrões próximos do esperado no dataset. O Role Prompting foi aplicado ao definir a persona "analista de requisitos experiente", garantindo contexto profissional e foco em escrita acionável para desenvolvimento. Já o CoT foi implementado por meio de etapas numeradas no System Prompt (leitura do bug, identificação de comportamento esperado/observado, extração de contexto e geração da user story), o que melhorou a qualidade do raciocínio antes da resposta final e aumentou a estabilidade das avaliações ao longo das iterações.

## Resultados Finais

Link do Hub (handle): https://smith.langchain.com/hub/alicemariano/bug_to_user_story_v2

Resumo da execução final aprovada (arquivo: `results/evaluation_20260611_194631.json`):

- Total de exemplos: 15
- Data/Hora: 20260611_194631

Métricas médias:

| Métrica | Valor | Status |
|---|---:|:---:|
| Helpfulness | 0.913 | OK |
| Correctness | 0.933 | OK |
| F1-Score | 0.956 | OK |
| Clarity | 0.927 | OK |
| Precision | 0.968 | OK |

- Média geral: 0.940
- Resultado: APROVADO (todas as métricas >= 0.9)