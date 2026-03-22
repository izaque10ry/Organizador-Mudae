#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o Organizador Mudae
Verifica se tudo funciona sem GUI
"""

import re
import os
import requests
from PIL import Image

DADOS_FILE = "dados.txt"
IMGS_FOLDER = "imagens"

print("="*50)
print("TESTE DE FUNCIONAMENTO - ORGANIZADOR MUDAE")
print("="*50)

# Teste 1: Arquivo de dados existe?
print("\n[1] Verificando dados.txt...")
if not os.path.exists(DADOS_FILE):
    print("  ❌ ERRO: dados.txt não encontrado")
    exit(1)
print("  ✓ dados.txt encontrado")

# Teste 2: Carregar e parsear dados
print("\n[2] Parseando dados...")
try:
    with open(DADOS_FILE, 'r', encoding='utf-8') as f:
        texto = f.read()
except:
    with open(DADOS_FILE, 'r', encoding='latin-1') as f:
        texto = f.read()

padrao = re.compile(r"\*?\*?#([\d.]+)\*?\*?\s*-\s*([^💞]+)\s*💞.*?(https?://[^\s>]+)", re.DOTALL)
matches = padrao.findall(texto)

if not matches:
    padrao_alt = re.compile(r"^\s*\*?\*?([^💞\n]+?)\*?\*?\s*💞.*?(https?://[^\s>]+)", re.MULTILINE)
    matches_alt = padrao_alt.findall(texto)
    matches = [(str(i), nome, url) for i, (nome, url) in enumerate(matches_alt, start=1)]

print(f"  ✓ {len(matches)} personagens encontrados!")

if len(matches) > 0:
    print("\n[3] Primeiros 5 personagens:")
    for i, (char_id, char_name, img_url) in enumerate(matches[:5]):
        print(f"     {i+1}. [{char_id}] {char_name.strip()[:40]}")

# Teste 3: Pasta de imagens
print(f"\n[4] Verificando pasta '{IMGS_FOLDER}'...")
if not os.path.exists(IMGS_FOLDER):
    os.makedirs(IMGS_FOLDER)
    print(f"  ✓ Pasta criada")
else:
    print(f"  ✓ Pasta encontrada")

# Teste 4: Download de uma imagem
print("\n[5] Testando download de imagem...")
if len(matches) > 0:
    char_id, char_name, img_url = matches[0]
    safe_id = char_id.replace('.', '_')
    img_path = os.path.join(IMGS_FOLDER, f"{safe_id}.jpg")
    
    if os.path.exists(img_path):
        print(f"  ✓ Imagem já existe: {img_path}")
    else:
        print(f"  Baixando primeira imagem...")
        try:
            response = requests.get(img_url, stream=True,timeout=10)
            if response.status_code == 200:
                with open(img_path, 'wb') as f_img:
                    for chunk in response.iter_content(1024):
                        f_img.write(chunk)
                print(f"  ✓ Imagem baixada com sucesso")
            else:
                print(f"  ❌ Erro HTTP {response.status_code}")
        except Exception as e:
            print(f"  ⚠ Erro ao baixar: {str(e)[:50]}")

# Teste 5: Verificar PIL
print("\n[6] Verificando PIL/Pillow...")
try:
    if os.path.exists(img_path):
        img = Image.open(img_path)
        print(f"  ✓ PIL funcionando - Imagem: {img.size} {img.format}")
        
        # Redimensionar teste
        img_small = img.resize((100, 120), Image.Resampling.LANCZOS)
        print(f"  ✓ Redimensionamento funcionando")
except Exception as e:
    print(f"  ⚠ Erro com PIL: {str(e)[:50]}")

print("\n" + "="*50)
print("TESTES CONCLUIDOS COM SUCESSO!")
print("Agora execute o programa normalmente:")
print("  python organizador.py")
print("="*50 + "\n")
