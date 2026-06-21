import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/api'

export const useVoiceStore = defineStore('voice', () => {
  const standardVoices = ref([])
  const clonedVoices = ref([])
  const activeVoiceId = ref('')
  const isLoading = ref(false)
  const error = ref('')

  const FALLBACK_VOICES = [
    { name: 'child', displayName: 'Детский', icon: '', ready: true },
    { name: 'female_3', displayName: 'Женский', icon: '', ready: true },
    { name: 'speaker_3', displayName: 'Мужской_1', icon: '', ready: true },
    { name: 'speaker_4', displayName: 'Мужской_2', icon: '', ready: true },
    { name: 'speaker_5', displayName: 'Мужской_3', icon: '', ready: true },
  ]

  const initVoiceId = FALLBACK_VOICES[0].name

  standardVoices.value = FALLBACK_VOICES
  activeVoiceId.value = initVoiceId

  async function fetchVoices() {
    try {
      const { data } = await api.post('/voices/standard', {}, { timeout: 8000 })
      if (data.voices && data.voices.length > 0) {
        standardVoices.value = data.voices
        if (!data.voices.some(v => v.name === activeVoiceId.value)) {
          activeVoiceId.value = data.voices[0].name
        }
      }
    } catch {
      
    }
  }

  function setActiveVoice(id) {
    activeVoiceId.value = id
  }

  function addClonedVoice(voice) {
    clonedVoices.value.push(voice)
    activeVoiceId.value = voice.id
  }

  return {
    standardVoices,
    clonedVoices,
    activeVoiceId,
    isLoading,
    error,
    fetchVoices,
    setActiveVoice,
    addClonedVoice,
  }
})
