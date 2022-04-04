<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <img alt="Vue logo" src="@/assets/logo.png" width="90" height="90" />
        <div class="title">
          <h1>Modular Intrusion Prevention System</h1>
        </div>
      </el-header>
      <div class="container">
        <ConfigModal
          :open="dialog"
          @close="closeModifyDialog"
          @save="saveModifyDialog"
        />
        <div class="infoCards">
          <ChartIPsByService
            class="infoItem"
            :data="chart_data"
            :total="data_table.length"
          />
          <ActiveServices class="infoItem" :services="services_data" />
          <Configurations
            class="infoItem"
            :nrRequests="config_data.threshold"
            :timeWindow="config_data.time_window"
            :blockedTime="config_data.block_time"
            @openDialog="openModifyDialog"
          />
        </div>
        <div class="bannedIPs">
          <BannedIPsList :data="data_table" @unban="unban" />
        </div>
      </div>
    </el-container>
  </div>
</template>

<script setup>
import ActiveServices from "./components/ActiveServices.vue";
import Configurations from "./components/Configurations.vue";
import ConfigModal from "./components/ConfigModal.vue";
import BannedIPsList from "./components/BannedIPsList.vue";
import ChartIPsByService from "./components/ChartIPsByService.vue";
import axios from "axios";
import { SERVER } from "./constant";
import { onMounted, ref } from "vue";
import { ElLoading, ElMessage } from "element-plus";

const POLL_INTERVAL = 2000 //millisecond 
const data_table = ref([]);
const chart_data = ref(null);
const services_data = ref(null);
const config_data = ref({});
const dialog = ref(false);

const openModifyDialog = () => {
  dialog.value = true;
};

const closeModifyDialog = () => {
  dialog.value = false;
};

const saveModifyDialog = async (threshold, time_window, block_time) => {
  try {
    const res = await axios.post(`${SERVER}/api/v1/change_config`, {
      threshold,
      time_window,
      block_time,
    });

    if (res.data === 200) {
      config_data.value = { threshold, time_window, block_time };
      ElMessage.success("Configuration has been modified successfully.");
      closeModifyDialog();
    }
  } catch (error) {
    ElMessage.error("Something went wrong while saving the configuration.");
  }
};

const unban = async (ip) => {
  const ld = loading();
  try {
    const res = await axios.post(`${SERVER}/api/v1/unban`, { ip });
    if (res.data === 200) {
      await updateBannedList();
      ElMessage.success("Host has successfully been unbanned.");
    } else {
      throw new Error("Failed to unban");
    }
  } catch (error) {
    ElMessage.error("Something went wrong while unbaning the host.");
  }
  ld.close();
};

const loading = () => {
  const loading = ElLoading.service({
    lock: true,
    text: "Loading",
    background: "rgba(0, 0, 0, 0.7)",
  });
  return loading;
};

const COLORS = {
  ssh: "rgb(255, 99, 132)",
  wordpress: "rgb(54, 162, 232)",
  phpmyadmin: "rgb(255, 205, 86)",
  joomla: "rgb(93, 98, 181)",
};

const randomColor = (l) => {
  return "#" + (0x1000000 + Math.random() * 0xffffff).toString(16).substr(1, 6);
};

const processChartData = (data) => {
  let _labels = new Set();
  let _dataLables = {};
  let _data = [];
  let _colors = [];

  for (const d of data) {
    _labels.add(d.service);
    if (!_dataLables[d.service]) _dataLables[d.service] = 0;
    _dataLables[d.service] += 1;
  }

  for (const l of _labels) {
    if (_dataLables[l]) _data.push(_dataLables[l]);
    else _data.push(0);
    if (COLORS[l.toLowerCase()]) _colors.push(COLORS[l.toLowerCase()]);
    else _colors.push(randomColor(l));
  }

  const ans = {
    labels: Array.from(_labels),
    datasets: [
      {
        label: "Total Banned IPs",
        data: _data,
        backgroundColor: _colors,
        hoverOffset: 4,
      },
    ],
  };

  return ans;
};

const processBannedList = (_data) => {
  let data = [];
  for (const d of _data) {
    let _tmp = JSON.parse(d);
    _tmp.timestamp = new Date(_tmp.timestamp).toString();
    data.push(_tmp);
  }
  return data;
};

const updateBannedList = async () => {
  const _data = await axios.get(`${SERVER}/api/v1/get_banned_ips`);
  const bannedList = processBannedList(_data.data);
  data_table.value = bannedList;
  chart_data.value = processChartData(bannedList);
};


async function startPollingBannedIPs() {
  setTimeout(async () => {
    await updateBannedList();
    startPollingBannedIPs();
  }, POLL_INTERVAL);
}

onMounted(async () => {
  const ld = loading();
  try {
    await updateBannedList();
    const _config = await axios.get(`${SERVER}/api/v1/config_state`);
    config_data.value = _config.data[0];
    const _services = await axios.get(`${SERVER}/api/v1/service_status`);
    services_data.value = _services.data;
    // set a timer to poll the banned IPs every POLL_INTERVAL
    startPollingBannedIPs();
  } catch (error) {
    console.log("error", error);
  }
  ld.close();
});
</script>

<style>
body {
  margin: 0;
  height: 100%;
  color: #1f2833;
}
</style>

<style scoped>
.title {
  align-self: center;
  flex: 1;
  padding-left: 10px;
}

.el-header {
  display: flex;
  flex-direction: row;
  justify-content: center;
  background-color: #1f2833;
  height: 20% !important;
  color: #66fcf1;
  padding: 0.5em 1.5em 0.5em 1.5em;
}

.container {
  margin-top: 25px;
  margin-bottom: 50px;
  max-width: 1000px;
  width: 100%;
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-self: center;
}

.infoCards {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-flow: wrap;
  gap: 12px;
  height: 100%;
  margin-left: 10px;
  margin-right: 10px;
}

.infoItem {
  flex: 1;
  min-width: 250px;
}

.bannedIPs {
  margin-top: 25px;
  width: 100%;
  align-self: center;
}

.chartsContainer {
  margin-top: 25px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-flow: wrap;
  gap: 12px;
  margin-left: 10px;
  margin-right: 10px;
}

.chartItem {
  flex: 1;
}
</style>
