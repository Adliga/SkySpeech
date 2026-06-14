<template>
  <div class="audio-result-panel">
    <h3 class="audio-result-title">Итоговое аудио</h3>
    <div class="audio-track-area">
      <audio
        ref="audioPlayerRef"
        :src="audioStore.audioUrl"
        class="audio-player-hidden"
        @ended="isPlaying = false"
        @timeupdate="onTimeUpdate"
        @loadedmetadata="onLoadedMetadata"
      ></audio>
      <div class="track-inner-white">
        <template v-if="audioStore.audioUrl">
          <div class="track-controls">
            <div class="progress-bar" ref="progressBarRef" @click="seekAudio">
              <div class="progress-fill" :style="{ width: progressPct + '%' }"></div>
            </div>
            <span class="time-display">{{ timeLabel }}</span>
          </div>
        </template>
        <template v-else>
          <span class="track-empty-text">Аудио пока нет</span>
        </template>
      </div>
    </div>
    <div class="play-btn-row">
      <button class="play-btn" @click="togglePlay" :disabled="!audioStore.audioUrl">
        <span v-if="!isPlaying">▶</span>
        <span v-else>⏸</span>
      </button>
    </div>
  </div>
  <button
    class="audio-download-btn"
    :disabled="!audioStore.audioUrl"
    @click="downloadAudio"
  >Скачать</button>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAudioStore } from '@/stores/audioStore'

const audioStore = useAudioStore()

const audioPlayerRef = ref(null)
const progressBarRef = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)

const progressPct = computed(() => {
  if (!duration.value) return 0
  return (currentTime.value / duration.value) * 100
})

function fmtTime(sec) {
  if (!sec || !isFinite(sec)) return '0:00'
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

const timeLabel = computed(() => {
  return `${fmtTime(currentTime.value)} / ${fmtTime(duration.value)}`
})

function togglePlay() {
  const el = audioPlayerRef.value
  if (!el) return
  if (el.paused) {
    el.play()
    isPlaying.value = true
  } else {
    el.pause()
    isPlaying.value = false
  }
}

function onTimeUpdate() {
  const el = audioPlayerRef.value
  if (!el) return
  currentTime.value = el.currentTime
}

function onLoadedMetadata() {
  const el = audioPlayerRef.value
  if (!el) return
  duration.value = el.duration
  currentTime.value = el.currentTime
}

function seekAudio(e) {
  const el = audioPlayerRef.value
  const bar = progressBarRef.value
  if (!el || !bar) return
  const rect = bar.getBoundingClientRect()
  const x = (e.clientX - rect.left) / rect.width
  el.currentTime = x * duration.value
  currentTime.value = el.currentTime
}

function downloadAudio() {
  if (!audioStore.audioUrl) return
  const a = document.createElement('a')
  a.href = audioStore.audioUrl
  a.download = 'speech.mp3'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

onMounted(() => {
  if (!audioStore.audioUrl) {
    audioStore.setAudio('/speech.mp3')
  }
})
</script>

<style scoped>
.audio-result-panel {
  background: rgba(0, 120, 200, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 28px;
  padding: 24px 24px 24px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
  border: 1px solid rgba(255,255,255,0.3);
}
.audio-result-title {
  color: white;
  text-align: center;
  font-size: 24px;
  margin: 0 0 16px;
  font-weight: 500;
}
.audio-track-area {
  margin-bottom: 0;
}
.audio-player-hidden {
  display: none;
}
.track-inner-white {
  background: rgba(255,255,255,0.8);
  border-radius: 24px;
  padding: 24px 20px;
  box-sizing: border-box;
  min-height: 80px;
}
.track-controls {
  display: flex;
  align-items: center;
  gap: 14px;
}
.progress-bar {
  flex: 1;
  height: 14px;
  background: rgba(0,0,0,0.12);
  border-radius: 7px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: rgba(50, 100, 200, 0.8);
  border-radius: 7px;
  transition: width 0.1s linear;
  pointer-events: none;
}
.time-display {
  font-size: 13px;
  color: #333;
  font-weight: 500;
  white-space: nowrap;
  font-family: 'Segoe UI', 'Montserrat', Arial, sans-serif;
}
.track-empty-text {
  color: #999;
  font-size: 14px;
  display: block;
  text-align: center;
  font-family: 'Segoe UI', 'Montserrat', Arial, sans-serif;
}
.play-btn-row {
  display: flex;
  justify-content: center;
  margin-top: -28px;
  position: relative;
  z-index: 2;
}
.play-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  background: rgba(50, 100, 200, 0.9);
  color: white;
  font-size: 22px;
  transition: 0.2s;
  line-height: 1;
}
.play-btn:hover:not(:disabled) {
  background: white;
  color: #3264c8;
  transform: scale(1.05);
}
.play-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.audio-download-btn {
  display: block;
  margin: 0px auto 0;
  padding: 16px;
  border: none;
  border-radius: 40px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  background: rgba(25, 57, 216, 0.7);
  color: white;
  transition: 0.2s;
}
.audio-download-btn:hover:not(:disabled) {
  background: #008080;
  transform: scale(1.02);
}
.audio-download-btn:active:not(:disabled) {
  transform: scale(0.98);
}
.audio-download-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
