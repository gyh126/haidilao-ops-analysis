import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "haidilao.db")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ============================================================
# 1. 年度财务汇总表
# ============================================================
c.execute("""
CREATE TABLE annual_financials (
    year INTEGER PRIMARY KEY,
    revenue INTEGER,                    -- 总收入(千元)
    restaurant_revenue INTEGER,         -- 餐厅经营收入(千元)
    delivery_revenue INTEGER,           -- 外卖业务收入(千元)
    condiment_revenue INTEGER,          -- 调味品及食材销售(千元)
    other_restaurant_revenue INTEGER,  -- 其他餐厅经营(千元)
    franchise_revenue INTEGER,          -- 特许经营业务(千元)
    others_revenue INTEGER,             -- 其他收入(千元)
    profit_before_tax INTEGER,          -- 除税前利润(千元)
    net_profit INTEGER,                 -- 年内利润(千元)
    core_operating_profit INTEGER,      -- 核心经营利润(千元, non-IFRS)
    gross_profit INTEGER,               -- 毛利润 = 收入 - 原材料(千元)
    gross_margin REAL,                  -- 毛利率
    net_margin REAL,                    -- 净利率
    core_op_margin REAL                 -- 核心经营利润率
)
""")

# 注: 2022年收入为持续经营业务收入(已剔除特海)
c.execute("""
INSERT INTO annual_financials VALUES
(2022, 31038634, 29087006, 1280100, 662164, 144367, 0, 9364, 2117641, 1637306, NULL,
 31038634-12906400, NULL, NULL, NULL),
(2023, 41453348, 39612779, 1041475, 788651, 346176, 0, 10443, 5833072, 4495399, 5246494,
 41453348-16946200, NULL, NULL, NULL),
(2024, 42754687, 40880951, 1253869, 575140, 483335, 16706, 28021, 6624055, 4700278, 6229880,
 42754687-16211077, NULL, NULL, NULL),
(2025, 43225355, 39063629, 2657600, 535000, 1520600, 50000, 30000, 5811695, 4041885, 5403233,
 43225355-17526186, NULL, NULL, NULL)
""");

# 更新计算字段
c.execute("""
UPDATE annual_financials SET
    gross_margin = gross_profit * 1.0 / revenue,
    net_margin = net_profit * 1.0 / revenue,
    core_op_margin = core_operating_profit * 1.0 / revenue
""")

# 2022年核心经营利润缺失, 设为NULL
c.execute("UPDATE annual_financials SET core_operating_profit = NULL, core_op_margin = NULL WHERE year = 2022")

# ============================================================
# 2. 成本明细表
# ============================================================
c.execute("""
CREATE TABLE cost_breakdown (
    year INTEGER PRIMARY KEY,
    raw_materials INTEGER,       -- 原材料及易耗品成本(千元)
    raw_materials_pct REAL,      -- 占收入比
    staff_costs INTEGER,         -- 员工成本(千元)
    staff_costs_pct REAL,       -- 占收入比
    rentals INTEGER,             -- 租金及相关支出(千元)
    rentals_pct REAL,            -- 占收入比
    utilities INTEGER,           -- 水电开支(千元)
    utilities_pct REAL,          -- 占收入比
    depreciation INTEGER,        -- 折旧及摊销(千元)
    depreciation_pct REAL,       -- 占收入比
    travel_comm INTEGER,         -- 差旅及通讯开支(千元)
    travel_comm_pct REAL,       -- 占收入比
    other_expenses INTEGER,     -- 其他开支(千元)
    other_expenses_pct REAL,    -- 占收入比
    total_operating_costs INTEGER,  -- 经营成本合计(千元)
    total_cost_pct REAL          -- 经营成本占收入比
)
""")

c.execute("""
INSERT INTO cost_breakdown VALUES
(2022, 12906400, NULL, 10239800, NULL, 274300, NULL, 1048000, NULL, 3321200, NULL, 144600, NULL, 1361200, NULL, NULL, NULL),
(2023, 16946200, NULL, 13039800, NULL, 361900, NULL, 1374300, NULL, 2945400, NULL, 204300, NULL, 1611000, NULL, NULL, NULL),
(2024, 16211077, NULL, 14113263, NULL, 425543, NULL, 1465696, NULL, 2558496, NULL, 230000, NULL, 1700000, NULL, NULL, NULL),
(2025, 17526186, NULL, 14072970, NULL, 428606, NULL, 1475499, NULL, 2182061, NULL, 289372, NULL, 1900000, NULL, NULL, NULL)
""");

# 更新百分比和合计
c.execute("""
UPDATE cost_breakdown SET
    raw_materials_pct = raw_materials * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year),
    staff_costs_pct = staff_costs * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year),
    rentals_pct = rentals * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year),
    utilities_pct = utilities * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year),
    depreciation_pct = depreciation * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year),
    travel_comm_pct = travel_comm * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year),
    other_expenses_pct = other_expenses * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year)
""")

c.execute("""
UPDATE cost_breakdown SET
    total_operating_costs = raw_materials + staff_costs + rentals + utilities + depreciation + travel_comm + other_expenses,
    total_cost_pct = total_operating_costs * 1.0 / (SELECT revenue FROM annual_financials WHERE year = cost_breakdown.year)
""")

# ============================================================
# 3. 运营指标表
# ============================================================
c.execute("""
CREATE TABLE operational_metrics (
    year INTEGER PRIMARY KEY,
    total_restaurants INTEGER,       -- 海底捞餐厅总数
    self_operated INTEGER,           -- 自营餐厅数
    franchised INTEGER,              -- 加盟餐厅数
    table_turnover REAL,             -- 平均翻台率(次/天)
    same_store_turnover REAL,        -- 同店翻台率(次/天)
    avg_spending_per_guest REAL,     -- 顾客人均消费(元)
    customer_visits_million REAL,    -- 全年接待顾客(百万人次)
    system_sales_growth REAL,        -- 系统销售额增长率
    new_stores INTEGER,              -- 新开店数
    closed_stores INTEGER,           -- 关闭/搬迁店数
    employees INTEGER                -- 员工人数(估算)
)
""")

c.execute("""
INSERT INTO operational_metrics VALUES
(2022, 1371, 1371, 0, 3.0, 3.1, 104.9, 276.3, NULL, 24, 50, NULL),
(2023, 1374, 1374, 0, 3.8, 3.9, 99.1, 397.0, NULL, 9, 32, NULL),
(2024, 1368, 1355, 13, 4.1, NULL, 97.5, 415.0, 3.0, 62, 70, 154000),
(2025, 1383, 1304, 79, 3.9, NULL, 97.7, 383.9, -3.7, 79, 85, 143000)
""");

# ============================================================
# 4. 同店销售表 (仅2022-2023有数据)
# ============================================================
c.execute("""
CREATE TABLE same_store_sales (
    year INTEGER,
    region TEXT,
    store_count INTEGER,
    same_store_sales INTEGER,      -- 同店销售额(千元)
    avg_daily_sales REAL,         -- 同店平均日销售额(千元)
    same_store_turnover REAL,     -- 同店翻台率(次/天)
    PRIMARY KEY (year, region)
)
""")

c.execute("""
INSERT INTO same_store_sales VALUES
(2022, '一线城市', 113, 2905807, 79.1, 3.1),
(2022, '二线城市', 290, 7190558, 72.1, 3.1),
(2022, '三线及以下', 337, 8112525, 69.7, 3.1),
(2022, '港澳台', 19, 950609, 138.7, 3.6),
(2022, '整体', 759, 19159499, 73.8, 3.1),
(2023, '一线城市', 130, 4422588, 93.5, 4.1),
(2023, '二线城市', 346, 10649277, 84.7, 4.0),
(2023, '三线及以下', 455, 13094689, 79.1, 3.8),
(2023, '港澳台', 19, 1159425, 168.1, 4.2),
(2023, '整体', 950, 29325979, 84.9, 3.9)
""");

# ============================================================
# 5. 分城市等级运营指标表
# ============================================================
c.execute("""
CREATE TABLE city_tier_metrics (
    year INTEGER,
    city_tier TEXT,
    avg_spending REAL,      -- 人均消费(元)
    table_turnover REAL,   -- 翻台率(次/天)
    store_count INTEGER,   -- 餐厅数量
    revenue INTEGER,       -- 经营收入(千元)
    revenue_share REAL,    -- 收入占比
    PRIMARY KEY (year, city_tier)
)
""")

c.execute("""
INSERT INTO city_tier_metrics VALUES
(2022, '一线城市', 114.2, 3.0, 234, 5153936, 0.178),
(2022, '二线城市', 104.3, 3.0, 538, 11338523, 0.391),
(2022, '三线及以下', 97.9, 2.9, 577, 11465959, 0.395),
(2022, '港澳台', 197.4, 3.5, 22, 1032421, 0.036),
(2023, '一线城市', 105.7, 3.8, 232, 7195389, 0.183),
(2023, '二线城市', 98.3, 3.9, 538, 15610835, 0.397),
(2023, '三线及以下', 92.8, 3.6, 581, 15160451, 0.385),
(2023, '港澳台', 202.8, 4.2, 23, 1369938, 0.035)
""");

# ============================================================
# 6. 收入结构表 (按分部)
# ============================================================
c.execute("""
CREATE TABLE revenue_segments (
    year INTEGER,
    segment TEXT,
    revenue INTEGER,        -- 收入(千元)
    revenue_pct REAL,       -- 占比
    yoy_growth REAL,        -- 同比增长率
    PRIMARY KEY (year, segment)
)
""")

c.execute("""
INSERT INTO revenue_segments VALUES
(2022, '海底捞餐厅经营', 28942639, 0.933, NULL),
(2022, '外卖业务', 1280100, 0.041, NULL),
(2022, '调味品及食材', 662164, 0.021, NULL),
(2022, '其他餐厅经营', 144367, 0.005, NULL),
(2022, '其他', 9364, 0.000, NULL),
(2023, '海底捞餐厅经营', 39266603, 0.947, 0.357),
(2023, '外卖业务', 1041475, 0.025, -0.185),
(2023, '调味品及食材', 788651, 0.019, 0.191),
(2023, '其他餐厅经营', 346176, 0.008, 1.397),
(2023, '其他', 10443, 0.000, 0.115),
(2024, '海底捞餐厅经营', 40397616, 0.945, 0.029),
(2024, '外卖业务', 1253869, 0.029, 0.204),
(2024, '调味品及食材', 575140, 0.013, -0.271),
(2024, '其他餐厅经营', 483335, 0.011, 0.396),
(2024, '特许经营', 16706, 0.000, NULL),
(2024, '其他', 28021, 0.001, 1.681),
(2025, '海底捞餐厅经营', 37543000, 0.869, -0.071),
(2025, '外卖业务', 2657600, 0.062, 1.119),
(2025, '其他餐厅经营', 1520600, 0.035, 2.146),
(2025, '调味品及食材', 535000, 0.012, -0.070),
(2025, '特许经营', 50000, 0.001, 1.993),
(2025, '其他', 30000, 0.001, 0.070)
""");

conn.commit()
conn.close()
print("Database created successfully at:", DB_PATH)
