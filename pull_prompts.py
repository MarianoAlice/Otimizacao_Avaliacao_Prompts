import os
from dotenv import load_dotenv
import yaml
from langchain.prompts import PromptHub


# Carrega variáveis do arquivo .env
load_dotenv()

# Configure sua chave de API do LangSmith
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

if not LANGCHAIN_API_KEY:
    raise ValueError("Defina a variável de ambiente LANGCHAIN_API_KEY com sua chave do LangSmith.")

# Inicializa o PromptHub
hub = PromptHub(api_key=LANGCHAIN_API_KEY)

# Diretório para salvar os prompts
PROMPT_DIR = os.getenv("PROMPT_DIR")
os.makedirs(PROMPT_DIR, exist_ok=True)

def save_prompt_yaml(prompt, path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(prompt, f, allow_unicode=True)

def main():
    print("Escolha o tipo de prompt que deseja baixar:")
    print("1. Meu prompt privado")
    print("2. Prompt público (ex: hwchase17/openai-functions-agent)")
    tipo = input("Digite 1 ou 2: ").strip()

    if tipo == "2":
        prompt_identifier = input("Digite o identificador do prompt público: ").strip()
        if not prompt_identifier:
            print("Identificador não informado.")
            return
        try:
            prompt = hub.pull(prompt_identifier)
            filename = prompt_identifier.replace('/', '__') + ".yaml"
            filepath = os.path.join(PROMPT_DIR, filename)
            save_prompt_yaml(prompt.dict(), filepath)
            print(f"Prompt salvo em: {filepath}")
        except Exception as e:
            print(f"Erro ao baixar o prompt: {e}")
        return

    elif tipo == "1":
        prompts = hub.list()
        if not prompts:
            print("Nenhum prompt encontrado no PromptHub.")
            return

        print("Prompts disponíveis:")
        for idx, prompt_id in enumerate(prompts, 1):
            print(f"{idx}. {prompt_id}")

        escolha = input("Digite o número do prompt que deseja baixar: ")
        try:
            escolha_idx = int(escolha) - 1
            if escolha_idx < 0 or escolha_idx >= len(prompts):
                print("Escolha inválida.")
                return
        except ValueError:
            print("Entrada inválida.")
            return

        prompt_id = list(prompts)[escolha_idx]
        prompt = hub.pull(prompt_id)
        filename = f"{prompt_id}.yaml"
        filepath = os.path.join(PROMPT_DIR, filename)
        save_prompt_yaml(prompt.dict(), filepath)
        print(f"Prompt salvo em: {filepath}")
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
