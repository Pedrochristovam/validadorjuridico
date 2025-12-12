"""
Utilitários para manipulação de arquivos
"""
import os
import json
from pathlib import Path
from typing import Optional


def ensure_upload_dir() -> Path:
    """Garante que o diretório de uploads existe"""
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    return upload_dir


def save_modelo_json(data: dict, filename: str = "modelo.json") -> str:
    """Salva o modelo oficial em JSON"""
    modelo_path = Path(filename)
    with open(modelo_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(modelo_path.absolute())


def load_modelo_json(filename: str = "modelo.json") -> dict:
    """Carrega o modelo oficial do JSON"""
    modelo_path = Path(filename)
    if not modelo_path.exists():
        raise FileNotFoundError(f"Modelo {filename} não encontrado")
    
    with open(modelo_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_uploaded_file(file_content: bytes, filename: str) -> Path:
    """Salva arquivo enviado no diretório de uploads"""
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path


def list_modelos() -> list:
    """Lista todos os modelos salvos"""
    modelos_dir = Path("modelos")
    modelos_dir.mkdir(exist_ok=True)
    
    modelos = []
    
    # Lista arquivos JSON no diretório modelos
    for modelo_file in modelos_dir.glob("*.json"):
        try:
            with open(modelo_file, "r", encoding="utf-8") as f:
                modelo_data = json.load(f)
                # Adiciona apenas informações essenciais
                modelos.append({
                    "id": modelo_data.get("id", modelo_file.stem),
                    "name": modelo_data.get("nome", modelo_file.stem),
                    "created_at": modelo_data.get("created_at", ""),
                    "tipo": modelo_data.get("tipo", "arquivo"),
                    "arquivo_original": modelo_data.get("arquivo_original", None),
                })
        except Exception as e:
            # Se houver erro ao ler um arquivo, continua com os outros
            continue
    
    # Ordena por data de criação (mais recente primeiro)
    modelos.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return modelos


def delete_modelo(modelo_id: str) -> dict:
    """Deleta um modelo específico"""
    modelos_dir = Path("modelos")
    modelos_dir.mkdir(exist_ok=True)
    
    # Procura o arquivo do modelo
    modelo_file = modelos_dir / f"{modelo_id}.json"
    
    if not modelo_file.exists():
        raise FileNotFoundError(f"Modelo {modelo_id} não encontrado")
    
    # Deleta o arquivo
    modelo_file.unlink()
    
    return {
        "success": True,
        "message": f"Modelo {modelo_id} deletado com sucesso"
    }


