<template>
  <el-card class="card" shadow="always">
    <template #header>
      <span>Banned IP Addresses:</span>
    </template>
    <el-table align="center" :data="props.data" style="width: 100%">
      <el-table-column sortable fixed prop="ip" label="IP" width="130px" />
      <el-table-column sortable prop="service" label="Service" width="200px" />
      <el-table-column sortable prop="timestamp" label="Date" width="450px" />
      <el-table-column fixed="right" label="Action" width="100px">
        <template #default="scope">
          <el-button type="text" size="small" @click="unban(scope.$index)"
            >Unban</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
const props = defineProps(["data"]);
const emits = defineEmits(["unban"]);
const unban = (index) => {
  emits("unban", props.data[index].ip);
};
</script>

<style scoped>
.card {
  margin-left: 10px;
  margin-right: 10px;
}
</style>
