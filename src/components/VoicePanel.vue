<template>
  <div class="column voices-column">
    <h2 class="column-title">Голоса</h2>

    <div class="panel voices-panel">
      <div class="voices-list">
        <div
          v-for="voice in allVoices"
          :key="voice.id"
          class="voice-item"
          :class="{ active: voiceStore.activeVoiceId === voice.id, cloned: voice.cloned }"
          @click="voiceStore.setActiveVoice(voice.id)"
        >
          <img :src="voice.icon" class="voice-icon" />
          <span>{{ voice.displayName }}</span>
          <span v-if="voice.cloned" class="cloned-badge">мой голос</span>
        </div>
      </div>
    </div>

    <div class="panel clone-panel">
      <h3 class="clone-title">Загрузить свой голос</h3>
      <p class="clone-hint">MP3 или WAV, не более 10 секунд</p>
      <input
        ref="fileInput"
        type="file"
        accept=".mp3,.wav"
        class="file-input-hidden"
        @change="onFileSelected"
      />
      <button class="file-select-btn" @click="fileInput?.click()">
        Выбрать файл
      </button>
      <p v-if="selectedFile" class="file-name">{{ selectedFile.name }}</p>
      <button
        class="clone-btn"
        :disabled="!selectedFile || cloneStore.isLoading"
        @click="uploadVoice"
      >
        <span v-if="cloneStore.isLoading" class="spinner"></span>
        <span v-else>Обучить</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useVoiceStore } from '@/stores/voiceStore'
import { useCloneStore } from '@/stores/cloneStore'
import { useNotificationStore } from '@/stores/notificationStore'

const voiceStore = useVoiceStore()
const cloneStore = useCloneStore()
const notificationStore = useNotificationStore()

const fileInput = ref(null)
const selectedFile = ref(null)

const allVoices = computed(() => {
  const standard = voiceStore.standardVoices.map(v => ({ ...v, id: v.name, cloned: false }))
  const cloned = voiceStore.clonedVoices.map(v => ({ ...v, cloned: true }))
  return [...standard, ...cloned]
})

function onFileSelected(e) {
  selectedFile.value = e.target.files[0] || null
}

async function uploadVoice() {
  if (!selectedFile.value) return
  await cloneStore.uploadAudio(selectedFile.value)
  selectedFile.value = null
  if (fileInput.value) fileInput.value.value = ''
}
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
.voices-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.voice-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.2);
  padding: 12px 16px;
  border-radius: 50px;
  cursor: pointer;
  transition: 0.2s;
  color: white;
  font-weight: 500;
  font-size: 18px;
}
.voice-item:hover {
  background: rgba(255,255,255,0.4);
  transform: scale(1.02);
}
.voice-item.active {
  background: rgba(255,255,255,0.7);
  color: #1e3c72;
  box-shadow: 0 0 0 2px white;
}
.voice-item.cloned {
  border: 1px solid #4caf50;
}
.voice-icon {
  font-size: 28px;
  width: 32px;
  text-align: center;
}
.cloned-badge {
  margin-left: auto;
  font-size: 12px;
  background: #4caf50;
  color: white;
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 600;
}
.clone-panel {
  background: rgba(0, 120, 200, 0.3);
  backdrop-filter: blur(10px);
}
.clone-title {
  color: white;
  text-align: center;
  font-size: 20px;
  margin: 0 0 8px;
  font-weight: 500;
}
.clone-hint {
  color: rgba(255,255,255,0.7);
  text-align: center;
  font-size: 13px;
  margin: 0 0 14px;
}
.file-input-hidden {
  display: none;
}
.file-select-btn {
  width: 100%;
  padding: 12px;
  margin-bottom: 8px;
  border: 1px solid rgba(255,255,255,0.4);
  border-radius: 40px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  background: rgba(255,255,255,0.15);
  color: white;
  transition: 0.2s;
}
.file-select-btn:hover {
  background: rgba(255,255,255,0.35);
  transform: scale(1.02);
}
.file-name {
  color: rgba(255,255,255,0.8);
  font-size: 13px;
  text-align: center;
  margin: 0 0 12px;
  word-break: break-all;
}
.clone-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 40px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  background: rgba(50, 100, 200, 0.9);
  color: white;
  transition: 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.clone-btn:hover:not(:disabled) {
  background: white;
  color: #3264c8;
  transform: scale(1.02);
}
.clone-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
