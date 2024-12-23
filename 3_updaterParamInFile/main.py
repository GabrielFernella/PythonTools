"""
Esse projeto tem como objetivo substituir uma parte de um arquivo de texto, nesse caso, vamos flegar o 
start string e o end string que vai determinar a parte onde vamos substituir o conteudo pelo que iremos passar por parametro
"""

def replace_tag_in_pom_by_bounds(pom_path, start_tag, end_tag, new_content):
    """
    Substitui o conteúdo entre duas tags específicas no pom.xml por um novo valor.

    Args:
        pom_path (str): Caminho para o arquivo pom.xml.
        start_tag (str): Tag inicial (ex.: "<parent>").
        end_tag (str): Tag final (ex.: "</parent>").
        new_content (str): Novo conteúdo para substituir (ex.: "<new>...</new>").

    Returns:
        bool: Retorna True se a substituição foi bem-sucedida, False caso contrário.
    """
    try:
        # Lê o conteúdo do arquivo como texto
        with open(pom_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Localiza as posições das tags
        start_pos = content.find(start_tag)
        end_pos = content.find(end_tag, start_pos)

        if start_pos == -1 or end_pos == -1:
            print(f"❌ As tags '{start_tag}' e/ou '{end_tag}' não foram encontradas no arquivo {pom_path}.")
            return False

        # Inclui o comprimento da tag final para capturar o fechamento
        end_pos += len(end_tag)

        # Substitui o trecho entre as tags pelo novo conteúdo
        updated_content = content[:start_pos] + new_content + content[end_pos:]

        # Salva o conteúdo atualizado no arquivo
        with open(pom_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"✅ Substituição concluída com sucesso no arquivo {pom_path}.")
        return True

    except Exception as e:
        print(f"⚠️ Erro ao processar o arquivo {pom_path}: {e}")
        return False


# Exemplo de uso
if __name__ == "__main__":
    # Caminho relativo para o pom.xml
    pom_file = "./pom.xml"

    # Tags a serem localizadas
    tag_inicial = "<parent>"
    tag_final = "</parent>"

    # Novo conteúdo para substituir
    novo_conteudo = """
    <new>
        <groupId>com.example</groupId>
        <artifactId>novo-projeto</artifactId>
        <version>2.0.0</version>
    </new>
    """

    # Atualiza o pom.xml
    if replace_tag_in_pom_by_bounds(pom_file, tag_inicial, tag_final, novo_conteudo):
        print("Tag substituída com sucesso!")
    else:
        print("Falha ao substituir a tag.")