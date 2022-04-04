<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>Configuration</span>
        <el-button @click="emits('openDialog')" class="button" type="text">
          Modify
        </el-button>
      </div>
    </template>
    <p
      v-if="props.nrRequests && props.timeWindow && props.blockedTime"
      class="configdesc"
    >
      More than <b>{{ props.nrRequests }} failed attempts,</b><br />
      <b> within {{ props.timeWindow }} minutes </b>, will result in <br />
      <b style="color: red">{{ props.blockedTime }} minutes IP ban.</b>
    </p>
    <p v-else class="configdesc">No Data</p>
  </el-card>
</template>

<script setup>
const emits = defineEmits(["openDialog"]);
const props = defineProps(["nrRequests", "timeWindow", "blockedTime"]);
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: 480px;
}

.configdesc {
  text-align: center;
  padding-top: 20px;
  padding-bottom: 20px;
}

.button {
  height: 0;
}
</style>
