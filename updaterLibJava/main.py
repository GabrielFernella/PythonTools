import os
import re
import git
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse, urlunparse

class VersionUpdater:
    @staticmethod
    def increment_version(current_version):
        """
        Incrementa a versão semanticamente 
        ultima versão de patch/build
        
        :param current_version: Versão atual no formato x.y.z
        :return: Nova versão incrementada
        """
        # Separar partes da versão
        parts = current_version.split('.')
        
        # Se tiver 2 partes, adiciona zero como patch
        if len(parts) == 2:
            parts.append('0')
        
        # Incrementa último componente
        parts[-1] = str(int(parts[-1]) + 1)
        
        return '.'.join(parts)

    @staticmethod
    def update_pom_version(pom_path):
        """
        Atualiza a versão no arquivo pom.xml
        
        :param pom_path: Caminho do arquivo pom.xml
        :return: Versão antiga e nova
        """
        # Parse XML
        tree = ET.parse(pom_path)
        root = tree.getroot()
        
        # Namespace do XML
        namespace = {'ns': 'http://maven.apache.org/POM/4.0.0'}
        
        # Encontrar elemento de versão
        version_element = root.find('.//ns:version', namespace)
        
        if version_element is not None:
            # Versão atual
            old_version = version_element.text
            
            # Nova versão
            new_version = VersionUpdater.increment_version(old_version)
            
            # Atualizar versão
            version_element.text = new_version
            
            # Salvar arquivo
            tree.write(pom_path, encoding='utf-8', xml_declaration=True)
            
            return old_version, new_version
        
        return None, None

class LibUpdater:
    def __init__(self, repositories):
        """
        Inicializa o atualizador de libs
        
        :param repositories: Lista de URLs de repositórios Git com branch opcional
        """
        self.repositories = repositories

    def parse_repo_url(self, repo_url):
        """
        Extrai URL do repositório e branch (se especificada)
        
        :param repo_url: URL do repositório com possível branch
        :return: Tupla (url_sem_branch, branch)
        """
        # Padrão para detectar branch na URL
        # Formatos suportados:
        # https://github.com/usuario/repo.git@branch
        # https://github.com/usuario/repo.git#branch
        if '@' in repo_url:
            url, branch = repo_url.split('@')
        elif '#' in repo_url:
            url, branch = repo_url.split('#')
        else:
            url, branch = repo_url, 'main'
        
        return url, branch

    def process_repositories(self):
        """
        Processa todos os repositórios, atualizando versão
        """
        for repo_url in self.repositories:
            # Extrair URL e branch
            clean_url, target_branch = self.parse_repo_url(repo_url)
            
            # Nome do repositório
            repo_name = clean_url.split('/')[-1].replace('.git', '')
            
            # Clonar repositório
            print(f"Clonando repositório: {repo_name}")
            repo = git.Repo.clone_from(clean_url, repo_name)
            
            # Mudar para branch específica
            repo.git.checkout(target_branch)
            
            # Flag para verificar se houve alteração
            version_updated = False
            
            # Encontrar arquivos pom.xml
            for root, dirs, files in os.walk(repo_name):
                for file in files:
                    if file == 'pom.xml':
                        full_path = os.path.join(root, file)
                        
                        # Atualizar versão no pom
                        old_version, new_version = VersionUpdater.update_pom_version(full_path)
                        
                        if old_version and new_version:
                            version_updated = True
                            print(f"Versão atualizada: {old_version} -> {new_version}")
            
            # Se houve atualização, criar branch e commitar
            if version_updated:
                # Criar branch de release
                timestamp = datetime.now().strftime("%Y%m%d")
                branch_name = f"release/version-{new_version}-{timestamp}"
                
                # Mudar para a nova branch
                repo.git.checkout('-b', branch_name)
                
                # Adicionar e commitar mudanças
                repo.git.add('.')
                commit_message = f"Bump project version to {new_version}"
                repo.git.commit('-m', commit_message)
                
                # Fazer push da nova branch
                repo.git.push('--set-upstream', 'origin', branch_name)
                
                print(f"Repositório {repo_name} atualizado com nova branch: {branch_name}")
            else:
                print(f"Nenhuma atualização necessária para {repo_name}")

def main():
    # Configuração dos repositórios com suporte a branch específica
    repositories = [
        'https://github.com/usuario/repo1.git@develop',  # Especifica branch develop
        'https://github.com/usuario/repo2.git#main',     # Especifica branch main
        'https://github.com/usuario/repo3.git',          # Usa branch padrão (main)
    ]
    
    # Iniciar atualização
    updater = LibUpdater(repositories)
    updater.process_repositories()

if __name__ == '__main__':
    main()