import os
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, RadarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(PROJECT_ROOT, "reports", "excel", "翻台率提升执行方案.xlsx")

wb = Workbook()

# ===== 样式 =====
HF = PatternFill(start_color="0969DA", end_color="0969DA", fill_type="solid")
HFt = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
TF = Font(name="微软雅黑", size=14, bold=True, color="0550AE")
SF = Font(name="微软雅黑", size=10, italic=True, color="6A737D")
DF = Font(name="微软雅黑", size=10)
BF = Font(name="微软雅黑", size=10, bold=True)
TB = Border(
    left=Side(style='thin', color='D0D7DE'),
    right=Side(style='thin', color='D0D7DE'),
    top=Side(style='thin', color='D0D7DE'),
    bottom=Side(style='thin', color='D0D7DE')
)
CA = Alignment(horizontal="center", vertical="center", wrap_text=True)
LA = Alignment(horizontal="left", vertical="center", wrap_text=True)
RED = PatternFill(start_color="FFEBEE", end_color="FFEBEE", fill_type="solid")
YEL = PatternFill(start_color="FFF8E1", end_color="FFF8E1", fill_type="solid")
GRN = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")
BLU = PatternFill(start_color="E3F2FD", end_color="E3F2FD", fill_type="solid")

def hdr(ws, row, cols):
    for c in range(1, cols+1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HF; cell.font = HFt; cell.alignment = CA; cell.border = TB

def data(ws, r, c, val, bold=False, fill=None, fmt=None):
    cell = ws.cell(row=r, column=c, value=val)
    cell.font = BF if bold else DF
    cell.alignment = CA
    cell.border = TB
    if fill: cell.fill = fill
    if fmt: cell.number_format = fmt
    return cell

# ============================================================
# Sheet 1: 策略总览
# ============================================================
ws1 = wb.active
ws1.title = "1-策略总览"
ws1.merge_cells('A1:G1')
ws1['A1'] = "海底捞翻台率提升策略总览"
ws1['A1'].font = TF; ws1['A1'].alignment = CA
ws1.merge_cells('A2:G2')
ws1['A2'] = "目标：翻台率从3.9提升至4.1次/天 (+0.2) | 周期：90天 | 覆盖：1,304家自营门店"
ws1['A2'].font = SF; ws1['A2'].alignment = CA

headers = ["排序", "策略名称", "对应根因", "提升幅度(次/天)", "优先级", "见效周期", "预计增量收入(亿/年)"]
for i, h in enumerate(headers, 1):
    ws1.cell(row=4, column=i, value=h)
hdr(ws1, 4, len(headers))

rows = [
    (1, "分时段精细化运营", "午市利用不足", 0.06, "P0", "30天", 3.5),
    (2, "排队体验与翻台效率", "排队流失", 0.05, "P0", "30天", 2.8),
    (3, "产品与菜单优化", "用餐时长增加", 0.04, "P1", "60天", 2.2),
    (4, "客流引流与会员复购", "客流流失", 0.04, "P1", "60天", 2.5),
    (5, "门店差异化运营", "门店关停影响", 0.01, "P2", "90天", 1.0),
]
fills = [RED, RED, YEL, YEL, BLU]
for i, (rank, name, cause, lift, pri, cycle, rev) in enumerate(rows, 5):
    data(ws1, i, 1, rank, bold=True)
    data(ws1, i, 2, name)
    data(ws1, i, 3, cause)
    data(ws1, i, 4, lift, fill=GRN, fmt='0.00')
    data(ws1, i, 5, pri, fill=fills[i-5])
    data(ws1, i, 6, cycle)
    data(ws1, i, 7, rev, fmt='0.0')

data(ws1, 10, 1, "合计", bold=True, fill=PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid"))
ws1.cell(row=10, column=1).font = HFt
for c in range(2, 8):
    cell = ws1.cell(row=10, column=c)
    cell.fill = PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid")
    cell.font = HFt; cell.border = TB; cell.alignment = CA
ws1.cell(row=10, column=4, value=0.20).number_format = '0.00'
ws1.cell(row=10, column=7, value=12.0).number_format = '0.0'

for col, w in enumerate([6, 22, 16, 16, 8, 10, 18], 1):
    ws1.column_dimensions[get_column_letter(col)].width = w

# ============================================================
# Sheet 2: 详细行动计划
# ============================================================
ws2 = wb.create_sheet("2-详细行动计划")
ws2.merge_cells('A1:H1')
ws2['A1'] = "翻台率提升详细行动计划"
ws2['A1'].font = TF; ws2['A1'].alignment = CA

h2 = ["策略", "行动项", "具体措施", "负责部门", "启动日", "完成日", "里程碑指标", "状态"]
for i, h in enumerate(h2, 1):
    ws2.cell(row=3, column=i, value=h)
hdr(ws2, 3, len(h2))

actions = [
    # 策略1: 分时段运营
    ("分时段运营", "智能排号系统", "小程序远程排号+AI精准预估等位时间，200家旗舰店试点", "数字化中心", "D1", "D10", "排号系统上线率100%", ""),
    ("分时段运营", "午市工作日套餐", "68/88元两档套餐(30分钟上齐)，全门店推广", "产品研发部", "D5", "D20", "午市套餐渗透率40%+", ""),
    ("分时段运营", "午市时段延长", "提前开门30分钟+延后收午市30分钟", "运营部", "D1", "D10", "午市时段从3h扩至4h", ""),
    ("分时段运营", "写字楼定向营销", "3公里内写字楼专属券(满100减30)+企业团餐合作", "市场营销部", "D10", "D25", "合作企业50+", ""),
    ("分时段运营", "下午茶场景", "58元下午茶套餐(甜品+饮品)，闺蜜/商务场景", "产品研发部", "D20", "D40", "下午茶日均2桌+", ""),
    ("分时段运营", "宵夜专属菜单", "烤串+啤酒+小龙虾品类，客单60-80元", "产品研发部", "D15", "D30", "宵夜菜单上线50店", ""),
    ("分时段运营", "深夜食堂试点", "50家门店周五/周六24小时营业", "运营部", "D21", "D30", "24h门店50家", ""),
    ("分时段运营", "演唱会赛事引流", "与演出场馆合作，凭票根宵夜8折", "市场营销部", "D20", "D35", "合作场馆10+", ""),
    # 策略2: 排队效率
    ("排队效率", "等位送菜机制", "等位每15分钟送1道菜(价值15-20元)", "运营部", "D1", "D10", "等位流失率<15%", ""),
    ("排队效率", "等位预点餐", "排队时扫码点餐，入座即上锅底", "数字化中心", "D5", "D15", "预点餐率60%+", ""),
    ("排队效率", "等位娱乐矩阵", "美甲+桌游+零食饮料台标准化", "运营部", "D1", "D15", "全门店覆盖", ""),
    ("排队效率", "三步收台法", "清桌面(2min)→换餐具消毒(2min)→迎新客(1min)", "运营部", "D1", "D10", "收台≤6min", ""),
    ("排队效率", "专职收台岗", "高峰时段设专职收台员(非服务员兼岗)", "运营部", "D1", "D7", "专职岗覆盖率80%+", ""),
    ("排队效率", "数字看板", "每桌用餐时长和空桌时间实时显示", "数字化中心", "D5", "D15", "看板上线率100%", ""),
    ("排队效率", "用餐时长柔性引导", "用餐90分钟后提供打包/甜品选项", "运营部", "D10", "D20", "超时率<10%", ""),
    ("排队效率", "预约制试点", "工作日晚市开放30%桌位预约", "数字化中心", "D15", "D30", "预约率20%+", ""),
    # 策略3: 产品优化
    ("产品优化", "SKU瘦身15%", "从120个SKU精简至100个，淘汰点单率<3%末位品", "产品研发部", "D31", "D40", "SKU减至≤100", ""),
    ("产品优化", "菜单分区重构", "招牌→人气→新品→饮品小吃四级分区", "产品研发部", "D35", "D45", "新菜单全店上线", ""),
    ("产品优化", "场景化套餐矩阵", "2人168/4人328/6人488三档套餐", "产品研发部", "D31", "D45", "套餐占比40%+", ""),
    ("产品优化", "鲜切系列效率优化", "现切改为半预制+现场摆盘(8min→3min)", "产品研发部", "D40", "D55", "鲜切等待≤3min", ""),
    ("产品优化", "锅底智能温控", "智能温控沸腾时间6min→4min", "设备部", "D45", "D60", "100店安装", ""),
    ("产品优化", "分阶段上菜SOP", "1min锅底→3min凉菜→10min热菜齐", "运营部", "D35", "D50", "SOP执行率90%+", ""),
    # 策略4: 客流引流
    ("客流引流", "短视频内容矩阵", "每店每周3-5条短视频，总部提供模板+AIGC工具", "市场营销部", "D31", "D40", "月触达5亿+", ""),
    ("客流引流", "达人探店合作", "月均50位腰部KOL探店，CPM<30元", "市场营销部", "D35", "D60", "达人合作200+/年", ""),
    ("客流引流", "直播带券", "每周2场门店直播(午市+宵夜)", "市场营销部", "D40", "D55", "月GMV5000万+", ""),
    ("客流引流", "季度IP联名", "Q1游戏/Q2动漫/Q3体育/Q4影视IP限定产品", "市场营销部", "D45", "D60", "联名产品4季", ""),
    ("客流引流", "会员体系2.0", "黑海特权升级+沉默会员激活+会员日运营", "会员运营部", "D41", "D50", "会员复购率35%+", ""),
    ("客流引流", "社交裂变", "带新朋友就餐双方各得50元券", "会员运营部", "D45", "D55", "裂变拉新率15%+", ""),
    ("客流引流", "付费会员PLUS", "99元/年PLUS(月1张免锅底+午市9折)", "会员运营部", "D61", "D75", "PLUS付费率5%+", ""),
    ("客流引流", "校园/家庭/宠物场景", "学生证套餐+亲子套餐+20家宠物友好店", "市场营销部", "D50", "D70", "场景店100+", ""),
    # 策略5: 门店运营
    ("门店运营", "一店一策分类", "6类门店分类运营模型部署", "运营部", "D41", "D55", "分类覆盖率100%", ""),
    ("门店运营", "AI智能排班", "基于客流预测+天气/节假日自动排班", "数字化中心", "D45", "D60", "排班AI覆盖率50%+", ""),
    ("门店运营", "AI智能订货", "根据翻台率预测自动生成采购量", "数字化中心", "D61", "D75", "订货系统上线", ""),
    ("门店运营", "低效门店改造", "104家低效门店改造/搬迁/关闭决策", "运营部", "D61", "D85", "决策完成率100%", ""),
    ("门店运营", "主题门店改造", "20家主题门店改造试点", "运营部", "D61", "D85", "主题店20家", ""),
]

for i, row in enumerate(actions, 4):
    fill = RED if row[0] in ("分时段运营","排队效率") else (YEL if row[0] in ("产品优化","客流引流") else BLU)
    for j, val in enumerate(row, 1):
        data(ws2, i, j, val, fill=fill if j <= 2 else None)

for col, w in enumerate([12, 16, 40, 14, 8, 8, 18, 8], 1):
    ws2.column_dimensions[get_column_letter(col)].width = w

# ============================================================
# Sheet 3: KPI追踪仪表盘
# ============================================================
ws3 = wb.create_sheet("3-KPI追踪仪表盘")
ws3.merge_cells('A1:F1')
ws3['A1'] = "翻台率KPI追踪仪表盘"
ws3['A1'].font = TF; ws3['A1'].alignment = CA

h3 = ["KPI指标", "当前值", "30天目标", "60天目标", "90天目标", "考核频率"]
for i, h in enumerate(h3, 1):
    ws3.cell(row=3, column=i, value=h)
hdr(ws3, 3, len(h3))

kpis = [
    ("整体翻台率(次/天)", 3.9, 3.96, 4.04, 4.1, "日"),
    ("午市翻台率(次/天)", 1.2, 1.5, 1.7, 1.8, "日"),
    ("晚市翻台率(次/天)", 2.1, 2.2, 2.3, 2.5, "日"),
    ("宵夜翻台率(次/天)", 0.8, 1.0, 1.1, 1.2, "日"),
    ("排队流失率", "20%", "15%", "12%", "10%", "周"),
    ("平均收台时间(分钟)", 10, 8, 7, 6, "周"),
    ("平均用餐时长(分钟)", 78, 76, 74, 72, "周"),
    ("套餐点单占比", "20%", "25%", "35%", "40%", "月"),
    ("会员复购率(月)", "25%", "28%", "32%", "35%", "月"),
    ("会员日到店量增幅", "—", "+10%", "+20%", "+30%", "月"),
    ("午市套餐渗透率", "0%", "20%", "35%", "40%", "周"),
    ("等位预点餐率", "0%", "30%", "50%", "60%", "周"),
]

for i, (kpi, cur, t1, t2, t3, freq) in enumerate(kpis, 4):
    data(ws3, i, 1, kpi)
    data(ws3, i, 2, cur, fill=YEL)
    data(ws3, i, 3, t1, fill=YEL)
    data(ws3, i, 4, t2, fill=BLU)
    data(ws3, i, 5, t3, fill=GRN)
    data(ws3, i, 6, freq)

for col, w in enumerate([22, 12, 12, 12, 12, 12], 1):
    ws3.column_dimensions[get_column_letter(col)].width = w

# KPI趋势图
chart1 = LineChart()
chart1.title = "翻台率提升路径 (当前→30天→60天→90天)"
chart1.style = 2
chart1.y_axis.title = "翻台率(次/天)"
chart1.height = 10; chart1.width = 20
data_kpi = Reference(ws3, min_col=2, min_row=3, max_col=5, max_row=4)
chart1.add_data(data_kpi, titles_from_data=True)
cats_kpi = Reference(ws3, min_col=1, min_row=4, max_row=4)
# 使用整体翻台率行
chart1 = LineChart()
chart1.title = "整体翻台率提升路径"
chart1.style = 2
chart1.y_axis.title = "次/天"
chart1.x_axis.title = "时间节点"
chart1.height = 8; chart1.width = 20
labels = ["当前", "30天", "60天", "90天"]
chart1.set_categories(Reference(ws3, min_col=2, min_row=3, max_col=5, max_row=3))
# 手动构造
ws3_t = wb.create_sheet("_tmp_data")
ws3_t.append(["节点", "整体翻台率", "午市", "晚市", "宵夜"])
ws3_t.append(["当前", 3.9, 1.2, 2.1, 0.8])
ws3_t.append(["30天", 3.96, 1.5, 2.2, 1.0])
ws3_t.append(["60天", 4.04, 1.7, 2.3, 1.1])
ws3_t.append(["90天", 4.1, 1.8, 2.5, 1.2])
chart_t = LineChart()
chart_t.title = "翻台率提升路径 (分时段)"
chart_t.style = 2
chart_t.y_axis.title = "翻台率(次/天)"
chart_t.x_axis.title = "时间节点"
chart_t.height = 10; chart_t.width = 22
data_t = Reference(ws3_t, min_col=2, min_row=1, max_col=5, max_row=5)
chart_t.add_data(data_t, titles_from_data=True)
cats_t = Reference(ws3_t, min_col=1, min_row=2, max_row=5)
chart_t.set_categories(cats_t)
chart_t.dataLabels = DataLabelList(showVal=True)
ws3.add_chart(chart_t, "A18")
wb.remove(ws3_t)

# ============================================================
# Sheet 4: 效果测算模型
# ============================================================
ws4 = wb.create_sheet("4-效果测算模型")
ws4.merge_cells('A1:F1')
ws4['A1'] = "翻台率提升效果测算模型"
ws4['A1'].font = TF; ws4['A1'].alignment = CA
ws4.merge_cells('A2:F2')
ws4['A2'] = "假设：翻台率每提升0.1次/天 ≈ 增量收入5-6亿元/年 | 毛利率59.5%"
ws4['A2'].font = SF; ws4['A2'].alignment = CA

h4 = ["策略", "翻台率提升(次/天)", "增量收入(亿/年)", "投入成本(亿/年)", "净增利润(亿/年)", "ROI"]
for i, h in enumerate(h4, 1):
    ws4.cell(row=4, column=i, value=h)
hdr(ws4, 4, len(h4))

model = [
    ("分时段运营", 0.06, 3.5, 0.8),
    ("排队效率", 0.05, 2.8, 0.3),
    ("产品优化", 0.04, 2.2, 0.5),
    ("客流引流", 0.04, 2.5, 1.2),
    ("门店运营", 0.01, 1.0, 0.4),
]

for i, (name, lift, rev, cost) in enumerate(model, 5):
    data(ws4, i, 1, name)
    data(ws4, i, 2, lift, fill=GRN, fmt='0.00')
    data(ws4, i, 3, rev, fmt='0.0')
    data(ws4, i, 4, cost, fmt='0.0')
    profit = round(rev * 0.595 - cost, 2)
    data(ws4, i, 5, profit, fill=GRN, fmt='0.00')
    roi = round(profit / cost, 2)
    data(ws4, i, 6, roi, fmt='0.00"x"')

# 合计
data(ws4, 10, 1, "合计", bold=True, fill=PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid"))
ws4.cell(row=10, column=1).font = HFt
data(ws4, 10, 2, 0.20, bold=True, fill=PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid"))
ws4.cell(row=10, column=2).font = HFt
ws4.cell(row=10, column=2).number_format = '0.00'
data(ws4, 10, 3, 12.0, bold=True, fill=PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid"))
ws4.cell(row=10, column=3).font = HFt
ws4.cell(row=10, column=3).number_format = '0.0'
data(ws4, 10, 4, 3.2, bold=True, fill=PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid"))
ws4.cell(row=10, column=4).font = HFt
ws4.cell(row=10, column=4).number_format = '0.0'
data(ws4, 10, 5, 3.94, bold=True, fill=PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid"))
ws4.cell(row=10, column=5).font = HFt
ws4.cell(row=10, column=5).number_format = '0.00'
data(ws4, 10, 6, 1.23, bold=True, fill=PatternFill(start_color="0969DA",end_color="0969DA",fill_type="solid"))
ws4.cell(row=10, column=6).font = HFt
ws4.cell(row=10, column=6).number_format = '0.00"x"'

# 注释
ws4.cell(row=12, column=1, value="注：净增利润 = 增量收入 × 毛利率(59.5%) - 投入成本；ROI = 净增利润 / 投入成本").font = SF

for col, w in enumerate([16, 18, 16, 16, 16, 10], 1):
    ws4.column_dimensions[get_column_letter(col)].width = w

# 效果柱状图
chart2 = BarChart()
chart2.type = "col"
chart2.title = "各策略增量收入与投入对比 (亿元/年)"
chart2.style = 2
chart2.y_axis.title = "亿元"
chart2.x_axis.title = "策略"
chart2.height = 10; chart2.width = 22
d1 = Reference(ws4, min_col=3, min_row=4, max_col=3, max_row=9)
chart2.add_data(d1, titles_from_data=True)
d2 = Reference(ws4, min_col=4, min_row=4, max_col=4, max_row=9)
chart2.add_data(d2, titles_from_data=True)
cats4 = Reference(ws4, min_col=1, min_row=5, max_row=9)
chart2.set_categories(cats4)
chart2.dataLabels = DataLabelList(showVal=True)
ws4.add_chart(chart2, "A14")

# ============================================================
# Sheet 5: 风险管理矩阵
# ============================================================
ws5 = wb.create_sheet("5-风险管理矩阵")
ws5.merge_cells('A1:E1')
ws5['A1'] = "风险管理矩阵"
ws5['A1'].font = TF; ws5['A1'].alignment = CA

h5 = ["风险描述", "发生概率", "影响程度", "风险等级", "应对措施"]
for i, h in enumerate(h5, 1):
    ws5.cell(row=3, column=i, value=h)
hdr(ws5, 3, len(h5))

risks = [
    ("策略执行不一致(1304家门店)", "高", "中", "WARN", "数字看板+区域巡检+月度KPI考核，末位10%门店重点帮扶"),
    ("午市套餐蚕食晚市利润", "中", "中", "WARN", "限定午市时段(11-14h)且套餐不含晚市招牌菜品"),
    ("收台提速影响顾客体验", "中", "高", "CRITICAL", "柔性引导(打包/甜品)替代催促，设90分钟用餐底线"),
    ("客流恢复不及预期", "中", "高", "CRITICAL", "月度check点，未达标启动B计划(加大折扣+直播频次)"),
    ("AI排号系统技术故障", "低", "中", "INFO", "备用人工排号流程+系统容灾方案"),
    ("外卖与到店互 cannibalize", "中", "低", "INFO", "外卖产品与到店差异化(一人食vs聚餐场景)"),
    ("员工激励成本超预算", "低", "低", "INFO", "激励预算封顶(月营收2%以内)"),
    ("竞争对手跟随降价", "中", "中", "WARN", "聚焦服务体验差异化而非价格战，强化服务即产品壁垒"),
]

for i, (desc, prob, impact, level, action) in enumerate(risks, 4):
    data(ws5, i, 1, desc)
    data(ws5, i, 2, prob)
    data(ws5, i, 3, impact)
    fill = RED if level == "CRITICAL" else (YEL if level == "WARN" else BLU)
    data(ws5, i, 4, level, fill=fill)
    data(ws5, i, 5, action)

for col, w in enumerate([28, 10, 10, 10, 50], 1):
    ws5.column_dimensions[get_column_letter(col)].width = w

# ============================================================
# Sheet 6: 分时段运营模板
# ============================================================
ws6 = wb.create_sheet("6-分时段运营模板")
ws6.merge_cells('A1:E1')
ws6['A1'] = "分时段运营策略模板"
ws6['A1'].font = TF; ws6['A1'].alignment = CA

h6 = ["时段", "时间区间", "目标翻台率", "核心策略", "关键动作"]
for i, h in enumerate(h6, 1):
    ws6.cell(row=3, column=i, value=h)
hdr(ws6, 3, len(h6))

slots = [
    ("午市", "10:30-14:30", 1.8, "商务套餐+快取通道+时段延长", "68/88元套餐30min上齐；3km写字楼定向券；10:30开门；预点餐到店即取"),
    ("下午茶", "14:30-17:00", 0.6, "社交场景+积分双倍", "58元下午茶套餐(甜品+饮品)；银海/红海积分双倍；跨界IP合作"),
    ("晚市", "17:00-21:00", 2.5, "排队优化+收台标准化+套餐化", "智能排号+等位送菜；三步收台≤6min；场景化套餐占比40%+"),
    ("宵夜", "21:00-24:00", 1.2, "专属菜单+演唱会引流+深夜食堂", "烤串啤酒小龙虾(60-80元)；凭票根8折；50店24h试点"),
    ("深夜", "24:00-03:00", 0.5, "24h门店+夜间专属优惠", "50家门店周五/六24h营业；深夜专属套餐；夜间会员双倍积分"),
]

for i, (slot, time, target, strategy, actions) in enumerate(slots, 4):
    data(ws6, i, 1, slot, bold=True)
    data(ws6, i, 2, time)
    data(ws6, i, 3, target, fill=GRN, fmt='0.0')
    data(ws6, i, 4, strategy)
    data(ws6, i, 5, actions)

for col, w in enumerate([8, 14, 12, 28, 55], 1):
    ws6.column_dimensions[get_column_letter(col)].width = w

# ============================================================
# 保存
# ============================================================
wb.save(OUTPUT)
print(f"Excel saved: {OUTPUT}")
