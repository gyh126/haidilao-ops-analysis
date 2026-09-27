document.addEventListener('DOMContentLoaded', function () {
  const PALETTE = {
    s1: '#0969DA', s2: '#8250DF', s3: '#06B6D4', s4: '#BF3989',
    positive: '#52C41A', warning: '#FAAD14', negative: '#FF4D4F',
    axis: '#6F6660', grid: 'rgba(36,32,29,0.12)'
  };

  function baseChart(opts) {
    return Object.assign({
      renderer: 'svg', animation: false,
      tooltip: { trigger: 'axis', appendToBody: true },
      grid: { left: 60, right: 30, top: 40, bottom: 40 },
      textStyle: { fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif', fontSize: 12, color: PALETTE.axis }
    }, opts);
  }

  function make(elId, opt) {
    const el = document.getElementById(elId);
    if (!el) return;
    const chart = echarts.init(el, null, { renderer: 'svg' });
    chart.setOption(baseChart(opt));
    window.addEventListener('resize', () => chart.resize());
  }

  // 1. 收入与利润趋势
  make('chart-revenue-profit', {
    legend: { top: 5, data: ['总收入', '净利润', '核心经营利润'] },
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => (v/10000).toFixed(2) + ' 亿元' },
    xAxis: { type: 'category', data: ['2022', '2023', '2024', '2025'], axisLabel: { fontSize: 13 } },
    yAxis: { type: 'value', name: '千元', axisLabel: { formatter: v => (v/10000).toFixed(0) + '亿' } },
    series: [
      { name: '总收入', type: 'line', smooth: true, data: [31038634, 41453348, 42754687, 43225355], itemStyle: { color: PALETTE.s1 }, label: { show: true, formatter: p => (p.value/10000).toFixed(1) } },
      { name: '净利润', type: 'line', smooth: true, data: [1637306, 4495399, 4700278, 4041885], itemStyle: { color: PALETTE.s2 }, label: { show: true, formatter: p => (p.value/10000).toFixed(1) } },
      { name: '核心经营利润', type: 'line', smooth: true, data: [null, 5246494, 6229880, 5403233], itemStyle: { color: PALETTE.s3 }, label: { show: true, formatter: p => p.value ? (p.value/10000).toFixed(1) : '' } }
    ]
  });

  // 2. 毛利率与净利率趋势
  make('chart-margins', {
    legend: { top: 5, data: ['毛利率', '净利率', '核心经营利润率'] },
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => v.toFixed(2) + '%' },
    xAxis: { type: 'category', data: ['2022', '2023', '2024', '2025'], axisLabel: { fontSize: 13 } },
    yAxis: { type: 'value', name: '%', axisLabel: { formatter: '{value}%' }, min: 0, max: 70 },
    series: [
      { name: '毛利率', type: 'line', smooth: true, data: [58.42, 59.12, 62.08, 59.45], itemStyle: { color: PALETTE.s1 }, label: { show: true, formatter: '{c}%' } },
      { name: '净利率', type: 'line', smooth: true, data: [5.28, 10.84, 10.99, 9.35], itemStyle: { color: PALETTE.s2 }, label: { show: true, formatter: '{c}%' } },
      { name: '核心经营利润率', type: 'line', smooth: true, data: [null, 12.66, 14.57, 12.50], itemStyle: { color: PALETTE.s3 }, label: { show: true, formatter: '{c}%' } }
    ]
  });

  // 3. 收入结构变化
  make('chart-revenue-structure', {
    legend: { top: 5, data: ['海底捞餐厅', '外卖业务', '调味品及食材', '其他餐厅', '特许经营'] },
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => (v/10000).toFixed(2) + ' 亿元' },
    xAxis: { type: 'category', data: ['2022', '2023', '2024', '2025'], axisLabel: { fontSize: 13 } },
    yAxis: { type: 'value', name: '千元', axisLabel: { formatter: v => (v/10000).toFixed(0) + '亿' } },
    series: [
      { name: '海底捞餐厅', type: 'bar', stack: 'rev', data: [28942639, 39266603, 40397616, 37543000], itemStyle: { color: PALETTE.s1 } },
      { name: '外卖业务', type: 'bar', stack: 'rev', data: [1280100, 1041475, 1253869, 2657600], itemStyle: { color: PALETTE.s2 } },
      { name: '调味品及食材', type: 'bar', stack: 'rev', data: [662164, 788651, 575140, 535000], itemStyle: { color: PALETTE.s3 } },
      { name: '其他餐厅', type: 'bar', stack: 'rev', data: [144367, 346176, 483335, 1520600], itemStyle: { color: PALETTE.s4 } },
      { name: '特许经营', type: 'bar', stack: 'rev', data: [0, 0, 16706, 50000], itemStyle: { color: PALETTE.warning } }
    ]
  });

  // 4. 运营指标趋势
  make('chart-ops-metrics', {
    legend: { top: 5, data: ['翻台率(次/天)', '顾客人次(百万)'] },
    tooltip: { trigger: 'axis', appendToBody: true },
    xAxis: { type: 'category', data: ['2022', '2023', '2024', '2025'], axisLabel: { fontSize: 13 } },
    yAxis: [
      { type: 'value', name: '翻台率', position: 'left', min: 2.5, max: 4.5 },
      { type: 'value', name: '顾客人次(百万)', position: 'right' }
    ],
    series: [
      { name: '翻台率(次/天)', type: 'line', smooth: true, data: [3.0, 3.8, 4.1, 3.9], itemStyle: { color: PALETTE.s1 }, label: { show: true, formatter: '{c}' }, yAxisIndex: 0 },
      { name: '顾客人次(百万)', type: 'bar', data: [276.3, 397.0, 415.0, 383.9], itemStyle: { color: PALETTE.s3 }, label: { show: true }, yAxisIndex: 1 }
    ]
  });

  // 5. 成本结构占比
  make('chart-cost-ratio', {
    legend: { top: 5, data: ['原材料', '员工成本', '折旧摊销', '其他开支', '水电', '租金'] },
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => v.toFixed(2) + '%' },
    xAxis: { type: 'category', data: ['2022', '2023', '2024', '2025'], axisLabel: { fontSize: 13 } },
    yAxis: { type: 'value', name: '占收入比%', axisLabel: { formatter: '{value}%' }, max: 100 },
    series: [
      { name: '原材料', type: 'bar', stack: 'cost', data: [41.58, 40.88, 37.92, 40.55], itemStyle: { color: PALETTE.s1 } },
      { name: '员工成本', type: 'bar', stack: 'cost', data: [32.99, 31.46, 33.01, 32.56], itemStyle: { color: PALETTE.s2 } },
      { name: '折旧摊销', type: 'bar', stack: 'cost', data: [10.70, 7.11, 5.98, 5.05], itemStyle: { color: PALETTE.s3 } },
      { name: '其他开支', type: 'bar', stack: 'cost', data: [4.39, 3.89, 3.98, 4.40], itemStyle: { color: PALETTE.s4 } },
      { name: '水电', type: 'bar', stack: 'cost', data: [3.38, 3.32, 3.43, 3.41], itemStyle: { color: PALETTE.warning } },
      { name: '租金', type: 'bar', stack: 'cost', data: [0.88, 0.87, 1.00, 0.99], itemStyle: { color: PALETTE.axis } }
    ]
  });

  // 6. 利润桥 (瀑布图)
  make('chart-profit-bridge', {
    tooltip: { trigger: 'axis', appendToBody: true, valueFormatter: v => (v/10000).toFixed(2) + ' 亿元' },
    xAxis: { type: 'category', data: ['2024年\n核心经营利润', '收入增长', '原材料\n成本增加', '员工成本\n下降', '折旧摊销\n减少', '其他成本\n增加', '2025年\n核心经营利润'], axisLabel: { fontSize: 11, interval: 0 } },
    yAxis: { type: 'value', name: '千元', axisLabel: { formatter: v => (v/10000).toFixed(0) + '亿' } },
    series: [{
      type: 'bar',
      data: [
        { value: 6229880, itemStyle: { color: PALETTE.s1 } },
        { value: 470668, itemStyle: { color: PALETTE.positive } },
        { value: -1315109, itemStyle: { color: PALETTE.negative } },
        { value: 40293, itemStyle: { color: PALETTE.positive } },
        { value: 376435, itemStyle: { color: PALETTE.positive } },
        { value: -272238, itemStyle: { color: PALETTE.negative } },
        { value: 5403233, itemStyle: { color: PALETTE.s1 } }
      ],
      label: { show: true, formatter: function(p) {
        if (p.value > 0) return '+' + (p.value/10000).toFixed(1) + '亿';
        if (p.value < 0) return (p.value/10000).toFixed(1) + '亿';
        return (p.value/10000).toFixed(1) + '亿';
      }, fontSize: 11 }
    }]
  });

  // 7. 门店数量变化
  make('chart-stores', {
    legend: { top: 5, data: ['自营门店', '加盟门店'] },
    tooltip: { trigger: 'axis', appendToBody: true },
    xAxis: { type: 'category', data: ['2022', '2023', '2024', '2025'], axisLabel: { fontSize: 13 } },
    yAxis: { type: 'value', name: '门店数' },
    series: [
      { name: '自营门店', type: 'bar', stack: 'stores', data: [1371, 1374, 1355, 1304], itemStyle: { color: PALETTE.s1 }, label: { show: true } },
      { name: '加盟门店', type: 'bar', stack: 'stores', data: [0, 0, 13, 79], itemStyle: { color: PALETTE.s3 }, label: { show: true } }
    ]
  });
});
