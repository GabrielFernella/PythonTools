from pathlib import Path
from typing import Dict, List, Tuple

"""
Esse servico compara um arquivo base e uma lista de arquivos cujo preciso consultar as variaveis de ambiente que estejam no formato KEY=VALUE
"""

def load_env_file(file_path: str) -> Dict[str, str]:
    """
    Carrega um arquivo de configuração no formato KEY=VALUE.
    
    Args:
        file_path (str): Caminho do arquivo
        
    Returns:
        Dict[str, str]: Dicionário com as variáveis e seus valores
    """
    variables = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                # Ignora linhas vazias ou comentários
                if line and not line.startswith('#'):
                    # Divide no primeiro '=' encontrado
                    if '=' in line:
                        key, value = line.split('=', 1)
                        variables[key.strip()] = value.strip()
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {str(e)}")
    return variables

def compare_env_files(base_file: str, files_to_compare: List[str]) -> None:
    """
    Compara um arquivo base com outros arquivos de configuração.
    
    Args:
        base_file (str): Caminho do arquivo base
        files_to_compare (List[str]): Lista de arquivos para comparar
    """
    # Carrega o arquivo base
    base_vars = load_env_file(base_file)
    if not base_vars:
        print("Erro: Arquivo base está vazio ou não pôde ser lido")
        return

    print(f"Arquivo base: {base_file}")
    print(f"Total de variáveis no arquivo base: {len(base_vars)}\n")

    # Para cada arquivo na lista
    for file_path in files_to_compare:
        print(f"\nAnalisando arquivo: {file_path}")
        print("-" * 50)

        # Carrega o arquivo para comparação
        compare_vars = load_env_file(file_path)
        if not compare_vars:
            print("Erro: Arquivo não pôde ser lido")
            continue

        # Variáveis para o relatório
        missing_vars = []
        different_values = []
        extra_vars = []

        # Verifica variáveis ausentes ou com valores diferentes
        for key, base_value in base_vars.items():
            if key not in compare_vars:
                missing_vars.append(key)
            elif compare_vars[key] != base_value:
                different_values.append((key, base_value, compare_vars[key]))

        # Verifica variáveis extras
        for key in compare_vars:
            if key not in base_vars:
                extra_vars.append(key)

        # Gera o relatório
        print("\nRelatório de diferenças:")
        if not (missing_vars or different_values or extra_vars):
            print("✓ Arquivo está idêntico ao arquivo base")
        else:
            if missing_vars:
                print("\nVariáveis ausentes:")
                for var in missing_vars:
                    print(f"  - {var} (valor esperado: {base_vars[var]})")

            if different_values:
                print("\nValores diferentes:")
                for var, base_val, current_val in different_values:
                    print(f"  - {var}:")
                    print(f"    Base: {base_val}")
                    print(f"    Atual: {current_val}")

            if extra_vars:
                print("\nVariáveis extras:")
                for var in extra_vars:
                    print(f"  - {var}={compare_vars[var]}")

        # Resumo
        print(f"\nResumo:")
        print(f"  Total de variáveis no arquivo base: {len(base_vars)}")
        print(f"  Total de variáveis neste arquivo: {len(compare_vars)}")
        print(f"  Variáveis ausentes: {len(missing_vars)}")
        print(f"  Valores diferentes: {len(different_values)}")
        print(f"  Variáveis extras: {len(extra_vars)}")

# Exemplo de uso
if __name__ == "__main__":
    # Arquivo base de referência
    base_file = "./dev.conf"
    
    # Lista de arquivos para comparar
    files_to_compare = [
        "./prod.conf",
    ]
    
    compare_env_files(base_file, files_to_compare)