
from pathlib import Path
import pandas as pd

# Localizar a pasta do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Carregar a base de ordens de serviço
ARQUIVO = PASTA_PROJETO / "data" / "raw" / "ordens_servico.csv"

df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

# Agrupar os indicadores por regional
analise = df.groupby("regional").agg(
    total_ordens=("ordem_id", "count"),
    ordens_concluidas=("status", lambda x: (x == "Concluída").sum()),
    ordens_pendentes=("status", lambda x: (x == "Pendente").sum()),
    ordens_em_andamento=("status", lambda x: (x == "Em andamento").sum()),
    ordens_canceladas=("status", lambda x: (x == "Cancelada").sum())
).reset_index()

# Calcular o backlog e as taxas
analise["backlog"] = (
    analise["ordens_pendentes"] + analise["ordens_em_andamento"]
)

analise["taxa_conclusao_pct"] = (
    analise["ordens_concluidas"] / analise["total_ordens"] * 100
).round(2)

analise["taxa_backlog_pct"] = (
    analise["backlog"] / analise["total_ordens"] * 100
).round(2)

# Ordenar da regional com maior backlog para a menor
analise = analise.sort_values(
    by="backlog", ascending=False
)

# Exibir os resultados
print("=" * 65)
print("RADAR ENERGIA - ANALISE POR REGIONAL")
print("=" * 65)

print(analise.to_string(index=False))

# Salvar o resultado em CSV
SAIDA = PASTA_PROJETO / "data" / "processed" / "indicadores_por_regional.csv"

SAIDA.parent.mkdir(parents=True, exist_ok=True)
analise.to_csv(SAIDA, index=False, encoding="utf-8-sig")

print("\nArquivo salvo em:")
print(SAIDA)
