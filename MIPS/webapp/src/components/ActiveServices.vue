<template>
  <el-card class="box-card">
    <template #header>
      <span>Available Services</span>
    </template>
    <div
      class="content"
      v-if="props.services && Object.keys(props.services).length > 0"
    >
      <div
        v-for="(key, index) in Object.keys(props.services)"
        :key="`services-${index}`"
      >
        <ServiceSwitch :state="props.services[key]" :name="key" />
      </div>
    </div>
    <div class="content" v-else><p>No Data</p></div>
  </el-card>
</template>

<script setup>
import ServiceSwitch from "./ServiceSwitch.vue";
const props = defineProps(["services"]);
</script>

<style scoped>
.content {
  text-align: center;
  padding: 20px;
  max-height: 150px;
  overflow-y: auto;
}
</style>
