import os
import yaml
from langsmith import Client

def save_prompt_yaml(prompt, path):
    # Extrai apenas campos essenciais serializáveis
    try:
        data = {}
        # Campos comuns em ChatPromptTemplate
        for attr in ["input_variables", "input_types", "partial_variables", "metadata"]:
            if hasattr(prompt, attr):
                data[attr] = getattr(prompt, attr)
        # Mensagens: extrai template de cada mensagem
        if hasattr(prompt, "messages"):
            data["messages"] = []
            for msg in prompt.messages:
                # Para cada mensagem, extrai tipo e template
                msg_data = {"type": type(msg).__name__}
                if hasattr(msg, "prompt") and hasattr(msg.prompt, "template"):
                    msg_data["template"] = msg.prompt.template
                data["messages"].append(msg_data)
        # Fallback: se nada foi extraído, salva como string
        if not data:
            data = str(prompt)
        print(f"[LOG] Conteúdo serializado a ser salvo:\n{data}")
    except Exception as e:
        print(f"[LOG] Erro ao converter prompt para formato serializável: {e}")
    abs_path = os.path.abspath(path)
    print(f"[LOG] Caminho absoluto do arquivo: {abs_path}")
    try:
        with open(abs_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)
        print(f"[LOG] Arquivo salvo com sucesso em: {abs_path}")
    except Exception as file_err:
        print(f"[LOG] Erro ao salvar arquivo: {file_err}")

def main():
    # Configuração
    prompt_id = input("Digite o identificador do prompt público (ex: leonanluppi/bug_to_user_story_v1): ").strip()
    if not prompt_id:
        print("Identificador não informado.")
        return

    # Diretório de destino
    prompt_dir = os.getenv("PROMPT_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts"))
    print(f"[LOG] Diretório de destino: {prompt_dir}")
    os.makedirs(prompt_dir, exist_ok=True)

    # Inicializa o cliente LangSmith
    client = Client()
    try:
        print("[LOG] Chamando client.pull_prompt...")
        prompt = client.pull_prompt(prompt_id, dangerously_pull_public_prompt=True)
        print(f"[LOG] Resultado do pull: {type(prompt)} | {prompt}")
        if not prompt or not getattr(prompt, 'dict', None) or not prompt.dict():
            print(f"Prompt '{prompt_id}' não encontrado ou está vazio. Nada foi salvo.")
            return
        # Gera nome de arquivo apenas com o nome do prompt (sem caminho anterior a /)
        filename = prompt_id.split("/")[-1] + ".yml"
        filepath = os.path.join(prompt_dir, filename)
        print(f"[LOG] Salvando arquivo em: {filepath}")
        save_prompt_yaml(prompt, filepath)
        print(f"Prompt salvo em: {filepath}")
    except Exception as e:
        print(f"Erro ao baixar o prompt: {e}")

if __name__ == "__main__":
    main()
