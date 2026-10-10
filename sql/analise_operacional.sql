
-- =====================================================
-- PROJETO: RADAR ENERGIA
-- OBJETIVO: Analise de indicadores operacionais
-- Base utilizada: ordens_servico
-- Dados ficticios para portfolio
-- =====================================================

-- 1. Quantidade de ordens por status
SELECT
    status,
    COUNT(*) AS quantidade_ordens
FROM ordens_servico
GROUP BY status
ORDER BY quantidade_ordens DESC;


-- 2. Indicadores gerais de ordens de servico
SELECT
    COUNT(*) AS total_ordens,
    SUM(CASE WHEN status = 'Concluída' THEN 1 ELSE 0 END) AS ordens_concluidas,
    SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END) AS ordens_pendentes,
    SUM(CASE WHEN status = 'Em andamento' THEN 1 ELSE 0 END) AS ordens_em_andamento,
    SUM(CASE WHEN status = 'Cancelada' THEN 1 ELSE 0 END) AS ordens_canceladas
FROM ordens_servico;


-- 3. Taxa de conclusao das ordens (%)
SELECT
    COUNT(*) AS total_ordens,
    SUM(CASE WHEN status = 'Concluída' THEN 1 ELSE 0 END) AS ordens_concluidas,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'Concluída' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS taxa_conclusao_pct
FROM ordens_servico;


-- 4. Backlog operacional por status
SELECT
    status,
    COUNT(*) AS quantidade
FROM ordens_servico
WHERE status IN ('Pendente', 'Em andamento')
GROUP BY status
ORDER BY quantidade DESC;


-- 5. Indicadores por regional
SELECT
    regional,
    COUNT(*) AS total_ordens,
    SUM(CASE WHEN status = 'Concluída' THEN 1 ELSE 0 END) AS ordens_concluidas,
    SUM(CASE WHEN status IN ('Pendente', 'Em andamento') THEN 1 ELSE 0 END) AS backlog
FROM ordens_servico
GROUP BY regional
ORDER BY backlog DESC;
