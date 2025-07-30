<template>
  <Transition name="section-fade" appear>
    <section class="py-12 md:py-16 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 relative overflow-hidden">
      <!-- Decorative background elements -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-1/2 left-1/4 w-96 h-96 bg-primary-500 rounded-full filter blur-3xl -translate-y-1/2"></div>
        <div class="absolute top-1/2 right-1/4 w-96 h-96 bg-blue-500 rounded-full filter blur-3xl -translate-y-1/2"></div>
      </div>
      <div class="container-custom relative z-10">
        <div class="bg-white/5 backdrop-blur-sm rounded-2xl p-8 md:p-12 border border-white/10 max-w-5xl mx-auto">
          <div class="flex flex-col md:flex-row items-center justify-between gap-8">
            <!-- Left Content -->
            <div class="text-center md:text-left">
              <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-3 text-white">
                Stop wasting hours on CVs.
              </h2>
              <p class="text-base md:text-lg text-white/70">
                Start seeing the truth in minutes.
              </p>
            </div>
            <!-- Right CTA -->
            <TransitionGroup name="cta-fade" tag="div" class="flex-shrink-0 flex flex-col sm:flex-row gap-3">
              <button 
                v-for="(btn, idx) in 2" :key="idx"
                @click="idx === 0 ? handleJoinBetaClick() : undefined"
                :class="[
                  'inline-block font-semibold transition-all duration-200 text-base md:text-lg shadow-lg whitespace-nowrap cta-fade-item',
                  idx === 0 ? 'bg-primary-600 text-white px-6 py-4 rounded-lg hover:bg-primary-700' : 'bg-white text-gray-900 px-6 py-4 rounded-lg hover:bg-gray-100'
                ]"
              >
                {{ idx === 0 ? 'Join Beta Program' : 'Analyse My Candidates Now' }}
              </button>
            </TransitionGroup>
          </div>
        </div>
      </div>
      <Toast v-model="showAlreadyLoggedIn" message="You are already logged in!" position="left" :duration="3000" />
    </section>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useJoinBetaDrawer } from '~/composables/useJoinBetaDrawer'
import Toast from '~/components/Toast.vue'
const isLoggedIn = ref(false)

// Функция для обновления состояния логина
const updateLoginState = () => {
  if (typeof window !== 'undefined') {
    isLoggedIn.value = !!localStorage.getItem('access_token')
  }
}

onMounted(() => {
  // Инициализация состояния
  updateLoginState()
  
  // Слушатель изменений в localStorage
  const storageHandler = (e) => {
    if (e.key === 'access_token') {
      updateLoginState()
    }
  }
  
  const authChangedHandler = () => {
    updateLoginState()
  }
  
  window.addEventListener('storage', storageHandler)
  window.addEventListener('auth-changed', authChangedHandler)
  
  // Очистка слушателей при размонтировании
  onUnmounted(() => {
    window.removeEventListener('storage', storageHandler)
    window.removeEventListener('auth-changed', authChangedHandler)
  })
})
const { open } = useJoinBetaDrawer()
const showAlreadyLoggedIn = ref(false)
function handleJoinBetaClick() {
  if (isLoggedIn.value) {
    showAlreadyLoggedIn.value = true
    setTimeout(() => showAlreadyLoggedIn.value = false, 3000)
  } else {
    open()
  }
}
</script>

<style scoped>
.section-fade-enter-active, .section-fade-leave-active {
  transition: opacity 0.7s cubic-bezier(.4,0,.2,1);
}
.section-fade-enter-from, .section-fade-leave-to {
  opacity: 0;
}
.section-fade-enter-to, .section-fade-leave-from {
  opacity: 1;
}
.cta-fade-enter-active, .cta-fade-leave-active {
  transition: all 0.6s cubic-bezier(.4,0,.2,1);
}
.cta-fade-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
.cta-fade-enter-to {
  opacity: 1;
  transform: none;
}
.cta-fade-leave-from {
  opacity: 1;
  transform: none;
}
.cta-fade-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
</style> 