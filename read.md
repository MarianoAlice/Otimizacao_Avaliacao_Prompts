# Otimizacao_Avaliacao_Prompts

Este projeto automatiza o download e o salvamento de prompts do LangChain PromptHub em arquivos YAML, facilitando a organização e o versionamento de prompts para aplicações de IA.

## Funcionalidade
- Carrega variáveis de ambiente do arquivo `.env` (utilizando `python-dotenv`).
- Utiliza a chave `LANGCHAIN_API_KEY` para autenticação com o LangChain PromptHub.
- Baixa todos os prompts disponíveis na sua conta PromptHub.
- Salva cada prompt como um arquivo YAML no diretório `prompts/`.

## Como usar

1. **Clone o repositório**

2. **Criar ambiente virtual (recomendado):**
    ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   python -m pip install --upgrade pip
   pip install langchain python-dotenv pyyaml
   ```

4. **Configure o arquivo `.env`:**
   Crie (ou edite) o arquivo `.env` na raiz do projeto e adicione sua chave:
   ```env
   LANGCHAIN_API_KEY=coloque_sua_chave_aqui
   TZ="America/Sao_Paulo"
   ambiente="local"
   ```

5. **Execute o script:**
   ```bash
   python pull_prompts.py
   ```

6. **Resultado:**
   Os prompts serão salvos como arquivos YAML no diretório `prompts/`.

## Estrutura dos arquivos
- `pull_prompts.py`: Script principal para baixar e salvar os prompts.
- `prompts/`: Diretório onde os arquivos YAML dos prompts são salvos.
- `.env`: Arquivo de variáveis de ambiente.

## Observações
- Certifique-se de que sua chave de API do LangChain está correta.
- O script irá criar o diretório `prompts/` automaticamente, se não existir.

## Otimização de Prompt: bug_to_user_story_v2

O prompt `bug_to_user_story_v2.yml` foi otimizado utilizando as seguintes técnicas:

- **Few-shot Learning:** Inclui exemplos claros de entrada (relato de bug) e saída (user story gerada), cobrindo casos comuns e edge cases.
- **Role Prompting:** Define a persona do modelo como um analista de requisitos experiente, especialista em transformar relatos de bugs em user stories acionáveis.
- **Chain of Thought (CoT):** Instruções explícitas para pensar passo a passo: analisar o relato, identificar comportamentos, extrair contexto e só então gerar a user story.
- **Regras explícitas:** O prompt detalha o formato da resposta, como tratar relatos vagos, como pedir esclarecimentos e como lidar com casos não reproduzíveis.
- **Edge cases:** Exemplos e instruções para lidar com relatos incompletos ou pouco claros.

### Exemplo de uso

Entrada (relato de bug):
```
Quando clico no botão 'Enviar' no formulário de contato, nada acontece. Não recebo mensagem de confirmação e o formulário não é enviado, mesmo preenchendo todos os campos corretamente.
```

Saída esperada (user story):
```
Como usuário do site, quero que o formulário de contato envie minha mensagem e exiba uma confirmação, para que eu saiba que meu contato foi recebido.
```

Veja o arquivo `prompts/bug_to_user_story_v2.yml` para o prompt completo e exemplos.

---

Qualquer dúvida ou sugestão, fique à vontade para abrir uma issue!
