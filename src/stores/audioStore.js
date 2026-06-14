import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAudioStore = defineStore('audio', () => {
  const audioUrl = ref(null)
  const isLoading = ref(false)

  function setAudio(url) {
    clearAudio()
    audioUrl.value = url
  }

  function clearAudio() {
    if (audioUrl.value) {
      URL.revokeObjectURL(audioUrl.value)
      audioUrl.value = null
    }
  }

  return { audioUrl, isLoading, setAudio, clearAudio }
})
