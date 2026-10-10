
from pathlib import Path
import pandas as pd

# 1. Localizar as pastas do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "data" / "raw"
PASTA_PROCESSADOS = PASTA_PROJETO / "data" / "processed"

# 2. Carregar a base principal
ARQUIVO = PASTA_DADOS / "ordens_servico.csv"
df = pd.read_csv(ARQUIVO, encoding="utf-8-sig")

# 3. Padronizar o campo de reincidência
df["reincidente_30_dias"] = (
    df["reincidente_30_dias"]
    .astype(str)
    .str.strip()
    .str.lower()
)

valores_verdadeiros = ["true", "1", "sim", "s", "yes"]

df["eh_reincidente"] = df["reincidente_30_dias"].isin(
    valores_verdadeiros
)

# 4. Criar os indicadores por regional
indicadores = df.groupby("regional").agg(
    total_ordens=("ordem_id", "count"),
    ordens_concluidas=(
        "status",
        lambda x: (x == "Concluída").sum()
    ),
    ordens_pendentes=(
        "status",
        lambda x: (x == "Pendente").sum()
    ),
    ordens_em_andamento=(
        "status",
        lambda x: (x == "Em andamento").sum()
    ),
    ordens_canceladas=(
        "status",
        lambda x: (x == "Cancelada").sum()
    ),
    ordens_reincidentes=("eh_reincidente", "sum")
).reset_index()

# 5. Calcular backlog e taxas
indicadores["backlog"] = (
    indicadores["ordens_pendentes"]
    + indicadores["ordens_em_andamento"]
)

indicadores["taxa_conclusao_pct"] = (
    indicadores["ordens_concluidas"]
    / indicadores["total_ordens"] * 100
).round(2)

indicadores["taxa_backlog_pct"] = (
    indicadores["backlog"]
    / indicadores["total_ordens"] * 100
).round(2)

indicadores["taxa_reincidencia_pct"] = (
    indicadores["ordens_reincidentes"]
    / indicadores["total_ordens"] * 100
).round(2)

# 6. Calcular indicadores de SLA somente para ordens concluídas
concluidas = df[df["status"] == "Concluída"].copy()

concluidas["horas_atraso_sla"] = pd.to_numeric(
    concluidas["horas_atraso_sla"],
    errors="coerce"
)

concluidas["fora_sla"] = (
    concluidas["horas_atraso_sla"] > 0
)

sla = concluidas.groupby("regional").agg(
    ordens_concluidas_sla=("ordem_id", "count"),
    ordens_com_atraso=("fora_sla", "sum")
).reset_index()

sla["taxa_atraso_pct"] = (
    sla["ordens_com_atraso"]
    / sla["ordens_concluidas_sla"] * 100
).round(2)

sla["taxa_dentro_sla_pct"] = (
    100 - sla["taxa_atraso_pct"]
).round(2)

# 7. Integrar os indicadores de SLA
indicadores = indicadores.merge(
    sla[
        [
            "regional",
            "ordens_concluidas_sla",
            "ordens_com_atraso",
            "taxa_atraso_pct",
            "taxa_dentro_sla_pct"
        ]
    ],
    on="regional",
    how="left"
)

# 8. Ordenar por maior backlog
indicadores = indicadores.sort_values(
    "backlog",
    ascending=False
)

# 9. Exibir o resultado
print("=" * 75)
print("RADAR ENERGIA - INDICADORES CONSOLIDADOS POR REGIONAL")
print("=" * 75)

print(indicadores.to_string(index=False))

# 10. Exportar para CSV
PASTA_PROCESSADOS.mkdir(parents=True, exist_ok=True)

SAIDA = (
    PASTA_PROCESSADOS
    / "radar_indicadores_consolidados.csv"
)

indicadores.to_csv(
    SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo consolidado salvo em:")
print(SAIDA)

print(f"\nTotal de regionais analisadas: {len(indicadores)}")
print(f"Total de ordens analisadas: {indicadores['total_ordens'].sum()}")
