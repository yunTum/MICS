<template>

<div class="container">
  <Plot_glaph/>
</div>
</template>

<script>
import Plot_glaph from './components/Plot_glaph.vue';



export default {

  name: 'App',
  components: { Plot_glaph}
}
</script>

<style>
  .container{
    background-color:whitesmoke; 
    height:5000px;
}
</style>