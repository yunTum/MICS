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
    :height="25"
   />
</template>



<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

import { Chart } from "chart.js";
import ChartjsPluginStacked100 from "chartjs-plugin-stacked100";

import { label_time_arr ,C1_maxint_data ,C1_nomalint_data ,C1_notint_data  } from "../../datain";


ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
Chart.register(ChartjsPluginStacked100);


export default {
  name: 'graph_C1',
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
        label:           "関心度なし",
        data:             C1_notint_data,
        backgroundColor: "rgba(171, 171, 171, 0.8)",
        borderColor:     "rgba(171, 171, 171, 1.0)",
        borderWidth:     1,
      }, 
      {  barPercentage:0.6,
         label:          "関心度有り",
        data:            C1_nomalint_data,
        backgroundColor: "rgba(232, 123, 134, 0.8)",
        borderColor:     "rgba(232, 123, 134, 1.0)",
        borderWidth:     1,
      }, 
      { barPercentage:0.6,
         label:          "関心度特に有り",
        data:            C1_maxint_data,
        backgroundColor: "rgba(220, 53, 69, 0.8)",
        borderColor:     "rgba(220, 53, 69, 1.0)",
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

      }
    }
  }
}
</script>