import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  const rate = ref(1)
  const pitch = ref(1)

  return { rate, pitch }
})
