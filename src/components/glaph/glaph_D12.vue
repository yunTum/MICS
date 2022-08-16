<template>
  <Bar
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="100"
    :height="20"
  />
</template>



<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

import { Chart } from "chart.js";
import ChartjsPluginStacked100 from "chartjs-plugin-stacked100";
import {label_time_arr ,D12_10_data ,D12_20_data ,D12_30_data ,D12_40_data ,D12_50_data ,D12_60_data  } from "../../datain";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
Chart.register(ChartjsPluginStacked100);


export default {
  name: 'glaph_D12',
  components: { Bar },
 //props: {
 //   chartId: {
 //     type: String,
 //     default: 'bar-chart'
 //   },
 //   datasetIdKey: {
 //     type: String,
 //     default: 'label'
 //   },
 //   width: {
 //     type: Number,
 //     default: 400
 //   },
 //   height: {
 //     type: Number,
 //     default: 400
 //   },
 //   cssClasses: {
 //     default: '',
 //     type: String
 //   },
 //   styles: {
 //     type: Object,
 //     default: () => {}
 //   },
 //   plugins: {
 //     type: Object,
 //     default: () => {}
 //    }
 // },
  data() {
    return {
      chartData: {
            labels: label_time_arr,
      datasets: [
      {
        barPercentage:0.6,
        label:           "10代以下",
        data:             D12_10_data,
        backgroundColor: "rgba(220,53,69, 0.8)",
        borderColor:     "rgba(220,53,69, 1.0)",
        borderWidth:     1,
      }, 
      {
        
        barPercentage:0.6,
        label:          "20代",
        data:            D12_20_data,
        backgroundColor: "rgba(255,142,10, 0.8)",
        borderColor:     "rgba(255,142,10, 1.0)",
        borderWidth:     1,
      }, 
      {
        barPercentage:0.6,
        label:          "30代",
        data:            D12_30_data,
        backgroundColor: "rgba(255,228,88, 0.8)",
        borderColor:     "rgba(255,228,88, 1.0)",
        borderWidth:     1,
      },
      {
       barPercentage:0.6,
       label:           "40代",
        data:            D12_40_data,
        backgroundColor: "rgba(84,241,100, 0.8)",
        borderColor:     "rgba(84,241,100, 1.0)",
        borderWidth:     1,
      }, 
      {
        barPercentage:0.6,
        label:          "50代",
        data:            D12_50_data,
        backgroundColor: "rgba(53,90,220, 0.8)",
        borderColor:     "rgba(53,90,220, 1.0)",
        borderWidth:     1,
      }, 
      {
        borderRadius:5,
        barPercentage:0.6,
        label:          "60代以上",
        data:            D12_60_data,
        backgroundColor: "rgba(151,71,255, 0.8)",
        borderColor:     "rgba(151,71,255, 1.0)",
        borderWidth:     1,
      }
      ],
      },
      chartOptions: {
        responsive: true,
         scales: {
      x: {
        display:      true,
        stacked:      true,
        suggestedMax: 100,
        suggestedMin: 0,
        ticks: {
          stepSize: 10,
        },
      },
      y: {
        display:      true,
        stacked:      true,
      }}
    //     indexAxis: "y",
    //     plugins: {
    //         stacked100: { enable: true },
    //   },
      }
    }
  }
}
</script>