"""Script de avaliacao automatica dos prompts com as 5 metricas."""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from utils import load_dataset, load_prompt, invoke_prompt, get_llm, save_results, calculate_average_metrics
from metrics import metric_helpfulness, metric_correctness, metric_f1_score, metric_clarity, metric_precision


def main():
    # Carregar variáveis de ambiente
    project_root = os.path.dirname(os.path.dirname(__file__))
    load_dotenv(os.path.join(project_root, ".env"))
    
    # Configuração
    dataset_path = os.path.join(project_root, "datasets", "bug_to_user_story.jsonl")
    prompt_path = os.path.join(project_root, "prompts", "bug_to_user_story_v2.yml")
    results_dir = os.path.join(project_root, "results")
    
    os.makedirs(results_dir, exist_ok=True)
    
    # Carregar dados e prompt
    print("[INFO] Carregando dataset...")
    dataset = load_dataset(dataset_path)
    print(f"[INFO] {len(dataset)} exemplos de bugs carregados.")
    
    print("[INFO] Carregando prompt...")
    prompt = load_prompt(prompt_path)
    
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    print(f"[INFO] Inicializando LLM (provider={provider})...")
    llm = get_llm(provider=provider)
    
    # Avaliar cada exemplo
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("[INFO] Iniciando avaliacao...\n")

    provider_failures = 0
    
    for idx, example in enumerate(dataset, 1):
        bug_report = example.get("bug_report", "")
        expected_story = example.get("expected_user_story", "")
        
        print(f"[{idx}/{len(dataset)}] Avaliando bug: {bug_report[:60]}...")
        
        # Gerar user story
        try:
            generated_story = invoke_prompt(prompt, llm, bug_report)
        except Exception as e:
            print(f"[ERRO] Falha ao invocar prompt: {e}")
            provider_failures += 1
            generated_story = ""
        
        # Calcular métricas
        try:
            helpfulness = metric_helpfulness(bug_report, generated_story, llm)
            correctness = metric_correctness(bug_report, generated_story, llm)
            f1_score = metric_f1_score(bug_report, generated_story, expected_story)
            clarity = metric_clarity(bug_report, generated_story, llm)
            precision = metric_precision(bug_report, generated_story, expected_story)
        except Exception as e:
            print(f"[ERRO] Falha ao calcular métricas: {e}")
            provider_failures += 1
            helpfulness = correctness = f1_score = clarity = precision = 0.0
        
        result = {
            "index": idx,
            "bug_report": bug_report,
            "generated_story": generated_story,
            "expected_story": expected_story,
            "helpfulness": round(helpfulness, 3),
            "correctness": round(correctness, 3),
            "f1_score": round(f1_score, 3),
            "clarity": round(clarity, 3),
            "precision": round(precision, 3)
        }
        results.append(result)
        
        # Exibir resultado
        print(f"  -> Helpfulness: {helpfulness:.3f}")
        print(f"  -> Correctness: {correctness:.3f}")
        print(f"  -> F1-Score: {f1_score:.3f}")
        print(f"  -> Clarity: {clarity:.3f}")
        print(f"  -> Precision: {precision:.3f}\n")

    if provider_failures > 0:
        raise RuntimeError(
            "Avaliacao interrompida: houve falhas de provedor LLM (API key, quota ou rede). "
            "Corrija credenciais/quota antes de confiar nas metricas."
        )
    
    # Calcular médias
    averages = calculate_average_metrics(results)
    
    # Salvar resultados
    output_filename = f"evaluation_{timestamp}.json"
    output_path = os.path.join(results_dir, output_filename)
    
    summary = {
        "timestamp": timestamp,
        "total_examples": len(dataset),
        "averages": averages,
        "results": results
    }
    
    save_results(summary, output_path)
    
    # Exibir resumo
    print("\n" + "="*60)
    print("RESUMO DA AVALIACAO")
    print("="*60)
    print(f"Total de exemplos: {len(dataset)}")
    print(f"Data/Hora: {timestamp}")
    print("\nMÉTRICAS MÉDIAS:")
    for metric, value in averages.items():
        status = "OK" if value >= 0.9 else "FAIL"
        print(f"  {metric:15}: {value:.3f} {status}")
    
    mean_all = sum(averages.values()) / len(averages) if averages else 0
    print(f"\n  MÉDIA GERAL: {mean_all:.3f}")
    
    # Critério de aceitação
    all_above_090 = all(v >= 0.9 for v in averages.values())
    if all_above_090:
        print("\nAPROVADO: Todas as metricas >= 0.9")
    else:
        below_090 = [k for k, v in averages.items() if v < 0.9]
        print(f"\nNAO APROVADO: Metricas abaixo de 0.9: {', '.join(below_090)}")
    
    print(f"\nResultados salvos em: {output_path}")
    print("="*60)


if __name__ == "__main__":
    main()
