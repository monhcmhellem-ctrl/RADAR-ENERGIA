
from pathlib import Path
import pandas as pd

# Localiza a pasta principal do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "data" / "raw"

arquivos = [
    "ordens_servico.csv",
    "equipes.csv",
    "ocorrencias_energia.csv",
    "regionais.csv",
]

print("=" * 50)
print("RADAR ENERGIA - VALIDACAO INICIAL")
print("=" * 50)

for nome_arquivo in arquivos:
    caminho = PASTA_DADOS / nome_arquivo

    if not caminho.exists():
        print(f"\nERRO: arquivo nao encontrado: {nome_arquivo}")
        continue

    df = pd.read_csv(caminho, encoding="utf-8-sig")

    print(f"\nArquivo: {nome_arquivo}")
    print(f"Quantidade de registros: {len(df)}")
    print(f"Quantidade de colunas: {len(df.columns)}")
    print(f"Colunas: {', '.join(df.columns)}")

print("\nValidacao inicial concluida.")
