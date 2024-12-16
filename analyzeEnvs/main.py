import os
import re
import yaml
import sys

# install package
## pip install pyyaml

def extract_env_variables(config):
    """
    Extrai variáveis de ambiente de um dicionário de configuração.
    """
    env_vars = []

    def search_env_vars(data, current_path=''):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{current_path}.{key}" if current_path else key
                search_env_vars(value, new_path)
        elif isinstance(data, str):
            # Regex para encontrar variáveis de ambiente no formato ${VAR_NAME} ou ${VAR_NAME:default_value}
            matches = re.findall(r'\${([A-Z0-9_]+)(?::([^}]+))?}', data)
            for match in matches:
                var_name, default_value = match
                env_vars.append({
                    'name': var_name,
                    'path': current_path,
                    'default_value': default_value if default_value else None
                })
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = f"{current_path}[{idx}]"
                search_env_vars(item, new_path)

    search_env_vars(config)
    return list({v['name']: v for v in env_vars}.values())

def load_yaml_config(file_path):
    """
    Carrega configurações de um arquivo YAML.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return None
    except yaml.YAMLError as e:
        print(f"Erro ao processar o arquivo YAML {file_path}: {e}")
        return None

def verify_env_variables(env_vars, env_files):
    """
    Verifica a existência de variáveis de ambiente em arquivos de configuração.
        env_vars (list): Lista de variáveis de ambiente
        env_files (list): Lista de caminhos para arquivos de ambiente
    """
    verification_report = {
        'total_env_files': len(env_files),
        'files_processed': 0,
        'variables_report': {}
    }

    # Relatório com todas as variáveis
    for var in env_vars:
        verification_report['variables_report'][var['name']] = {
            'original_path': var['path'],
            'default_value': var.get('default_value'),
            'found_in_files': []
        }

    # Verifica cada arquivo de ambiente
    for env_file in env_files:
        env_config = load_yaml_config(env_file)
        
        if env_config is None:
            continue
        
        verification_report['files_processed'] += 1

        # Converte env_config para string para busca de variáveis
        env_config_str = str(env_config)

        for var_name in verification_report['variables_report'].keys():
            if var_name in env_config_str:
                verification_report['variables_report'][var_name]['found_in_files'].append(env_file)

    return verification_report

def print_verification_report(report):
    """
    Imprime relatório de verificação de variáveis.
    """
    print("\n=== Relatório de Verificação de Variáveis de Ambiente ===")
    print(f"Total de arquivos de ambiente: {report['total_env_files']}")
    print(f"Arquivos processados: {report['files_processed']}\n")

    print("Detalhamento das Variáveis:")
    
    # Contadores
    total_vars = len(report['variables_report'])
    found_vars = 0
    not_found_vars = 0

    for var_name, var_info in report['variables_report'].items():
        print(f"\nVariável: {var_name}")
        print(f"  Caminho original: {var_info['original_path']}")
        
        # Adiciona informação de valor padrão, se existir
        if var_info['default_value']:
            print(f"  Valor padrão: {var_info['default_value']}")
        
        if var_info['found_in_files']:
            print(f"  Status: Encontrada em {len(var_info['found_in_files'])} arquivo(s)")
            for file in var_info['found_in_files']:
                print(f"    - {file}")
            found_vars += 1
        else:
            print("  Status: ❌ Não encontrada em nenhum arquivo de ambiente")
            not_found_vars += 1

    # Resumo final
    print("\n=== Resumo ===")
    print(f"Total de variáveis: {total_vars}")
    print(f"Variáveis encontradas: {found_vars}")
    print(f"Variáveis não encontradas: {not_found_vars}")

def main():
    # Configuração dos caminhos dos arquivos
    APPLICATION_YML_PATH = './application.yml'
    ENVIRONMENT_FILES = [
        './dev.conf',
        './prod.conf'
    ]

    # Carrega o arquivo de aplicação
    application_config = load_yaml_config(APPLICATION_YML_PATH)
    
    if application_config is None:
        sys.exit(1)
    
    # Extrai variáveis de ambiente
    env_vars = extract_env_variables(application_config)
    
    print("Variáveis de Ambiente Encontradas:")
    for var in env_vars:
        output = f"- {var['name']} (em: {var['path']})"
        if var.get('default_value'):
            output += f" | Valor Padrão: {var['default_value']}"
        print(output)
    
    # Verifica a existência das variáveis nos arquivos de ambiente
    verification_report = verify_env_variables(env_vars, ENVIRONMENT_FILES)
    
    # Imprime o relatório
    print_verification_report(verification_report)

if __name__ == "__main__":
    main()