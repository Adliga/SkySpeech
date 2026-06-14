<template>
  <div class="background">
    <div class="sky-bg"></div>

    <div
      class="notification-bar"
      :class="[notificationStore.visible ? 'show' : 'hide', notificationStore.type]"
    >
      {{ notificationStore.message }}
    </div>

    <div class="content">
      <h1 class="title">SkySpeech</h1>

      <div class="main-layout">
        <VoicePanel />
        <div class="center-col">
          <TextPanel ref="textPanelRef" />
          <button class="generate-btn" @click="textPanelRef?.synthesizeSpeech()">
            <span v-if="audioStore.isLoading" class="spinner"></span>
            <span v-else>Сгенерировать речь</span>
          </button>

          <AudioPlayer />
        </div>
        <SettingsPanel />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VoicePanel from '@/components/VoicePanel.vue'
import TextPanel from '@/components/TextPanel.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'
import { useAudioStore } from '@/stores/audioStore'
import { useNotificationStore } from '@/stores/notificationStore'

const textPanelRef = ref(null)
const audioStore = useAudioStore()
const notificationStore = useNotificationStore()
</script>

<style scoped>
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  background: #0f172a;
}
.sky-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/sky.png');
  background-size: cover;
  background-position: center;
  z-index: -1;
}
.content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 80px 30px 40px;
  font-family: 'Segoe UI', 'Montserrat', Arial, sans-serif;
  box-sizing: border-box;
}
.title {
  text-align: center;
  font-size: 68px;
  font-weight: bold;
  color: white;
  text-shadow: 0 4px 20px rgba(0,0,0,0.5);
  letter-spacing: 2px;
  margin-top: 0;
  margin-bottom: 90px;
}
.main-layout {
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 30px;
  align-items: start;
}
.center-col {
  width: 820px;
  justify-self: center;
  margin-top: -50px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.generate-btn {
  display: block;  
  margin: 0 auto;
  padding: 16px;
  border: none;
  border-radius: 40px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  background: rgba(25, 57, 216, 0.7);
  color: white;
  transition: 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.generate-btn:hover {
  background: #008080;
}
.generate-btn:active {
  transform: scale(0.98);
}
.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.spinner {
  width: 22px;
  height: 22px;
  border: 3px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.notification-bar {
  position: fixed;
  top: 0;
  left: 50%;
  width: 820px;
  z-index: 1000;
  padding: 10px 20px;
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  color: white;
  background: rgba(25, 57, 216, 0.9);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
  transform: translateX(-50%) translateY(-100%);
  transition: transform 0.35s ease;
  font-family: 'Segoe UI', 'Montserrat', Arial, sans-serif;
  border-radius: 0 0 12px 12px;
}
.notification-bar.show {
  transform: translateX(-50%) translateY(0);
}
.notification-bar.hide {
  transform: translateX(-50%) translateY(-100%);
}
.notification-bar.error {
  background: rgba(200, 50, 50, 0.9);
}
.notification-bar.success {
  background: rgba(50, 180, 80, 0.9);
}

@media (max-width: 960px) {
  .main-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  .content {
    padding: 20px;
  }
  .notification-bar {
    width: calc(100% - 40px);
  }
}
</style>
