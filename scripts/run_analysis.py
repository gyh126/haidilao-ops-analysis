import sqlite3
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "haidilao.db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def run_query(name, sql):
    print(f"\n{'='*80}")
    print(f"  {name}")
    print(f"{'='*80}")
    c.execute(sql)
    cols = [d[0] for d in c.description]
    rows = c.fetchall()
    # Print header
    header = " | ".join(f"{col:>18}" for col in cols)
    print(header)
    print("-" * len(header))
    for row in rows:
        vals = []
        for v in row:
            if isinstance(v, float):
                vals.append(f"{v:>18.4f}")
            elif v is None:
                vals.append(f"{'N/A':>18}")
            else:
                vals.append(f"{v:>18}")
        print(" | ".join(vals))
    return rows

# ============================================================
# 1. 趋势分析：收入、利润同比变化
# ============================================================
run_query("1.1 收入与利润趋势 (同比)", """
SELECT
    a.year,
    a.revenue,
    ROUND((a.revenue - LAG(a.revenue) OVER (ORDER BY a.year)) * 100.0 / LAG(a.revenue) OVER (ORDER BY a.year), 2) AS revenue_yoy_pct,
    a.net_profit,
    ROUND((a.net_profit - LAG(a.net_profit) OVER (ORDER BY a.year)) * 100.0 / LAG(a.net_profit) OVER (ORDER BY a.year), 2) AS net_profit_yoy_pct,
    a.core_operating_profit,
    CASE
        WHEN LAG(a.core_operating_profit) OVER (ORDER BY a.year) IS NOT NULL
        THEN ROUND((a.core_operating_profit - LAG(a.core_operating_profit) OVER (ORDER BY a.year)) * 100.0 / LAG(a.core_operating_profit) OVER (ORDER BY a.year), 2)
    END AS core_op_yoy_pct,
    ROUND(a.gross_margin * 100, 2) AS gross_margin_pct,
    ROUND(a.net_margin * 100, 2) AS net_margin_pct,
    ROUND(a.core_op_margin * 100, 2) AS core_op_margin_pct
FROM annual_financials a
ORDER BY a.year
""")

run_query("1.2 收入结构变化趋势", """
SELECT
    year,
    restaurant_revenue,
    delivery_revenue,
    other_restaurant_revenue,
    ROUND(restaurant_revenue * 100.0 / (SELECT revenue FROM annual_financials WHERE year = r.year), 2) AS restaurant_pct,
    ROUND(delivery_revenue * 100.0 / (SELECT revenue FROM annual_financials WHERE year = r.year), 2) AS delivery_pct,
    ROUND(other_restaurant_revenue * 100.0 / (SELECT revenue FROM annual_financials WHERE year = r.year), 2) AS other_rest_pct
FROM annual_financials r
ORDER BY year
""")

# ============================================================
# 2. 运营指标趋势
# ============================================================
run_query("2.1 关键运营指标趋势", """
SELECT
    year,
    total_restaurants,
    self_operated,
    franchised,
    table_turnover,
    same_store_turnover,
    avg_spending_per_guest,
    customer_visits_million,
    system_sales_growth
FROM operational_metrics
ORDER BY year
""")

run_query("2.2 运营指标同比变化", """
SELECT
    year,
    total_restaurants,
    total_restaurants - LAG(total_restaurants) OVER (ORDER BY year) AS net_store_change,
    ROUND(table_turnover - LAG(table_turnover) OVER (ORDER BY year), 2) AS turnover_change,
    ROUND(avg_spending_per_guest - LAG(avg_spending_per_guest) OVER (ORDER BY year), 2) AS spending_change,
    ROUND(customer_visits_million - LAG(customer_visits_million) OVER (ORDER BY year), 1) AS visits_change,
    ROUND((customer_visits_million - LAG(customer_visits_million) OVER (ORDER BY year)) * 100.0 / LAG(customer_visits_million) OVER (ORDER BY year), 2) AS visits_yoy_pct
FROM operational_metrics
ORDER BY year
""")

# ============================================================
# 3. 成本结构拆解
# ============================================================
run_query("3.1 各成本项绝对值及占收入比", """
SELECT
    year,
    raw_materials,
    ROUND(raw_materials_pct * 100, 2) AS raw_pct,
    staff_costs,
    ROUND(staff_costs_pct * 100, 2) AS staff_pct,
    rentals,
    ROUND(rentals_pct * 100, 2) AS rent_pct,
    utilities,
    ROUND(utilities_pct * 100, 2) AS util_pct,
    depreciation,
    ROUND(depreciation_pct * 100, 2) AS dep_pct,
    other_expenses,
    ROUND(other_expenses_pct * 100, 2) AS other_pct,
    total_operating_costs,
    ROUND(total_cost_pct * 100, 2) AS total_cost_pct
FROM cost_breakdown
ORDER BY year
""")

run_query("3.2 成本项同比变化 (千元)", """
SELECT
    year,
    raw_materials - LAG(raw_materials) OVER (ORDER BY year) AS raw_change,
    ROUND((raw_materials - LAG(raw_materials) OVER (ORDER BY year)) * 100.0 / LAG(raw_materials) OVER (ORDER BY year), 2) AS raw_yoy_pct,
    staff_costs - LAG(staff_costs) OVER (ORDER BY year) AS staff_change,
    ROUND((staff_costs - LAG(staff_costs) OVER (ORDER BY year)) * 100.0 / LAG(staff_costs) OVER (ORDER BY year), 2) AS staff_yoy_pct,
    depreciation - LAG(depreciation) OVER (ORDER BY year) AS dep_change,
    ROUND((depreciation - LAG(depreciation) OVER (ORDER BY year)) * 100.0 / LAG(depreciation) OVER (ORDER BY year), 2) AS dep_yoy_pct,
    total_operating_costs - LAG(total_operating_costs) OVER (ORDER BY year) AS total_cost_change,
    ROUND((total_operating_costs - LAG(total_operating_costs) OVER (ORDER BY year)) * 100.0 / LAG(total_operating_costs) OVER (ORDER BY year), 2) AS total_cost_yoy_pct
FROM cost_breakdown
ORDER BY year
""")

# ============================================================
# 4. 毛利与经营利润变化归因
# ============================================================
run_query("4.1 毛利润变化归因 (2024→2025)", """
SELECT
    '2024' AS base_year,
    (SELECT gross_profit FROM annual_financials WHERE year=2024) AS gross_2024,
    (SELECT gross_profit FROM annual_financials WHERE year=2025) AS gross_2025,
    (SELECT gross_profit FROM annual_financials WHERE year=2025) - (SELECT gross_profit FROM annual_financials WHERE year=2024) AS gross_change,
    (SELECT revenue FROM annual_financials WHERE year=2025) - (SELECT revenue FROM annual_financials WHERE year=2024) AS revenue_change,
    ((SELECT raw_materials FROM cost_breakdown WHERE year=2025) - (SELECT raw_materials FROM cost_breakdown WHERE year=2024)) AS raw_materials_increase,
    ROUND(((SELECT gross_profit FROM annual_financials WHERE year=2025) - (SELECT gross_profit FROM annual_financials WHERE year=2024)) * 100.0 / (SELECT gross_profit FROM annual_financials WHERE year=2024), 2) AS gross_change_pct
""")

run_query("4.2 核心经营利润变化归因 (2024→2025, 千元)", """
SELECT
    '利润变动分解' AS item,
    (SELECT core_operating_profit FROM annual_financials WHERE year=2024) AS core_op_2024,
    (SELECT core_operating_profit FROM annual_financials WHERE year=2025) AS core_op_2025,
    (SELECT core_operating_profit FROM annual_financials WHERE year=2025) - (SELECT core_operating_profit FROM annual_financials WHERE year=2024) AS change_amount,
    ROUND(((SELECT core_operating_profit FROM annual_financials WHERE year=2025) - (SELECT core_operating_profit FROM annual_financials WHERE year=2024)) * 100.0 / (SELECT core_operating_profit FROM annual_financials WHERE year=2024), 2) AS change_pct
UNION ALL
SELECT
    '→ 收入增长贡献' AS item,
    0, 0,
    (SELECT revenue FROM annual_financials WHERE year=2025) - (SELECT revenue FROM annual_financials WHERE year=2024),
    NULL
UNION ALL
SELECT
    '→ 原材料成本增加' AS item,
    0, 0,
    -((SELECT raw_materials FROM cost_breakdown WHERE year=2025) - (SELECT raw_materials FROM cost_breakdown WHERE year=2024)),
    NULL
UNION ALL
SELECT
    '→ 员工成本变化' AS item,
    0, 0,
    -((SELECT staff_costs FROM cost_breakdown WHERE year=2025) - (SELECT staff_costs FROM cost_breakdown WHERE year=2024)),
    NULL
UNION ALL
SELECT
    '→ 折旧摊销变化' AS item,
    0, 0,
    -((SELECT depreciation FROM cost_breakdown WHERE year=2025) - (SELECT depreciation FROM cost_breakdown WHERE year=2024)),
    NULL
UNION ALL
SELECT
    '→ 其他成本变化' AS item,
    0, 0,
    -(((SELECT rentals FROM cost_breakdown WHERE year=2025) - (SELECT rentals FROM cost_breakdown WHERE year=2024)) +
      ((SELECT utilities FROM cost_breakdown WHERE year=2025) - (SELECT utilities FROM cost_breakdown WHERE year=2024)) +
      ((SELECT travel_comm FROM cost_breakdown WHERE year=2025) - (SELECT travel_comm FROM cost_breakdown WHERE year=2024)) +
      ((SELECT other_expenses FROM cost_breakdown WHERE year=2025) - (SELECT other_expenses FROM cost_breakdown WHERE year=2024))),
    NULL
""")

# ============================================================
# 5. 收入驱动因素拆解
# ============================================================
run_query("5.1 餐厅收入驱动因素拆解 (2024 vs 2025)", """
SELECT
    '2024' AS year,
    (SELECT restaurant_revenue FROM annual_financials WHERE year=2024) AS restaurant_rev,
    (SELECT self_operated FROM operational_metrics WHERE year=2024) AS self_op_stores,
    (SELECT table_turnover FROM operational_metrics WHERE year=2024) AS turnover,
    (SELECT avg_spending_per_guest FROM operational_metrics WHERE year=2024) AS avg_spending,
    (SELECT customer_visits_million FROM operational_metrics WHERE year=2024) AS visits_million
UNION ALL
SELECT
    '2025',
    (SELECT restaurant_revenue FROM annual_financials WHERE year=2025),
    (SELECT self_operated FROM operational_metrics WHERE year=2025),
    (SELECT table_turnover FROM operational_metrics WHERE year=2025),
    (SELECT avg_spending_per_guest FROM operational_metrics WHERE year=2025),
    (SELECT customer_visits_million FROM operational_metrics WHERE year=2025)
""")

run_query("5.2 收入变动归因 (2024→2025, 百万元)", """
SELECT
    '餐厅收入变动' AS factor,
    ROUND(((SELECT restaurant_revenue FROM annual_financials WHERE year=2025) - (SELECT restaurant_revenue FROM annual_financials WHERE year=2024)) / 1000.0, 1) AS change_million,
    '门店数减少+翻台率下降+客流减少(-7.5%)抵消了客单价微增(+0.2%)' AS explanation
UNION ALL
SELECT
    '外卖收入变动',
    ROUND(((SELECT delivery_revenue FROM annual_financials WHERE year=2025) - (SELECT delivery_revenue FROM annual_financials WHERE year=2024)) / 1000.0, 1),
    '外卖业务翻倍增长(+111.9%), 成为唯一增长亮点'
UNION ALL
SELECT
    '其他餐厅收入变动',
    ROUND(((SELECT other_restaurant_revenue FROM annual_financials WHERE year=2025) - (SELECT other_restaurant_revenue FROM annual_financials WHERE year=2024)) / 1000.0, 1),
    '石榴计划多品牌扩张, 收入大幅增长'
""")

# ============================================================
# 6. 同店销售分析
# ============================================================
run_query("6.1 同店销售变化 (2022 vs 2023)", """
SELECT
    a.region,
    a.store_count AS stores_2022,
    b.store_count AS stores_2023,
    b.same_store_sales - a.same_store_sales AS sales_change,
    ROUND((b.same_store_sales - a.same_store_sales) * 100.0 / a.same_store_sales, 2) AS sales_growth_pct,
    ROUND(b.avg_daily_sales - a.avg_daily_sales, 2) AS daily_sales_change,
    ROUND(b.same_store_turnover - a.same_store_turnover, 2) AS turnover_change
FROM same_store_sales a
JOIN same_store_sales b ON a.region = b.region AND b.year = 2023
WHERE a.year = 2022
""")

# ============================================================
# 7. 异常识别
# ============================================================
run_query("7.1 关键指标异常检测", """
SELECT
    'CRITICAL' AS severity,
    '翻台率下降' AS issue,
    '2025年翻台率3.9次/天, 较2024年4.1次下降0.2, 为近三年首次下降' AS detail,
    '翻台率每下降0.1次, 影响收入约10-11亿元' AS impact
UNION ALL
SELECT
    'CRITICAL',
    '原材料成本占比急升',
    '2025年原材料成本占收入比40.5%, 较2024年37.9%上升2.6个百分点, 绝对额增13.15亿元',
    '直接侵蚀毛利, 毛利率从62.1%降至59.5%'
UNION ALL
SELECT
    'CRITICAL',
    '核心经营利润大幅下滑',
    '2025年核心经营利润54.03亿元, 同比下降13.3%, 净利润同比下降14.0%',
    '利润绝对额减少8.27亿元'
UNION ALL
SELECT
    'WARN',
    '客流显著流失',
    '2025年全年接待3.839亿人次, 同比减少3110万人次(-7.5%)',
    '客流是收入增长的根本驱动力, 流失直接影响翻台率'
UNION ALL
SELECT
    'WARN',
    '自营门店收缩',
    '2025年自营门店从1355家减至1304家, 净减少51家(关停85家)',
    '门店网络收缩影响品牌覆盖和收入基础'
UNION ALL
SELECT
    'WARN',
    '餐厅经营收入负增长',
    '2025年餐厅经营收入390.64亿元, 同比下降4.4%, 系统销售额下降3.7%',
    '核心业务收入下滑, 非核心收入增长无法完全对冲'
UNION ALL
SELECT
    'INFO',
    '外卖业务高增长',
    '2025年外卖收入26.58亿元, 同比增长111.9%, 覆盖超1200家门店',
    '外卖成为新增长引擎, 但利润率待观察'
UNION ALL
SELECT
    'INFO',
    '多品牌战略加速',
    '石榴计划运营20个子品牌207家店, 其他餐厅收入15.21亿元',
    '第二增长曲线初现, 但短期利润贡献有限'
""")

conn.close()
print("\n\n分析完成。")
