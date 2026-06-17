import pytest
import yaml
import os
import re

PROMPT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "bug_to_user_story_v2.yml")

def load_prompt():
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def test_prompt_has_system_prompt():
    prompt = load_prompt()
    assert "system" in prompt and prompt["system"].strip() != ""

def test_prompt_has_role_definition():
    prompt = load_prompt()
    system = prompt.get("system", "").lower()
    assert "analista de requisitos" in system or "persona" in system or "você é" in system

def test_prompt_mentions_format():
    prompt = load_prompt()
    system = prompt.get("system", "").lower()
    assert "como [tipo de usuário], quero" in system or "user story" in system

def test_prompt_has_few_shot_examples():
    prompt = load_prompt()
    system = prompt.get("system", "")
    assert "exemplo" in system.lower() or "relato de bug" in system.lower()
    assert "user story gerada" in system.lower()

def test_prompt_no_todos():
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        content = f.read().lower()
    # Busca 'todo' como palavra isolada ou precedida de #, ignorando dentro de outras palavras
    assert not re.search(r"(^|\s|#)todo(\s|$|:)" , content), "Encontrado 'todo' como palavra isolada ou comentário."

def test_minimum_techniques():
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    techniques = []
    for line in lines:
        if "técnicas" in line.lower() or "techniques" in line.lower():
            techniques = [t.strip() for t in line.split(":",1)[-1].split(",")]
    assert len([t for t in techniques if t]) >= 2
