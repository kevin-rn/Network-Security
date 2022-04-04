<template>
  <el-card shadow="always">
    <template #header>
      <span
        >Total Banned IPs: <b>{{ props.total }}</b></span
      >
    </template>
    <PieChart
      v-if="props.data && props.total > 0" 
      class="chart"
      :chartData="props.data"
      :options="options"
      :plugins="plugins"
    />
    <div class="desc" v-else><p>No Data</p></div>
  </el-card>
</template>

<script setup>
import { PieChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);
const props = defineProps(["data", "total"]);

const options = {
  animations: false,
  plugins: {
    legend: {
      position: "left",
    },
  },
};
</script>

<style scoped>
.chart {
  height: 200px;
  width: 100%;
}
.desc {
  text-align: center;
  padding: 20px;
}
</style>
