
from pathlib import Path
import pandas as pd

# Localizar a pasta do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Carregar a base de ordens de serviço
ARQUIVO = (
    PASTA_PROJETO
    / "data"
    / "raw"
    / "ordens_servico.csv"
)

df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

# Normalizar o campo de reincidência
df["reincidente_30_dias"] = (
    df["reincidente_30_dias"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Considerar como reincidente os registros marcados como verdadeiro
valores_verdadeiros = ["true", "1", "sim", "s", "yes"]

df["eh_reincidente"] = df["reincidente_30_dias"].isin(
    valores_verdadeiros
)

# Indicadores gerais
total_ordens = len(df)
total_reincidentes = int(df["eh_reincidente"].sum())

taxa_reincidencia = (
    total_reincidentes / total_ordens * 100
    if total_ordens else 0
)

# Análise por regional
analise = df.groupby("regional").agg(
    total_ordens=("ordem_id", "count"),
    ordens_reincidentes=("eh_reincidente", "sum")
).reset_index()

analise["ordens_sem_reincidencia"] = (
    analise["total_ordens"] - analise["ordens_reincidentes"]
)

analise["taxa_reincidencia_pct"] = (
    analise["ordens_reincidentes"]
    / analise["total_ordens"] * 100
).round(2)

analise = analise.sort_values(
    by="taxa_reincidencia_pct",
    ascending=False
)

# Exibir resultados
print("=" * 60)
print("RADAR ENERGIA - ANALISE DE REINCIDENCIA")
print("=" * 60)

print(f"Total de ordens: {total_ordens}")
print(f"Ordens reincidentes: {total_reincidentes}")
print(f"Taxa geral de reincidencia: {taxa_reincidencia:.2f}%")

print("\nANALISE POR REGIONAL")
print(analise.to_string(index=False))

# Salvar resultados
SAIDA = (
    PASTA_PROJETO
    / "data"
    / "processed"
    / "indicadores_reincidencia_por_regional.csv"
)

SAIDA.parent.mkdir(parents=True, exist_ok=True)

analise.to_csv(
    SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo salvo em:")
print(SAIDA)
