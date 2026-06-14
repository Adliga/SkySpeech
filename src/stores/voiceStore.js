import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/api'

export const useVoiceStore = defineStore('voice', () => {
  const standardVoices = ref([
    { name: 'ru-Male', displayName: 'Мужской (Рус)', icon: '-' },
    { name: 'ru-Female', displayName: 'Женский (Рус)', icon: '-' },
    { name: 'en-US-Male', displayName: 'English Male', icon: '-' },
    { name: 'en-US-Female', displayName: 'English Female', icon: '-' },
    { name: 'robot', displayName: 'Робот', icon: '-' },
  ])

  const clonedVoices = ref([])
  const activeVoiceId = ref('ru-Male')
  const isLoading = ref(false)
  const error = ref('')

  async function fetchVoices() {
    isLoading.value = true
    error.value = ''
    try {
      const { data } = await api.post('/voices/standard')
      standardVoices.value = data.voices
    } catch (e) {
      if (e.code !== 'ERR_NETWORK') {
        error.value = 'Не удалось загрузить голоса с сервера'
      }
    } finally {
      isLoading.value = false
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
