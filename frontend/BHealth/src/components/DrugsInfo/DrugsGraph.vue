<template>
  <div ref="chartContainer" style="width: 100%; height: 400px;"></div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import api from "@/api";

const chartContainer = ref<HTMLDivElement | null>(null);
let myChart: echarts.ECharts | null = null;

const dataAxis = ref<string[]>(['1']);
const data = ref<number[]>([1]);
const yMax =  ref<number>();

const getAllDrugs = async () => {
  const res = await api.getAllDrugs();
  const drugs = res.results;
  console.log('drugList:', drugs);

  dataAxis.value = [];
  data.value = [];
  let yMaxValue = 0;
  // Populate dataAxis and data
  for (const drug of drugs) {
    dataAxis.value.push(drug.name);
    data.value.push(drug.stock);
    yMaxValue = Math.max(yMaxValue, drug.stock);
  }
  yMax.value = yMaxValue * 1.2;
  console.log('dataAxis:', dataAxis.value);
  console.log('data:', data.value);

  // Update chart after fetching data
  setChartOption();
};

const setChartOption = () => {
  const option: echarts.EChartsOption = {
    xAxis: {
      data: dataAxis.value,
      axisLabel: {
        inside: true,
        color: '#fff'
      },
      axisTick: {
        show: false
      },
      axisLine: {
        show: false
      },
      z: 10
    },
    yAxis: {
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: '#999'
      },
      max: yMax.value
    },
    dataZoom: [
      {
        type: 'inside'
      }
    ],
    series: [
      {
        type: 'bar',
        showBackground: true,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#2378f7' },
              { offset: 0.7, color: '#2378f7' },
              { offset: 1, color: '#83bff6' }
            ])
          }
        },
        data: data.value
      }
    ]
  };
  myChart?.setOption(option);

  // Keep the click event for zooming
  const zoomSize = 6;
  myChart?.on('click', (params) => {
    myChart?.dispatchAction({
      type: 'dataZoom',
      startValue: dataAxis.value[Math.max(params.dataIndex - zoomSize / 2, 0)],
      endValue: dataAxis.value[Math.min(params.dataIndex + zoomSize / 2, data.value.length - 1)]
    });
  });
};

const initChart = () => {
  if (chartContainer.value) {
    myChart = echarts.init(chartContainer.value);
  }
};

onMounted(() => {
  initChart();
  getAllDrugs();
});
</script>

<style scoped>

</style>
