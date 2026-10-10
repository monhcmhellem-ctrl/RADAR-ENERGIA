
from pathlib import Path
import pandas as pd

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO = PASTA_PROJETO / "data" / "raw" / "ordens_servico.csv"

df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

print("=" * 50)
print("RADAR ENERGIA - ANALISE DE STATUS")
print("=" * 50)

print("\nQuantidade de ordens por status:")
print(df["status"].value_counts().to_string())

print("\nValores ausentes por status:")
campos = [
    "data_conclusao",
    "duracao_execucao_horas",
    "horas_atraso_sla",
]

resultado = df.groupby("status")[campos].apply(
    lambda grupo: grupo.isna().sum()
)

print(resultado.to_string())

print("\nAnalise de status concluida.")
