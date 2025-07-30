<template>
  <Transition name="toast-fade">
    <div v-if="visible" :class="['fixed z-[1000]', toastPositionClass, 'max-w-xs w-full shadow-xl rounded-xl px-5 py-4 bg-white/90 dark:bg-gray-900/90 border border-gray-200 dark:border-gray-800 text-gray-900 dark:text-gray-100 font-semibold text-base flex items-center gap-3 toast-blur']" :style="{fontFamily: 'Inter, Space Grotesk, sans-serif'}">
      <slot>{{ message }}</slot>
      <button @click="close" class="ml-auto text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors focus:outline-none">
        <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
const props = defineProps({
  message: String,
  duration: { type: Number, default: 3000 },
  modelValue: Boolean,
  position: { type: String, default: 'right' } // 'right' or 'left'
})
const emit = defineEmits(['update:modelValue'])
const visible = ref(props.modelValue)
watch(() => props.modelValue, v => visible.value = v)
watch(visible, v => emit('update:modelValue', v))
let timer
watch(visible, v => {
  if (v && props.duration > 0) {
    clearTimeout(timer)
    timer = setTimeout(() => visible.value = false, props.duration)
  }
})
function close() { visible.value = false }
const toastPositionClass = computed(() => props.position === 'left' ? 'bottom-6 left-6' : 'bottom-6 right-6')
</script>

<style scoped>
.toast-blur {
  backdrop-filter: blur(8px);
}
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style> 