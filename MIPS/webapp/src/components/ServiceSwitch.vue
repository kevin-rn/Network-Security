<template>
  <div class="container">
    <span> {{ props.name }} </span>
    <el-switch
      v-model="state"
      :loading="loading"
      :before-change="beforeChange"
    />
  </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import { SERVER } from "../constant";
import { ref } from "vue";
import { ElMessage } from "element-plus";

const props = defineProps(["state", "name"]);

const state = ref(props.state);
const loading = ref(false);

const beforeChange = () => {
  loading.value = true;
  console.log("toggled", props.name, !state.value);
  return new Promise((resolve, reject) => {
    axios
      .post(`${SERVER}/api/v1/toggle_service`, {
        service: props.name,
        toggle: !state.value,
      })
      .then((_ans) => {
        if (_ans.data === 200) {
          loading.value = false;
          return resolve(true);
        } else throw new Error("Failed to toggle");
      })
      .catch((err) => {
        console.log("Switch error", err);
        loading.value = false;
        ElMessage.error(`Failed to toggle ${props.name}`);
        return reject();
      });
  });
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
}
</style>
