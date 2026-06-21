<template>
  <div class="column text-column">
    <h2 class="column-title">Введите текст для озвучки</h2>

    <div class="panel text-panel">
      <textarea
        v-model="textToSpeak"
        class="text-input"
        placeholder="Напишите что-нибудь..."
      ></textarea>

      <div class="action-row">
        <button class="mic-btn" @click="startVoiceInput" title="Голосовой ввод">
          <img src="/micro_white.png" class="mic-icon" />
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAudioStore } from '@/stores/audioStore'
import { useVoiceStore } from '@/stores/voiceStore'
import { useSettingsStore } from '@/stores/settingsStore'
import { useNotificationStore } from '@/stores/notificationStore'
import api from '@/api/api'

const audioStore = useAudioStore()
const voiceStore = useVoiceStore()
const settingsStore = useSettingsStore()
const notificationStore = useNotificationStore()

const textToSpeak = ref('')

let recognition = null

async function synthesizeSpeech() {
  if (!textToSpeak.value.trim()) {
    notificationStore.show('⚠️ Введите текст! ⚠️', 'error', 2500)
    return
  }

  audioStore.isLoading = true

  try {
    const response = await api.post('/synthesize', {
      text: textToSpeak.value,
      voice_id: voiceStore.activeVoiceId,
      rate: settingsStore.rate,
      pitch: settingsStore.pitch,
    }, { responseType: 'blob' })

    const url = URL.createObjectURL(response.data)
    audioStore.setAudio(url)
  } catch {
    notificationStore.show('❌ Сервер недоступен. Попробуйте позже. ❌', 'error', 3000)
  } finally {
    audioStore.isLoading = false
  }
}

defineExpose({ synthesizeSpeech })

function startVoiceInput() {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    notificationStore.show('Ваш браузер не поддерживает распознавание речи', 'error', 3000)
    return
  }
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  recognition = new SpeechRecognition()
  recognition.lang = 'ru-RU'
  recognition.interimResults = false
  recognition.maxAlternatives = 1

  recognition.onstart = () => { notificationStore.show('Слушаю... Говорите', 'info') }
  recognition.onresult = (event) => {
    const spokenText = event.results[0][0].transcript
    textToSpeak.value = spokenText
  }
  recognition.onerror = (event) => {
    notificationStore.show(`❌ Ошибка: ${event.error} ❌`, 'error', 3000)
  }
  recognition.onend = () => {
    notificationStore.show('Распознавание завершено', 'info', 1500)
  }
  recognition.start()
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
.text-input {
  width: 100%;
  background: rgba(255,255,255,0.8);
  border: none;
  border-radius: 24px;
  padding: 16px;
  font-size: 20px;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
  margin-bottom: 0;
}
.text-input:focus {
  outline: none;
  background: white;
  box-shadow: 0 0 0 2px #4c9aff;
}
.action-row {
  display: flex;
  justify-content: center;
  margin-top: -28px;
  position: relative;
  z-index: 2;
}
.mic-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  background: rgba(50, 100, 200, 0.9);
  transition: 0.2s;
}
.mic-btn:hover {
  background: white;
  transform: scale(1.05);
}
.mic-icon {
  width: 28px;
  height: 28px;
  display: block;
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
</style>
