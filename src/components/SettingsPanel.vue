<template>
  <div class="column settings-column">
    <h2 class="column-title">Настройки</h2>
    <div class="panel settings-panel">
      <div class="setting">
        <label>Скорость: {{ settingsStore.rate }}</label>
        <input type="range" v-model.number="settingsStore.rate" min="0.5" max="2" step="0.1" />
      </div>
      <div class="setting">
        <label>Высота тона: {{ settingsStore.pitch }}</label>
        <input type="range" v-model.number="settingsStore.pitch" min="0.5" max="2" step="0.1" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSettingsStore } from '@/stores/settingsStore'

const settingsStore = useSettingsStore()
</script>

<style scoped>
.column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.column-title {
  color: white;
  text-align: center;
  font-size: 28px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
  margin: 0;
}
.panel {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 28px;
  padding: 24px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
  border: 1px solid rgba(255,255,255,0.3);
  transition: all 0.2s;
}
.setting {
  margin-bottom: 24px;
}
.setting:last-child {
  margin-bottom: 0;
}
.setting label {
  display: block;
  color: white;
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 18px;
}
input[type="range"] {
  width: 100%;
  cursor: pointer;
  background: rgba(255,255,255,0.4);
  border-radius: 10px;
  height: 6px;
}
</style>
