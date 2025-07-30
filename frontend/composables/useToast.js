import { ref, provide, inject, nextTick } from 'vue'

const toastMessage = ref('')
const toastVisible = ref(false)

export function provideToast() {
  provide('toast', {
    show(msg, duration = 3000) {
      toastMessage.value = msg
      toastVisible.value = false
      nextTick(() => {
        toastVisible.value = true
        setTimeout(() => { toastVisible.value = false }, duration)
      })
    },
    toastMessage,
    toastVisible
  })
}

export function useToast() {
  return inject('toast')
} 