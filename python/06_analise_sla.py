
from pathlib import Path
import pandas as pd

# Localizar a pasta do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Carregar a base de ordens de serviço
ARQUIVO = PASTA_PROJETO / "data" / "raw" / "ordens_servico.csv"

df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

# Converter os campos numéricos
df["horas_atraso_sla"] = pd.to_numeric(
    df["horas_atraso_sla"], errors="coerce"
)

# Considerar apenas ordens concluídas
concluidas = df[df["status"] == "Concluída"].copy()

# Identificar ordens concluídas com atraso no SLA
concluidas["fora_sla"] = concluidas["horas_atraso_sla"] > 0

total_concluidas = len(concluidas)
fora_sla = int(concluidas["fora_sla"].sum())
dentro_sla = total_concluidas - fora_sla

taxa_atraso = (
    fora_sla / total_concluidas * 100
    if total_concluidas else 0
)

taxa_dentro_sla = (
    dentro_sla / total_concluidas * 100
    if total_concluidas else 0
)

# Analisar o resultado por regional
analise = concluidas.groupby("regional").agg(
    ordens_concluidas=("ordem_id", "count"),
    ordens_com_atraso=("fora_sla", "sum")
).reset_index()

analise["ordens_dentro_sla"] = (
    analise["ordens_concluidas"] - analise["ordens_com_atraso"]
)

analise["taxa_atraso_pct"] = (
    analise["ordens_com_atraso"]
    / analise["ordens_concluidas"] * 100
).round(2)

analise = analise.sort_values(
    by="taxa_atraso_pct", ascending=False
)

# Exibir indicadores gerais
print("=" * 60)
print("RADAR ENERGIA - ANALISE DE SLA")
print("=" * 60)

print(f"Ordens concluidas: {total_concluidas}")
print(f"Ordens concluidas com atraso: {fora_sla}")
print(f"Ordens concluidas dentro do SLA: {dentro_sla}")
print(f"Taxa de atraso: {taxa_atraso:.2f}%")
print(f"Taxa dentro do SLA: {taxa_dentro_sla:.2f}%")

print("\nANALISE POR REGIONAL")
print(analise.to_string(index=False))

# Salvar o resultado
SAIDA = (
    PASTA_PROJETO
    / "data"
    / "processed"
    / "indicadores_sla_por_regional.csv"
)

SAIDA.parent.mkdir(parents=True, exist_ok=True)
analise.to_csv(SAIDA, index=False, encoding="utf-8-sig")

print("\nArquivo salvo em:")
print(SAIDA)
