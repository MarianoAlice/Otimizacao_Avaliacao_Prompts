import os
import yaml
from langsmith import Client
from langsmith.utils import LangSmithUserError
from dotenv import load_dotenv

def main():
    project_root = os.path.dirname(os.path.dirname(__file__))
    load_dotenv(os.path.join(project_root, ".env"))

    # Caminho do prompt otimizado
    prompt_path = os.path.join(project_root, "prompts", "bug_to_user_story_v2.yml")
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_data = yaml.safe_load(f)

    # Monta o template para push
    system = prompt_data.get("system", "")
    user = prompt_data.get("user", "")
    # Nome do prompt no hub
    username = os.getenv("LANGCHAIN_USERNAME", "").strip()

    if not (os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")):
        raise ValueError("Defina LANGSMITH_API_KEY (ou LANGCHAIN_API_KEY) no .env antes do push.")

    # Se username estiver ausente ou em formato de e-mail, publica no tenant autenticado.
    if (not username) or ("@" in username) or (" " in username):
        prompt_id = "bug_to_user_story_v2"
    else:
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
    # Push para o hub. Se ainda não houver handle público no Hub,
    # faz fallback para push privado para não bloquear as iterações.
    try:
        client.push_prompt(
            prompt_id,
            object=prompt,
            description=f"{description} | Techniques: {techniques}",
            tags=tags,
            is_public=True,
        )
        print(f"Prompt publicado como PUBLICO: {prompt_id}")
    except (LangSmithUserError, ValueError) as e:
        if "Cannot create a public prompt without first" not in str(e):
            raise
        client.push_prompt(
            prompt_id,
            object=prompt,
            description=f"{description} | Techniques: {techniques}",
            tags=tags,
            is_public=False,
        )
        print(
            "Prompt publicado como PRIVADO (handle público ainda não configurado). "
            "Crie um prompt público manualmente no Hub e rode novamente para publicar público."
        )

if __name__ == "__main__":
    main()
