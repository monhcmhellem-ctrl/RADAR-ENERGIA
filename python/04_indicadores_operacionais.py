
from pathlib import Path
import pandas as pd

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO = PASTA_PROJETO / "data" / "raw" / "ordens_servico.csv"

df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

total = len(df)
concluidas = (df["status"] == "Concluída").sum()
pendentes = (df["status"] == "Pendente").sum()
em_andamento = (df["status"] == "Em andamento").sum()
canceladas = (df["status"] == "Cancelada").sum()

backlog = pendentes + em_andamento

taxa_conclusao = concluidas / total * 100 if total else 0
taxa_backlog = backlog / total * 100 if total else 0

print("=" * 50)
print("RADAR ENERGIA - INDICADORES OPERACIONAIS")
print("=" * 50)

print(f"Total de ordens: {total}")
print(f"Ordens concluidas: {concluidas}")
print(f"Ordens pendentes: {pendentes}")
print(f"Ordens em andamento: {em_andamento}")
print(f"Ordens canceladas: {canceladas}")
print(f"Backlog operacional: {backlog}")
print(f"Taxa de conclusao: {taxa_conclusao:.2f}%")
print(f"Taxa de backlog: {taxa_backlog:.2f}%")
