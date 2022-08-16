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
import{A22_data} from '../../datain'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale)

export default {
  name: 'glahp_A21',
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
        labels: ["女性", "男性"],
        datasets: [{
          backgroundColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)'
          ],
          data: A22_data
    }]
  }

  }}}

</script>
