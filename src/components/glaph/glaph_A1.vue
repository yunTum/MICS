<template>
<Pie
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</template>

<script>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale,} from 'chart.js'
import{A1_data} from '../../datain'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale)

export default {
  name: 'glahp_A1',
  components: { Pie }, 
   props: {
    dataA1:Number
    // chartId: {
    //   type: String,
    //   default: 'bar-chart'
    // },
    // datasetIdKey: {
    //   type: String,
    //   default: 'label'
    // },
    // width: {
    //   type: Number,
    //   default: 400
    // },
    // height: {
    //   type: Number,
    //   default: 400
    // },
    // cssClasses: {
    //   default: '',
    //   type: String
    // },
    // styles: {
    //   type: Object,
    //   default: () => {}
    // },
    // plugins: {
    //   type: Object,
    //   default: () => {}
    // }
  },
  data() {
    return {
      chartData: {
      labels: ["特に関心有り", "関心有り", "関心なし"],
            datasets: [{
                backgroundColor: [
                'rgba(220, 53, 69, 1)'  ,
                'rgba(255, 141, 152, 1)',
                'rgba(138, 138, 138, 1)',
                ],
                data: A1_data
            }]
  }

  }}}

</script>
