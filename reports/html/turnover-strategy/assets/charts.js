document.addEventListener('DOMContentLoaded', function () {
  const C = {
    s1: '#0969DA', s2: '#8250DF', s3: '#06B6D4', s4: '#BF3989',
    pos: '#52C41A', warn: '#FAAD14', neg: '#FF4D4F',
    axis: '#6A737D', grid: 'rgba(36,32,29,0.12)',
    bg: '#F6F8FA', border: '#D0D7DE'
  };

  function base(opts) {
    return Object.assign({
      renderer: 'svg', animation: false,
      tooltip: { trigger: 'axis', appendToBody: true },
      grid: { left: 55, right: 30, top: 50, bottom: 40 },
      textStyle: { fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif', fontSize: 12, color: C.axis }
    }, opts);
  }

  function make(id, opt) {
    const el = document.getElementById(id);
    if (!el) return;
    const chart = echarts.init(el, null, { renderer: 'svg' });
    chart.setOption(base(opt));
    window.addEventListener('resize', () => chart.resize());
  }

  // 1. 翻台率下降根因分解树
  make('chart-rootcause', {
    tooltip: { trigger: 'item', appendToBody: true },
    series: [{
      type: 'treemap',
      roam: false,
      data: [
        { name: '客流流失\n-3110万人次\n(-7.5%)', value: 35, itemStyle: { color: C.neg } },
        { name: '午市利用不足\n空置率~40%', value: 25, itemStyle: { color: C.warn } },
        { name: '用餐时长增加\n+8-12分钟/桌', value: 20, itemStyle: { color: C.s2 } },
        { name: '排队流失\n等位>30min流失率\n约15-20%', value: 12, itemStyle: { color: C.s4 } },
        { name: '门店关停影响\n-51家自营门店', value: 8, itemStyle: { color: C.axis } }
      ],
      label: { show: true, formatter: '{b}', fontSize: 11, color: '#fff', fontWeight: 'bold' },
      breadcrumb: { show: false }
    }]
  });

  // 2. 分时段翻台率对比 (当前 vs 目标)
  make('chart-time-slot', {
    legend: { top: 5, data: ['当前翻台率', '目标翻台率', '行业标杆'] },
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => v.toFixed(2) + ' 次/天' },
    xAxis: { type: 'category', data: ['午市(11-14时)', '下午茶(14-17时)', '晚市(17-21时)', '宵夜(21-24时)', '深夜(24时后)'], axisLabel: { fontSize: 11, interval: 0 } },
    yAxis: { type: 'value', name: '翻台率(次/天)', min: 0, max: 3 },
    series: [
      { name: '当前翻台率', type: 'bar', data: [1.2, 0.3, 2.1, 0.8, 0.2], itemStyle: { color: C.neg }, label: { show: true, formatter: '{c}' } },
      { name: '目标翻台率', type: 'bar', data: [1.8, 0.6, 2.5, 1.2, 0.5], itemStyle: { color: C.pos }, label: { show: true, formatter: '{c}' } },
      { name: '行业标杆', type: 'line', smooth: true, data: [2.0, 0.8, 2.8, 1.5, 0.6], itemStyle: { color: C.s1 }, lineStyle: { type: 'dashed' } }
    ]
  });

  // 3. 策略影响测算瀑布图
  make('chart-impact-waterfall', {
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => '翻台率 +' + v.toFixed(2) + ' 次/天' },
    xAxis: { type: 'category', axisLabel: { fontSize: 10, interval: 0, formatter: function(v) { return v.replace(/\\n/g, '\n'); } },
      data: ['当前\n3.9次', '分时段\n运营', '排队效率\n提升', '产品菜单\n优化', '客流引流\n复购', '门店运营\n升级', '目标\n4.1次']
    },
    yAxis: { type: 'value', name: '翻台率(次/天)', min: 3.8, max: 4.3 },
    series: [{
      type: 'bar',
      data: [
        { value: 3.9, itemStyle: { color: C.s1 } },
        { value: 0.06, itemStyle: { color: C.pos } },
        { value: 0.05, itemStyle: { color: C.pos } },
        { value: 0.04, itemStyle: { color: C.pos } },
        { value: 0.04, itemStyle: { color: C.pos } },
        { value: 0.01, itemStyle: { color: C.pos } },
        { value: 4.1, itemStyle: { color: C.s1 } }
      ],
      label: { show: true, formatter: function(p) {
        if (p.dataIndex === 0 || p.dataIndex === 6) return p.value.toFixed(1);
        return '+' + p.value.toFixed(2);
      }, fontSize: 11 }
    }]
  });

  // 4. 90天实施路线图甘特图
  make('chart-roadmap', {
    legend: { top: 5, data: ['第一阶段: 速赢(0-30天)', '第二阶段: 深化(31-60天)', '第三阶段: 固化(61-90天)'] },
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => '第' + v + '天' },
    grid: { left: 120, right: 30, top: 50, bottom: 30 },
    xAxis: { type: 'value', name: '天数', min: 0, max: 90 },
    yAxis: { type: 'category', data: ['智能排号上线', '收台SOP标准化', '午市工作日套餐', '等位增值服务升级', '菜单精简(减SKU 15%)', '短视频营销矩阵', '会员体系2.0上线', '一店一策模型部署', '宵夜场景试点', '翻台率KPI看板', 'AI智能订货系统', '主题门店改造试点'] },
    series: [
      { name: '第一阶段: 速赢(0-30天)', type: 'bar', stack: 'roadmap', data: [15, 10, 20, 15, 0, 0, 0, 0, 0, 12, 0, 0], itemStyle: { color: C.neg } },
      { name: '第二阶段: 深化(31-60天)', type: 'bar', stack: 'roadmap', data: [15, 20, 10, 15, 30, 25, 30, 30, 20, 18, 0, 0], itemStyle: { color: C.warn } },
      { name: '第三阶段: 固化(61-90天)', type: 'bar', stack: 'roadmap', data: [0, 0, 0, 0, 0, 15, 0, 0, 10, 0, 30, 30], itemStyle: { color: C.pos } }
    ]
  });

  // 5. KPI拆解雷达图
  make('chart-kpi-radar', {
    tooltip: { trigger: 'item', appendToBody: true },
    radar: {
      indicator: [
        { name: '翻台率', max: 5 },
        { name: '午市利用率', max: 5 },
        { name: '排队转化率', max: 5 },
        { name: '平均用餐时长管控', max: 5 },
        { name: '会员复购率', max: 5 },
        { name: '收台效率', max: 5 }
      ],
      radius: '65%'
    },
    series: [{
      type: 'radar',
      data: [
        { value: [3.9, 1.2, 3.5, 2.8, 3.0, 3.2], name: '当前水平', itemStyle: { color: C.neg }, areaStyle: { color: 'rgba(255,77,79,0.2)' } },
        { value: [4.1, 1.8, 4.5, 4.0, 4.0, 4.2], name: '90天目标', itemStyle: { color: C.pos }, areaStyle: { color: 'rgba(82,196,26,0.2)' } }
      ]
    }]
  });

  // 6. 预期收入影响测算
  make('chart-revenue-impact', {
    legend: { top: 5, data: ['增量收入(亿元)'] },
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => v.toFixed(2) + ' 亿元' },
    xAxis: { type: 'category', data: ['分时段运营', '排队效率提升', '产品菜单优化', '客流引流复购', '门店运营升级'], axisLabel: { fontSize: 11, interval: 0 } },
    yAxis: { type: 'value', name: '增量收入(亿元)' },
    series: [{
      name: '增量收入(亿元)',
      type: 'bar',
      data: [3.5, 2.8, 2.2, 2.5, 1.0],
      itemStyle: { color: C.s1 },
      label: { show: true, formatter: '+{c}亿', fontSize: 12, fontWeight: 'bold' }
    }]
  });
});
