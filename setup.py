#!/usr/bin/env python3
"""
Script de configuração e instalação do Sistema de Criptografia
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directory_structure():
    """Cria a estrutura de diretórios necessária"""
    directories = [
        "modules",
        "modules/auth",
        "modules/crypto", 
        "modules/file_ops",
        "modules/utils",
        "logs"
    ]
    
    print("📁 Criando estrutura de diretórios...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✓ {directory}")
    
    # Cria arquivos __init__.py para tornar os diretórios em pacotes Python
    init_files = [
        "modules/__init__.py",
        "modules/auth/__init__.py",
        "modules/crypto/__init__.py",
        "modules/file_ops/__init__.py",
        "modules/utils/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()

def install_requirements():
    """Instala as dependências necessárias"""
    print("\n📦 Instalando dependências...")
    
    try:
        # Verifica se pip está disponível
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # Instala dependências
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("  ✓ Dependências instaladas com sucesso!")
        
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Erro ao instalar dependências: {e}")
        print("  💡 Tente executar manualmente: pip install -r requirements.txt")
        return False
    
    return True

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("  ❌ Python 3.7 ou superior é necessário!")
        return False
    
    print("  ✓ Versão do Python compatível")
    return True

def create_sample_files():
    """Cria arquivos de exemplo para testar o sistema"""
    sample_dir = Path("sample_files")
    sample_dir.mkdir(exist_ok=True)
    
    # Arquivo de texto simples
    with open(sample_dir / "exemplo.txt", "w", encoding="utf-8") as f:
        f.write("Este é um arquivo de exemplo para testar a criptografia AES.\n")
        f.write("O sistema deve ser capaz de criptografar e descriptografar este arquivo.\n")
        f.write("Data de criação: 2025-09-04\n")
    
    # Arquivo JSON
    import json
    sample_data = {
        "nome": "Sistema de Criptografia AES",
        "versao": "1.0.0",
        "autor": "Claude Assistant", 
        "recursos": [
            "Criptografia AES-256",
            "Interface de linha de comando",
            "Backup automático",
            "Logs detalhados"
        ]
    }
    
    with open(sample_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Arquivos de exemplo criados em: {sample_dir}")

def main():
    """Função principal de configuração"""
    print("=" * 60)
    print("  CONFIGURAÇÃO DO SISTEMA DE CRIPTOGRAFIA AES")
    print("=" * 60)
    
    # Verifica versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Cria estrutura de diretórios
    create_directory_structure()
    
    # Instala dependências
    if not install_requirements():
        print("\n⚠️  Aviso: Algumas dependências podem não ter sido instaladas.")
        print("   Execute 'pip install -r requirements.txt' manualmente se necessário.")
    
    # Cria arquivos de exemplo
    create_sample_files()
    
    print("\n" + "=" * 60)
    print("  ✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n🚀 Para usar o sistema:")
    print("   python main.py")
    print("\n📚 Estrutura do projeto:")
    print("   ├── main.py                    # Programa principal")
    print("   ├── requirements.txt           # Dependências")
    print("   ├── modules/                   # Módulos do sistema")
    print("   │   ├── auth/                  # Gerenciamento de senhas")
    print("   │   ├── crypto/                # Criptografia AES")
    print("   │   ├── file_ops/              # Operações de arquivo")
    print("   │   └── utils/                 # Utilitários (logging)")
    print("   ├── logs/                      # Arquivos de log")
    print("   └── sample_files/              # Arquivos de exemplo")
    
    print("\n📝 Recursos disponíveis:")
    print("   • Criptografia AES-256 segura")
    print("   • Interface intuitiva de linha de comando") 
    print("   • Backup automático de arquivos criptografados")
    print("   • Sistema de logging detalhado")
    print("   • Validação de senha com critérios de segurança")
    print("   • Suporte a múltiplos formatos de arquivo")

if __name__ == "__main__":
    main()