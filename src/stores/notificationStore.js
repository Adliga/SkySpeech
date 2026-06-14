import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotificationStore = defineStore('notification', () => {
  const message = ref('')
  const type = ref('info')
  const visible = ref(false)
  let timeoutId = null

  function show(msg, typeName = 'info', duration = 3000) {
    clearTimeout(timeoutId)
    message.value = msg
    type.value = typeName
    visible.value = true
    timeoutId = setTimeout(() => {
      visible.value = false
    }, duration)
  }

  return { message, type, visible, show }
})
