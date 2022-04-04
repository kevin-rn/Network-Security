<template>
  <el-dialog
    v-model="isOpen"
    title="Change the current configurations"
    :before-close="handleClose"
    :destroy-on-close="true"
    width="100%"
    :center="true"
  >
    <div class="content">
      <p>The number of failures a host is allowed before it is banned:</p>
      <input
        type="text"
        v-model="threshold"
        onkeypress="return event.charCode >= 48 && event.charCode <= 57"
      />
      requests
      <p>The failures should happen within a time window of:</p>
      <input
        v-model="timeWindow"
        type="text"
        onkeypress="return event.charCode >= 48 && event.charCode <= 57"
      />
      minutes
      <p>The time an IP address or host is banned:</p>
      <input
        v-model="blockedTime"
        type="text"
        onkeypress="return event.charCode >= 48 && event.charCode <= 57"
      />
      minutes <br /><br />
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button type="primary" @click="handleSave">Confirm</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from "vue";
import { ElMessage } from "element-plus";

const emits = defineEmits(["close", "save"]);
const props = defineProps(["open"]);

const isOpen = ref(props.open, "dialog");
const threshold = ref("");
const timeWindow = ref("");
const blockedTime = ref("");

const handleClose = (done) => {
  emits("close");
  if (done instanceof Function) done();
};

const handleSave = () => {
  if (!threshold.value || !timeWindow.value || !blockedTime.value) {
    ElMessage({
      message: "All configuration values should be filled in!",
      center: true,
      type: "error",
    });
    return;
  } else {
    emits("save", threshold.value, timeWindow.value, blockedTime.value);
  }
};

watch(
  () => props.open,
  (newValue, _) => (isOpen.value = newValue)
);
</script>

<style scoped>
.content {
  text-align: center;
}
</style>
