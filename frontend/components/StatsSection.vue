<template>
  <Transition name="section-fade" appear>
    <section id="stats" class="py-12 md:py-16 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white relative overflow-hidden">
      <!-- Decorative background elements -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-0 left-1/4 w-96 h-96 bg-primary-500 rounded-full filter blur-3xl"></div>
        <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500 rounded-full filter blur-3xl"></div>
      </div>
      
      <div class="container-custom relative z-10">
        <div class="text-center mb-10 md:mb-12">
          <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-3 leading-tight">
            Thousands of CVs, Hundreds of Calls,<br class="hidden sm:block">
            Zero Certainty.
          </h2>
          <p class="text-base md:text-lg opacity-80 max-w-2xl mx-auto px-4">
            The traditional hiring process is broken. Here's what companies face every day.
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 max-w-5xl mx-auto">
          <!-- Stat 1 -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 md:p-8 border border-white/10 hover:bg-white/10 transition-all duration-300">
            <div class="text-3xl md:text-4xl font-bold mb-2 text-primary-300">
              <span class="counter" data-target="80">{{ stat1 }}</span>%
            </div>
            <p class="text-base md:text-lg font-medium mb-1">of hiring hours wasted</p>
            <p class="text-sm opacity-70">on triaging instead of evaluating</p>
            <p class="text-xs opacity-50 mt-4 font-medium">Forbes • Deloitte</p>
          </div>
          
          <!-- Stat 2 -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 md:p-8 border border-white/10 hover:bg-white/10 transition-all duration-300">
            <div class="text-3xl md:text-4xl font-bold mb-2 text-blue-300">
              1 in <span class="counter" data-target="5">{{ stat2 }}</span>
            </div>
            <p class="text-base md:text-lg font-medium mb-1">CVs contain fraud</p>
            <p class="text-sm opacity-70">fake credentials & experience</p>
            <p class="text-xs opacity-50 mt-4 font-medium">HireRight Benchmark</p>
          </div>
          
          <!-- Stat 3 -->
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 md:p-8 border border-white/10 hover:bg-white/10 transition-all duration-300">
            <div class="text-3xl md:text-4xl font-bold mb-2 text-green-300">
              $<span class="counter" data-target="240">{{ stat3 }}</span>K
            </div>
            <p class="text-base md:text-lg font-medium mb-1">cost of a bad hire</p>
            <p class="text-sm opacity-70">in lost productivity & rehiring</p>
            <p class="text-xs opacity-50 mt-4 font-medium">Harvard Business Review</p>
          </div>
        </div>
        
        <!-- Bottom CTA -->
        <div class="text-center mt-10 md:mt-12">
          <p class="text-lg md:text-xl font-medium mb-6 opacity-90 italic">
            "There has to be a smarter way."
          </p>
          <div class="flex flex-col sm:flex-row gap-3 justify-center">
            <button class="bg-white text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-all duration-200 text-sm md:text-base shadow-lg">
              See How NuoMetrics Solves This →
            </button>
            <button class="border border-white/30 text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/10 backdrop-blur-sm transition-all duration-200 text-sm md:text-base" @click="handleJoinBetaClick">
              Join the Beta
            </button>
          </div>
        </div>
      </div>
    </section>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useJoinBetaDrawer } from '~/composables/useJoinBetaDrawer'
import { useToast } from '~/composables/useToast'
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
const toast = useToast()
function handleJoinBetaClick() {
  if (isLoggedIn.value) {
    toast?.show('You have already joined the beta!')
  } else {
    open()
  }
}

const stat1 = ref(0)
const stat2 = ref(0)
const stat3 = ref(0)

const animateValue = (ref, start, end, duration) => {
  let startTimestamp = null
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp
    const progress = Math.min((timestamp - startTimestamp) / duration, 1)
    ref.value = Math.floor(progress * (end - start) + start)
    if (progress < 1) {
      window.requestAnimationFrame(step)
    }
  }
  window.requestAnimationFrame(step)
}

onMounted(() => {
  // Animate counters when component is mounted with staggered delays for better UX
  setTimeout(() => animateValue(stat1, 0, 80, 2000), 200)
  setTimeout(() => animateValue(stat2, 0, 5, 1500), 600)
  setTimeout(() => animateValue(stat3, 0, 240, 2500), 1000)
})
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
</style> 