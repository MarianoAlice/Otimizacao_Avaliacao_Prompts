import os
import yaml
from langsmith import Client

def main():
    # Caminho do prompt otimizado
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "bug_to_user_story_v2.yml")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_data = yaml.safe_load(f)

    # Monta o template para push
    system = prompt_data.get("system", "")
    user = prompt_data.get("user", "")
    # Nome do prompt no hub
    username = os.getenv("LANGCHAIN_USERNAME", "seu_username")
    prompt_id = f"{username}/bug_to_user_story_v2"

    # Inicializa o cliente LangSmith
    client = Client()
    # Cria o prompt como ChatPromptTemplate
    from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system),
        HumanMessagePromptTemplate.from_template(user)
    ])
    # Metadados
    tags = ["few-shot", "role-prompting", "chain-of-thought", "edge-cases"]
    description = "Prompt otimizado para transformar relatos de bugs em user stories, com exemplos, persona e raciocínio passo a passo."
    techniques = "Few-shot, Role Prompting, Chain of Thought"
    # Push para o hub
    client.push_prompt(
        prompt_id,
        prompt,
        description=description,
        tags=tags,
        metadata={"techniques": techniques}
    )
    print(f"Prompt publicado como: {prompt_id}")

if __name__ == "__main__":
    main()
