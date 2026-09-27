# 海底捞经营分析与翻台率提升策略

> 基于 2022-2025 年年度财报数据，通过 SQL 分析 + Excel 可视化 + HTML 交互报告，完成海底捞（06862.HK）经营全链路分析，并输出可执行的翻台率提升运营策略方案。

## 项目解决什么问题

海底捞 2025 年核心经营利润同比下降 13.3%，翻台率从 4.1 降至 3.9 次/天，为近三年首次下降。本项目通过财报数据驱动的分析方法，解决两个核心问题：

1. **利润为什么下降？** — 从收入、成本、运营指标三个维度拆解利润变动归因，识别原材料成本攀升（-13.15 亿）和客流流失（-3110 万人次）为主要拖累因素
2. **翻台率怎么提升？** — 基于 5 大根因诊断，输出 "5+1" 策略体系（分时段运营、排队效率、产品优化、客流引流、门店运营 + 组织保障），90 天内将翻台率从 3.9 提升至 4.1+，预计年化增量收入约 12 亿元

## 主要功能

### 数据层
- **SQLite 数据库**：6 张表覆盖年度财务、成本明细、运营指标、同店销售、城市等级、收入结构
- **SQL 查询引擎**：7 类分析查询，含同比/环比趋势、成本结构拆解、利润桥归因、同店对比、异常识别

### 分析层
- **趋势分析**：收入增速从 +33.6% 衰减至 +1.1%，利润拐点确认
- **结构拆解**：翻台率(-0.2)、客流(-7.5%)、门店(-51 家)、客单价对收入的贡献归因
- **成本归因**：原材料占比从 37.9% 升至 40.5%，侵蚀毛利 8.44 亿元；折旧下降贡献 +3.76 亿元
- **利润桥**：2024→2025 核心经营利润变动 8.27 亿元的逐项分解
- **异常识别**：3 个 CRITICAL + 3 个 WARN + 2 个 INFO 问题分级清单
- **翻台率策略**：根因诊断 → "5+1" 策略 → 90 天路线图 → 效果测算 → 风险矩阵

### 可视化层
- **Excel 报表**：经营分析报告（8 Sheet / 11 图表）+ 翻台率执行方案（6 Sheet / KPI 看板）
- **HTML 报告**：经营分析报告（7 个 ECharts 交互图表）+ 翻台率策略报告（6 个 ECharts 图表）

## 项目结构

```
haidilao-ops-analysis/
├── README.md                              # 项目说明
├── ARCHITECTURE.md                        # 架构与方法论文档
├── requirements.txt                       # Python 依赖
├── .gitignore
├── scripts/                               # Python 分析脚本
│   ├── create_database.py                 # SQLite 建表 + 数据导入
│   ├── run_analysis.py                    # SQL 分析查询（7 类查询）
│   ├── generate_excel.py                  # 经营分析 Excel 报表生成
│   └── generate_strategy_excel.py         # 翻台率策略 Excel 执行方案生成
├── data/                                  # 数据文件
│   └── haidilao.db                        # SQLite 数据库（6 张表）
├── reports/                               # 交付物
│   ├── excel/                             # Excel 可视化报表
│   │   ├── 海底捞经营分析报告.xlsx          # 8 Sheet / 11 图表
│   │   └── 翻台率提升执行方案.xlsx          # 6 Sheet / KPI 看板
│   └── html/                              # HTML 交互报告
│       ├── haidilao-ops-report/            # 经营分析报告（7 ECharts 图表）
│       │   ├── haidilao-ops-report.html
│       │   ├── assets/charts.js
│       │   └── _shared/js/echarts.min.js
│       └── turnover-strategy/             # 翻台率策略报告（6 ECharts 图表）
│           ├── turnover-strategy.html
│           ├── assets/charts.js
│           └── _shared/js/echarts.min.js
└── docs/                                  # 文档目录
```

## 使用方法

### 环境要求

- Python 3.8+
- 依赖：`sqlite3`（标准库）、`openpyxl`

### 安装

```bash
git clone https://github.com/<your-username>/haidilao-ops-analysis.git
cd haidilao-ops-analysis
pip install -r requirements.txt
```

### 运行分析

```bash
# 1. 创建数据库并导入财报数据
python scripts/create_database.py

# 2. 运行 SQL 分析查询（输出到终端）
python scripts/run_analysis.py

# 3. 生成经营分析 Excel 报表
python scripts/generate_excel.py

# 4. 生成翻台率策略 Excel 执行方案
python scripts/generate_strategy_excel.py
```

### 查看报告

- **Excel 报表**：打开 `reports/excel/` 下的 `.xlsx` 文件
- **HTML 报告**：在浏览器中打开 `reports/html/` 下的 `.html` 文件（含交互式图表）

## 结果示例

### 核心发现：利润桥分析（2024 → 2025）

| 驱动因素 | 影响金额（亿元） | 方向 |
|---|---|---|
| 收入增长 | +4.71 | 正向 |
| 原材料成本增加 | **-13.15** | **最大拖累** |
| 员工成本下降 | +0.40 | 正向 |
| 折旧摊销减少 | +3.76 | 正向 |
| 其他成本增加 | -2.72 | 负向 |
| **核心经营利润变动** | **-8.27** | — |

### 翻台率提升 "5+1" 策略

| 策略 | 提升（次/天） | 优先级 | 增量收入（亿/年） |
|---|---|---|---|
| 分时段精细化运营 | +0.06 | P0 | 3.5 |
| 排队体验与翻台效率 | +0.05 | P0 | 2.8 |
| 产品与菜单优化 | +0.04 | P1 | 2.2 |
| 客流引流与会员复购 | +0.04 | P1 | 2.5 |
| 门店差异化运营 | +0.01 | P2 | 1.0 |
| **合计** | **+0.20** | — | **12.0** |

## 数据来源

所有财务数据来自海底捞国际控股有限公司（06862.HK）在香港联交所发布的年度业绩公告：

| 年度 | 来源 |
|---|---|
| 2022 | [HKExNews 2023-03-30](https://www.hkexnews.hk/listedco/listconews/sehk/2023/0330/2023033001797_c.pdf) |
| 2023 | [HKExNews 2024-03-26](https://www.hkexnews.hk/listedco/listconews/sehk/2024/0326/2024032601044_c.pdf) |
| 2024 | [HKExNews 2025-03-25](https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0325/2025032501303.pdf) |
| 2025 | [HKExNews 2026-03-24](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0324/2026032400912.pdf) |

> 注：2022 年起特海国际（海外业务）分拆上市，不再纳入合并报表。2022 年收入为持续经营业务收入。

## 分析方法

采用 **经营分析全链路 Skill（business-ops-analysis）** 的标准工作流：

```
数据理解 → 趋势分析 → 结构拆解 → 异常识别 → 合成报告 → 交付渲染
```

- **置信度框架**：高（多视角交叉印证）/ 中（单一视角 + 数据充分）/ [待验证]（数据不足）
- **可视化优先**：能用图表说清楚的不堆文字
- **事实与推断分离**：明确区分"数据事实"与"分析推断"

详见 [ARCHITECTURE.md](./ARCHITECTURE.md)

## 技术栈

| 层 | 工具 | 用途 |
|---|---|---|
| 数据存储 | SQLite | 6 张表存储年度财务、成本、运营指标 |
| 查询分析 | SQL | 7 类分析查询（趋势、结构、归因、异常） |
| 数据可视化 | openpyxl (Excel) | 14 个 Sheet / 11+ 个原生 Excel 图表 |
| 交互报告 | HTML + ECharts | 13 个交互式图表（折线/柱图/瀑布/雷达/甘特） |
| 分析方法 | business-ops-analysis Skill | 经营分析全链路标准工作流 |

## License

MIT License - 本项目仅供学习和研究使用，不构成任何投资建议。
