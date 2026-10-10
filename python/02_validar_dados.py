
from pathlib import Path
import pandas as pd

# Caminhos do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "data" / "raw"

arquivos = [
    "ordens_servico.csv",
    "equipes.csv",
    "ocorrencias_energia.csv",
    "regionais.csv",
]

print("=" * 60)
print("RADAR ENERGIA - VALIDACAO DA QUALIDADE DOS DADOS")
print("=" * 60)

for nome_arquivo in arquivos:
    caminho = PASTA_DADOS / nome_arquivo

    print(f"\n{'-' * 60}")
    print(f"Arquivo: {nome_arquivo}")

    df = pd.read_csv(caminho, encoding="utf-8-sig")

    # Quantidade de registros e colunas
    print(f"Registros: {len(df)}")
    print(f"Colunas: {len(df.columns)}")

    # Verificar valores ausentes
    ausentes = int(df.isna().sum().sum())
    print(f"Valores ausentes: {ausentes}")

    # Verificar linhas duplicadas
    duplicados = int(df.duplicated().sum())
    print(f"Linhas duplicadas: {duplicados}")

    # Verificar colunas com valores ausentes
    colunas_ausentes = df.columns[df.isna().any()].tolist()

    if colunas_ausentes:
        print(f"Colunas com ausencias: {colunas_ausentes}")
    else:
        print("Colunas com ausencias: nenhuma")

    # Tipos de dados
    print("\nTipos de dados:")
    print(df.dtypes.to_string())

print("\nValidacao de qualidade concluida.")
