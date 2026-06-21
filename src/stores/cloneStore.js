import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/api'
import { useVoiceStore } from '@/stores/voiceStore'
import { useNotificationStore } from '@/stores/notificationStore'

export const useCloneStore = defineStore('clone', () => {
  const isLoading = ref(false)

  async function uploadAudio(audioFile, name) {
    isLoading.value = true

    try {
      const formData = new FormData()
      formData.append('audio', audioFile)
      const { data } = await api.post('/clone', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      const voiceStore = useVoiceStore()
      voiceStore.addClonedVoice({
        id: data.voice_id,
        displayName: name,
        icon: '',
        ready: true,
      })
      const notificationStore = useNotificationStore()
      notificationStore.show('Голос добавлен!', 'success', 3000)
    } catch (e) {
      const notificationStore = useNotificationStore()
      if (e.code === 'ERR_NETWORK') {
        notificationStore.show('Сервер недоступен.', 'error', 4000)
      } else {
        notificationStore.show('Ошибка при загрузке голоса', 'error', 4000)
      }
    } finally {
      isLoading.value = false
    }
  }

  return { isLoading, uploadAudio }
})
