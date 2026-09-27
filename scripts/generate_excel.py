import sqlite3
import os
from openpyxl import Workbook
from openpyxl.chart import BarChart, BarChart3D, LineChart, PieChart, Reference, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "haidilao.db")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "reports", "excel", "海底捞经营分析报告.xlsx")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

wb = Workbook()

# ============================================================
# 样式定义
# ============================================================
HEADER_FILL = PatternFill(start_color="D32F2F", end_color="D32F2F", fill_type="solid")
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="微软雅黑", size=14, bold=True, color="D32F2F")
SUBTITLE_FONT = Font(name="微软雅黑", size=10, italic=True, color="666666")
DATA_FONT = Font(name="微软雅黑", size=10)
BOLD_FONT = Font(name="微软雅黑", size=10, bold=True)
WARN_FILL = PatternFill(start_color="FFF3E0", end_color="FFF3E0", fill_type="solid")
CRITICAL_FILL = PatternFill(start_color="FFEBEE", end_color="FFEBEE", fill_type="solid")
INFO_FILL = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")
THIN_BORDER = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC')
)
CENTER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT_ALIGN = Alignment(horizontal="left", vertical="center", wrap_text=True)

def style_header_row(ws, row, cols):
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER_ALIGN
        cell.border = THIN_BORDER

def style_data_cell(ws, row, col, bold=False, fill=None):
    cell = ws.cell(row=row, column=col)
    cell.font = BOLD_FONT if bold else DATA_FONT
    cell.alignment = CENTER_ALIGN
    cell.border = THIN_BORDER
    if fill:
        cell.fill = fill
    return cell

# ============================================================
# Sheet 1: 趋势分析
# ============================================================
ws1 = wb.active
ws1.title = "1-趋势分析"

ws1.merge_cells('A1:H1')
ws1['A1'] = "海底捞 2022-2025 年度趋势分析"
ws1['A1'].font = TITLE_FONT
ws1['A1'].alignment = CENTER_ALIGN
ws1.merge_cells('A2:H2')
ws1['A2'] = "数据来源: 海底捞国际控股有限公司 (06862.HK) 年度业绩公告 | 单位: 人民币千元"
ws1['A2'].font = SUBTITLE_FONT
ws1['A2'].alignment = CENTER_ALIGN

headers = ["年份", "总收入(千元)", "收入同比%", " " + "净利润(千元)", "净利润同比%", "核心经营利润(千元)", "核心经营利润同比%", "毛利率%"]
for i, h in enumerate(headers, 1):
    ws1.cell(row=4, column=i, value=h)
style_header_row(ws1, 4, len(headers))

c.execute("""
SELECT year, revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY year)) * 100.0 / LAG(revenue) OVER (ORDER BY year), 2),
    net_profit,
    ROUND((net_profit - LAG(net_profit) OVER (ORDER BY year)) * 100.0 / LAG(net_profit) OVER (ORDER BY year), 2),
    core_operating_profit,
    CASE WHEN LAG(core_operating_profit) OVER (ORDER BY year) IS NOT NULL
         THEN ROUND((core_operating_profit - LAG(core_operating_profit) OVER (ORDER BY year)) * 100.0 / LAG(core_operating_profit) OVER (ORDER BY year), 2)
    END,
    ROUND(gross_margin * 100, 2)
FROM annual_financials ORDER BY year
""")
rows = c.fetchall()
for i, row in enumerate(rows, 5):
    for j, val in enumerate(row, 1):
        cell = style_data_cell(ws1, i, j)
        if val is not None:
            cell.value = val
        else:
            cell.value = "N/A"
        if j in (3, 5, 7, 8) and val is not None:
            cell.number_format = '0.00"%"'

# 收入与利润趋势图
chart1 = LineChart()
chart1.title = "收入与利润趋势 (2022-2025)"
chart1.style = 2
chart1.y_axis.title = "金额 (千元)"
chart1.x_axis.title = "年份"
chart1.height = 10
chart1.width = 20

data = Reference(ws1, min_col=2, min_row=4, max_col=2, max_row=8)
chart1.add_data(data, titles_from_data=True)
data2 = Reference(ws1, min_col=4, min_row=4, max_col=4, max_row=8)
chart1.add_data(data2, titles_from_data=True)
data3 = Reference(ws1, min_col=6, min_row=4, max_col=6, max_row=8)
chart1.add_data(data3, titles_from_data=True)
cats = Reference(ws1, min_col=1, min_row=5, max_row=8)
chart1.set_categories(cats)
chart1.dataLabels = DataLabelList(showVal=True)
ws1.add_chart(chart1, "A11")

# 毛利率趋势图
chart2 = LineChart()
chart2.title = "毛利率趋势 (%)"
chart2.style = 3
chart2.y_axis.title = "毛利率 (%)"
chart2.x_axis.title = "年份"
chart2.height = 8
chart2.width = 20
data_gm = Reference(ws1, min_col=8, min_row=4, max_col=8, max_row=8)
chart2.add_data(data_gm, titles_from_data=True)
chart2.set_categories(cats)
chart2.dataLabels = DataLabelList(showVal=True)
ws1.add_chart(chart2, "A32")

# ============================================================
# Sheet 2: 运营指标
# ============================================================
ws2 = wb.create_sheet("2-运营指标")

ws2.merge_cells('A1:I1')
ws2['A1'] = "关键运营指标趋势分析"
ws2['A1'].font = TITLE_FONT
ws2['A1'].alignment = CENTER_ALIGN

headers2 = ["年份", "餐厅总数", "自营门店", "加盟门店", "翻台率(次/天)", "同店翻台率", "人均消费(元)", "顾客人次(百万)", "系统销售增长%"]
for i, h in enumerate(headers2, 1):
    ws2.cell(row=3, column=i, value=h)
style_header_row(ws2, 3, len(headers2))

c.execute("""
SELECT year, total_restaurants, self_operated, franchised, table_turnover, same_store_turnover,
    avg_spending_per_guest, customer_visits_million, system_sales_growth
FROM operational_metrics ORDER BY year
""")
rows2 = c.fetchall()
for i, row in enumerate(rows2, 3 + 1):
    for j, val in enumerate(row, 1):
        cell = style_data_cell(ws2, i, j)
        if val is not None:
            cell.value = val
        else:
            cell.value = "N/A"

# 翻台率与客流趋势图
chart3 = BarChart()
chart3.title = "翻台率与客流变化"
chart3.style = 2
chart3.y_axis.title = "翻台率 (次/天)"
chart3.x_axis.title = "年份"
chart3.height = 10
chart3.width = 20
data_to = Reference(ws2, min_col=5, min_row=3, max_col=5, max_row=7)
chart3.add_data(data_to, titles_from_data=True)
cats2 = Reference(ws2, min_col=1, min_row=4, max_row=7)
chart3.set_categories(cats2)
chart3.dataLabels = DataLabelList(showVal=True)
ws2.add_chart(chart3, "A10")

# 门店数量变化图
chart4 = BarChart()
chart4.type = "col"
chart4.grouping = "stacked"
chart4.title = "门店数量变化 (自营+加盟)"
chart4.style = 3
chart4.y_axis.title = "门店数"
chart4.x_axis.title = "年份"
chart4.height = 8
chart4.width = 20
data_stores = Reference(ws2, min_col=3, min_row=3, max_col=4, max_row=7)
chart4.add_data(data_stores, titles_from_data=True)
chart4.set_categories(cats2)
chart4.dataLabels = DataLabelList(showVal=True)
ws2.add_chart(chart4, "A30")

# 人均消费趋势
chart5 = LineChart()
chart5.title = "顾客人均消费趋势 (元)"
chart5.style = 4
chart5.y_axis.title = "人均消费 (元)"
chart5.x_axis.title = "年份"
chart5.height = 8
chart5.width = 20
data_spend = Reference(ws2, min_col=7, min_row=3, max_col=7, max_row=7)
chart5.add_data(data_spend, titles_from_data=True)
chart5.set_categories(cats2)
chart5.dataLabels = DataLabelList(showVal=True)
ws2.add_chart(chart5, "A50")

# ============================================================
# Sheet 3: 成本结构
# ============================================================
ws3 = wb.create_sheet("3-成本结构")

ws3.merge_cells('A1:J1')
ws3['A1'] = "成本结构拆解 (2022-2025)"
ws3['A1'].font = TITLE_FONT
ws3['A1'].alignment = CENTER_ALIGN

headers3 = ["年份", "原材料(千元)", "原材料占比%", "员工成本(千元)", "员工占比%", "租金(千元)", "租金占比%", "折旧摊销(千元)", "折旧占比%", "其他(千元)"]
for i, h in enumerate(headers3, 1):
    ws3.cell(row=3, column=i, value=h)
style_header_row(ws3, 3, len(headers3))

c.execute("""
SELECT year, raw_materials, ROUND(raw_materials_pct*100,2), staff_costs, ROUND(staff_costs_pct*100,2),
    rentals, ROUND(rentals_pct*100,2), depreciation, ROUND(depreciation_pct*100,2), other_expenses
FROM cost_breakdown ORDER BY year
""")
rows3 = c.fetchall()
for i, row in enumerate(rows3, 3 + 1):
    for j, val in enumerate(row, 1):
        cell = style_data_cell(ws3, i, j)
        cell.value = val

# 成本占比堆叠柱图
chart6 = BarChart()
chart6.type = "col"
chart6.grouping = "percentStacked"
chart6.title = "成本结构占比变化"
chart6.style = 2
chart6.y_axis.title = "占比"
chart6.x_axis.title = "年份"
chart6.height = 12
chart6.width = 22
data_cost = Reference(ws3, min_col=2, min_row=3, max_col=2, max_row=7)
chart6.add_data(data_cost, titles_from_data=True)
data_cost2 = Reference(ws3, min_col=4, min_row=3, max_col=4, max_row=7)
chart6.add_data(data_cost2, titles_from_data=True)
data_cost3 = Reference(ws3, min_col=6, min_row=3, max_col=6, max_row=7)
chart6.add_data(data_cost3, titles_from_data=True)
data_cost4 = Reference(ws3, min_col=8, min_row=3, max_col=8, max_row=7)
chart6.add_data(data_cost4, titles_from_data=True)
data_cost5 = Reference(ws3, min_col=10, min_row=3, max_col=10, max_row=7)
chart6.add_data(data_cost5, titles_from_data=True)
cats3 = Reference(ws3, min_col=1, min_row=4, max_row=7)
chart6.set_categories(cats3)
ws3.add_chart(chart6, "A10")

# 原材料成本变化趋势
chart7 = LineChart()
chart7.title = "原材料成本与占比趋势"
chart7.style = 3
chart7.y_axis.title = "金额 (千元)"
chart7.x_axis.title = "年份"
chart7.height = 8
chart7.width = 22
data_raw = Reference(ws3, min_col=2, min_row=3, max_col=2, max_row=7)
chart7.add_data(data_raw, titles_from_data=True)
chart7.set_categories(cats3)
chart7.dataLabels = DataLabelList(showVal=True)
ws3.add_chart(chart7, "A35")

# ============================================================
# Sheet 4: 利润桥 (瀑布图模拟)
# ============================================================
ws4 = wb.create_sheet("4-利润桥分析")

ws4.merge_cells('A1:E1')
ws4['A1'] = "核心经营利润变化桥分析 (2024 → 2025)"
ws4['A1'].font = TITLE_FONT
ws4['A1'].alignment = CENTER_ALIGN
ws4.merge_cells('A2:E2')
ws4['A2'] = "单位: 千元 | 正数=利润增加贡献, 负数=利润减少因素"
ws4['A2'].font = SUBTITLE_FONT
ws4['A2'].alignment = CENTER_ALIGN

# 瀑布图数据
waterfall_data = [
    ("2024年核心经营利润", 6229880, "base"),
    ("收入增长", 470668, "positive"),
    ("原材料成本增加", -1315109, "negative"),
    ("员工成本下降", 40293, "positive"),
    ("折旧摊销减少", 376435, "positive"),
    ("其他成本增加", -272238, "negative"),
    ("2025年核心经营利润", 5403233, "base"),
]

ws4.cell(row=4, column=1, value="项目")
ws4.cell(row=4, column=2, value="金额(千元)")
ws4.cell(row=4, column=3, value="类型")
ws4.cell(row=4, column=4, value="累计影响")
style_header_row(ws4, 4, 4)

cumulative = 0
for i, (label, val, typ) in enumerate(waterfall_data, 5):
    ws4.cell(row=i, column=1, value=label).font = DATA_FONT
    ws4.cell(row=i, column=1).alignment = LEFT_ALIGN
    ws4.cell(row=i, column=1).border = THIN_BORDER
    cell2 = ws4.cell(row=i, column=2, value=val)
    cell2.font = BOLD_FONT if typ == "base" else DATA_FONT
    cell2.alignment = CENTER_ALIGN
    cell2.border = THIN_BORDER
    cell3 = ws4.cell(row=i, column=3, value=typ)
    cell3.alignment = CENTER_ALIGN
    cell3.border = THIN_BORDER
    if typ == "negative":
        cell2.fill = CRITICAL_FILL
        cell3.fill = CRITICAL_FILL
    elif typ == "positive":
        cell2.fill = INFO_FILL
        cell3.fill = INFO_FILL
    else:
        cell2.fill = HEADER_FILL
        cell2.font = HEADER_FONT
        cell3.fill = HEADER_FILL
        cell3.font = HEADER_FONT

    if typ == "base":
        cumulative = val
    else:
        cumulative += val
    cell4 = ws4.cell(row=i, column=4, value=cumulative)
    cell4.font = BOLD_FONT
    cell4.alignment = CENTER_ALIGN
    cell4.border = THIN_BORDER

# 利润桥柱状图
chart8 = BarChart()
chart8.type = "col"
chart8.title = "核心经营利润变化桥 (2024→2025)"
chart8.style = 2
chart8.y_axis.title = "金额 (千元)"
chart8.x_axis.title = "驱动因素"
chart8.height = 12
chart8.width = 24
data_wf = Reference(ws4, min_col=2, min_row=4, max_col=2, max_row=11)
chart8.add_data(data_wf, titles_from_data=True)
cats_wf = Reference(ws4, min_col=1, min_row=5, max_row=11)
chart8.set_categories(cats_wf)
chart8.dataLabels = DataLabelList(showVal=True)
ws4.add_chart(chart8, "F4")

# ============================================================
# Sheet 5: 收入结构
# ============================================================
ws5 = wb.create_sheet("5-收入结构")

ws5.merge_cells('A1:F1')
ws5['A1'] = "收入结构拆解 (2022-2025)"
ws5['A1'].font = TITLE_FONT
ws5['A1'].alignment = CENTER_ALIGN

headers5 = ["年份", "海底捞餐厅经营(千元)", "外卖业务(千元)", "调味品及食材(千元)", "其他餐厅(千元)", "特许经营(千元)"]
for i, h in enumerate(headers5, 1):
    ws5.cell(row=3, column=i, value=h)
style_header_row(ws5, 3, len(headers5))

c.execute("""
SELECT year,
    SUM(CASE WHEN segment='海底捞餐厅经营' THEN revenue END) AS haidilao,
    SUM(CASE WHEN segment='外卖业务' THEN revenue END) AS delivery,
    SUM(CASE WHEN segment='调味品及食材' THEN revenue END) AS condiment,
    SUM(CASE WHEN segment='其他餐厅经营' THEN revenue END) AS other_rest,
    SUM(CASE WHEN segment='特许经营' THEN revenue END) AS franchise
FROM revenue_segments GROUP BY year ORDER BY year
""")
rows5 = c.fetchall()
for i, row in enumerate(rows5, 3 + 1):
    for j, val in enumerate(row, 1):
        cell = style_data_cell(ws5, i, j)
        cell.value = val if val else 0

# 收入结构堆叠柱图
chart9 = BarChart()
chart9.type = "col"
chart9.grouping = "stacked"
chart9.title = "收入结构变化 (按分部)"
chart9.style = 2
chart9.y_axis.title = "金额 (千元)"
chart9.x_axis.title = "年份"
chart9.height = 12
chart9.width = 22
data_rev = Reference(ws5, min_col=2, min_row=3, max_col=6, max_row=7)
chart9.add_data(data_rev, titles_from_data=True)
cats5 = Reference(ws5, min_col=1, min_row=4, max_row=7)
chart9.set_categories(cats5)
ws5.add_chart(chart9, "A10")

# 外卖收入增长图
chart10 = LineChart()
chart10.title = "外卖业务收入爆发式增长"
chart10.style = 3
chart10.y_axis.title = "收入 (千元)"
chart10.x_axis.title = "年份"
chart10.height = 8
chart10.width = 22
data_del = Reference(ws5, min_col=3, min_row=3, max_col=3, max_row=7)
chart10.add_data(data_del, titles_from_data=True)
chart10.set_categories(cats5)
chart10.dataLabels = DataLabelList(showVal=True)
ws5.add_chart(chart10, "A35")

# ============================================================
# Sheet 6: 同店分析
# ============================================================
ws6 = wb.create_sheet("6-同店分析")

ws6.merge_cells('A1:G1')
ws6['A1'] = "同店销售分析 (2022 vs 2023)"
ws6['A1'].font = TITLE_FONT
ws6['A1'].alignment = CENTER_ALIGN

headers6 = ["区域", "2022同店数", "2023同店数", "同店销售额变动(千元)", "同店增长%", "日均销售额变动(千元)", "翻台率变动"]
for i, h in enumerate(headers6, 1):
    ws6.cell(row=3, column=i, value=h)
style_header_row(ws6, 3, len(headers6))

c.execute("""
SELECT a.region, a.store_count, b.store_count,
    b.same_store_sales - a.same_store_sales,
    ROUND((b.same_store_sales - a.same_store_sales) * 100.0 / a.same_store_sales, 2),
    ROUND(b.avg_daily_sales - a.avg_daily_sales, 2),
    ROUND(b.same_store_turnover - a.same_store_turnover, 2)
FROM same_store_sales a
JOIN same_store_sales b ON a.region = b.region AND b.year = 2023
WHERE a.year = 2022
ORDER BY a.region
""")
rows6 = c.fetchall()
for i, row in enumerate(rows6, 3 + 1):
    for j, val in enumerate(row, 1):
        cell = style_data_cell(ws6, i, j)
        cell.value = val

chart11 = BarChart()
chart11.type = "col"
chart11.title = "各区域同店销售增长率 (%)"
chart11.style = 3
chart11.y_axis.title = "增长率 (%)"
chart11.x_axis.title = "区域"
chart11.height = 10
chart11.width = 20
data_ss = Reference(ws6, min_col=5, min_row=3, max_col=5, max_row=3 + len(rows6))
chart11.add_data(data_ss, titles_from_data=True)
cats6 = Reference(ws6, min_col=1, min_row=4, max_row=3 + len(rows6))
chart11.set_categories(cats6)
chart11.dataLabels = DataLabelList(showVal=True)
ws6.add_chart(chart11, "A10")

# ============================================================
# Sheet 7: 改善方向排序
# ============================================================
ws7 = wb.create_sheet("7-改善方向排序")

ws7.merge_cells('A1:F1')
ws7['A1'] = "经营改善方向 (按影响程度排序)"
ws7['A1'].font = TITLE_FONT
ws7['A1'].alignment = CENTER_ALIGN
ws7.merge_cells('A2:F2')
ws7['A2'] = "基于2024→2025年利润变动归因分析, 按对核心经营利润的影响金额排序"
ws7['A2'].font = SUBTITLE_FONT
ws7['A2'].alignment = CENTER_ALIGN

headers7 = ["排序", "改善方向", "影响金额(千元)", "影响程度", "严重级别", "建议行动"]
for i, h in enumerate(headers7, 1):
    ws7.cell(row=4, column=i, value=h)
style_header_row(ws7, 4, len(headers7))

improvements = [
    (1, "控制原材料成本占比", -1315109, "原材料成本增13.15亿, 占比从37.9%升至40.5%", "CRITICAL",
     "1.优化供应链集中采购 2.推动区域特色产品本地化降本 3.菜单结构优化(高毛利产品占比提升)"),
    (2, "提升翻台率至4.0+", -470668 - 272238 + 376435 + 40293, "翻台率降0.2次致客流减3110万, 餐厅收入降18.17亿", "CRITICAL",
     "1.深化'一店一策'差异化运营 2.强化夜间时段和宵夜场景 3.优化排队体验提升翻台效率"),
    (3, "恢复客流增长", 0, "全年客流3.839亿, 同比减少3110万人次(-7.5%)", "WARN",
     "1.加大年轻客群触达(短视频/IP联名) 2.提升会员复购率 3.校园/家庭场景创新"),
    (4, "优化门店网络质量", 0, "自营门店净减51家(关停85家), 门店效率待提升", "WARN",
     "1.持续淘汰低效门店 2.加盟模式加速下沉市场扩张 3.门店改造升级提升单店产出"),
    (5, "扩大外卖业务规模", 1403700, "外卖收入增14.04亿(+111.9%), 但利润率待提升", "INFO",
     "1.扩大外卖覆盖至全部门店 2.开发外卖专属产品提升利润率 3.多平台深度合作"),
    (6, "加速多品牌矩阵", 1037300, "石榴计划20品牌207店, 其他餐厅收入增10.37亿", "INFO",
     "1.加快'厨师'和'人民餐厅'双体系孵化 2.共享中后台降低新品牌成本 3.择优收购互补品牌"),
]

for i, (rank, direction, amount, impact, severity, action) in enumerate(improvements, 5):
    ws7.cell(row=i, column=1, value=rank).font = BOLD_FONT
    ws7.cell(row=i, column=1).alignment = CENTER_ALIGN
    ws7.cell(row=i, column=2, value=direction).font = BOLD_FONT
    ws7.cell(row=i, column=2).alignment = LEFT_ALIGN
    cell_amt = ws7.cell(row=i, column=3, value=amount if amount != 0 else "—")
    cell_amt.alignment = CENTER_ALIGN
    cell_imp = ws7.cell(row=i, column=4, value=impact)
    cell_imp.alignment = LEFT_ALIGN
    cell_sev = ws7.cell(row=i, column=5, value=severity)
    cell_sev.alignment = CENTER_ALIGN
    cell_act = ws7.cell(row=i, column=6, value=action)
    cell_act.alignment = LEFT_ALIGN

    for col in range(1, 7):
        ws7.cell(row=i, column=col).border = THIN_BORDER
        ws7.cell(row=i, column=col).font = DATA_FONT if col != 1 else BOLD_FONT

    if severity == "CRITICAL":
        ws7.cell(row=i, column=5).fill = CRITICAL_FILL
    elif severity == "WARN":
        ws7.cell(row=i, column=5).fill = WARN_FILL
    else:
        ws7.cell(row=i, column=5).fill = INFO_FILL

for col in range(1, 7):
    ws7.column_dimensions[get_column_letter(col)].width = [8, 22, 18, 40, 12, 55][col-1]

# ============================================================
# Sheet 8: 原始数据
# ============================================================
ws8 = wb.create_sheet("8-原始数据")
ws8.merge_cells('A1:C1')
ws8['A1'] = "数据来源说明"
ws8['A1'].font = TITLE_FONT
ws8['A1'].alignment = CENTER_ALIGN

sources = [
    ("数据来源", "海底捞国际控股有限公司 (06862.HK) 年度业绩公告", ""),
    ("2022年报", "https://www.hkexnews.hk/listedco/listconews/sehk/2023/0330/2023033001797_c.pdf", "持续经营业务"),
    ("2023年报", "https://www.hkexnews.hk/listedco/listconews/sehk/2024/0326/2024032601044_c.pdf", "持续经营业务"),
    ("2024年报", "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0325/2025032501303.pdf", ""),
    ("2025年报", "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0324/2026032400912.pdf", ""),
    ("", "", ""),
    ("注意", "2022年起特海国际(海外业务)分拆上市, 不再纳入合并报表", ""),
    ("注意", "2024年差旅通讯及其他开支为估算值", ""),
    ("注意", "2025年分部收入中部分项目为估算", ""),
    ("分析工具", "SQLite + SQL 查询", ""),
    ("可视化", "openpyxl (Excel)", ""),
    ("分析方法", "经营分析全链路 Skill (business-ops-analysis)", ""),
]

for i, (label, value, note) in enumerate(sources, 3):
    ws8.cell(row=i, column=1, value=label).font = BOLD_FONT
    ws8.cell(row=i, column=1).alignment = LEFT_ALIGN
    ws8.cell(row=i, column=2, value=value).font = DATA_FONT
    ws8.cell(row=i, column=2).alignment = LEFT_ALIGN
    ws8.cell(row=i, column=3, value=note).font = DATA_FONT
    ws8.cell(row=i, column=3).alignment = LEFT_ALIGN

ws8.column_dimensions['A'].width = 15
ws8.column_dimensions['B'].width = 80
ws8.column_dimensions['C'].width = 20

# ============================================================
# 保存
# ============================================================
conn.close()
wb.save(OUTPUT_PATH)
print(f"Excel report saved to: {OUTPUT_PATH}")
