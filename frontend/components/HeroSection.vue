<!--
==============================================================================
COMPONENT: HeroSection.vue
==============================================================================
PURPOSE: 
Primary hero section that serves as the main value proposition and first 
impression for visitors. Features responsive layout with heading, description, 
CTA buttons, and hero image. Integrates with the global join-beta drawer 
functionality for user conversion.

OPERATING PRINCIPLE:
- Responsive grid layout that adapts from mobile to desktop
- Prominent call-to-action buttons for conversion optimization
- Integration with join-beta drawer through composable
- Optimized image loading with proper alt text for accessibility
- Strategic use of visual hierarchy and typography scaling
==============================================================================
-->

<template>
  <Transition name="section-fade" appear>
    <section class="relative bg-[#f4f6fb] min-h-[500px] md:min-h-[600px] lg:h-[700px] flex items-center">
      <div class="container-custom w-full">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 w-full items-center">
          <!-- =============================================================== -->
          <!-- SECTION 1.1: CONTENT AREA (LEFT COLUMN)                      -->
          <!-- Purpose: Main value proposition text and call-to-action       -->
          <!-- =============================================================== -->
          <Transition name="fade-slide" appear>
            <div class="order-2 lg:order-1 px-4 md:px-0 lg:pr-8 py-8 md:py-12 lg:py-0">
              <!-- Main Heading -->
              <h1 class="text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-extrabold text-gray-900 mb-4 md:mb-6 text-center lg:text-left leading-tight">
                Stop Guessing. <br />Hire the Real Talent.
              </h1>
              <!-- Value Proposition Description -->
              <p class="text-base md:text-lg lg:text-xl text-gray-600 mb-6 md:mb-8 text-center lg:text-left max-w-xl mx-auto lg:mx-0">
                Watch how our coming-soon AI video-analysis spots interview fraud and start today with instant CV fraud & fit scoring.
              </p>
              <!-- Call-to-Action Buttons -->
              <div class="flex flex-col sm:flex-row gap-3 md:gap-4 justify-center lg:justify-start">
                <!-- Primary CTA - Join Beta -->
                <button 
                  @click="handleHeroJoinBetaClick"
                  class="px-4 md:px-6 py-3 rounded-lg bg-primary-600 text-white font-semibold text-sm md:text-base shadow-lg hover:bg-primary-700 hover:shadow-xl transition-all duration-200 fade-slide-item"
                >
                  Get on Wait-List
                </button>
                <!-- Secondary CTA - Free Trial -->
                <NuxtLink to="#video-ai" class="px-4 md:px-6 py-3 rounded-lg border-2 border-primary-600 text-primary-600 font-semibold text-sm md:text-base bg-white hover:bg-primary-50 hover:shadow-md transition-all duration-200 fade-slide-item" scroll-to>
                  Analyze Your First 3 CVs Free
                </NuxtLink>
              </div>
            </div>
          </Transition>
          <!-- =============================================================== -->
          <!-- SECTION 1.2: HERO IMAGE (RIGHT COLUMN)                       -->
          <!-- Purpose: Visual representation of the product/service         -->
          <!-- =============================================================== -->
          <Transition name="fade-slide" appear>
            <div class="order-1 lg:order-2 flex items-center justify-center w-full h-[300px] md:h-[400px] lg:h-[500px] xl:h-[600px]">
              <div class="w-full h-full max-w-md lg:max-w-none overflow-hidden rounded-lg lg:rounded-xl shadow-xl">
                <img 
                  :src="heroImg" 
                  alt="AI Video Interview Analysis Dashboard" 
                  class="w-full h-full object-cover object-center fade-slide-item" 
                />
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </section>
  </Transition>
  <Toast v-model="showAlreadyLoggedIn" message="You are already logged in!" position="left" :duration="3000" />
</template>

<script setup>
// ==============================================================================
// SCRIPT SETUP SECTION
// ==============================================================================
// PURPOSE: 
// Integrates the hero section with the global join-beta drawer functionality.
// Provides clean separation between presentation and state management.
//
// OPERATING PRINCIPLE:
// - Uses composable for drawer state management
// - Maintains component simplicity with minimal logic
// - Follows Vue 3 Composition API best practices
// ==============================================================================

// =================================================================== 
// SECTION 1: DRAWER INTEGRATION
// Purpose: Connect to global drawer state management for CTA button
// ===================================================================
const { open } = useJoinBetaDrawer()

// Импорт hero image для корректной загрузки
import heroImg from '~/public/hero-image-v0.jpg'
import { ref, onUnmounted } from 'vue'
import { useToast } from '~/composables/useToast'
import Toast from '~/components/Toast.vue'
const isLoggedIn = ref(false)
const toast = useToast()
const showAlreadyLoggedIn = ref(false)

// Функция для обновления состояния логина
const updateLoginState = () => {
  if (typeof window !== 'undefined') {
    isLoggedIn.value = !!localStorage.getItem('access_token')
  }
}

// Инициализация состояния
updateLoginState()

// Слушатель изменений в localStorage
if (typeof window !== 'undefined') {
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
}
function handleHeroJoinBetaClick() {
  if (isLoggedIn.value) {
    showAlreadyLoggedIn.value = true
    setTimeout(() => showAlreadyLoggedIn.value = false, 3000)
  } else {
    open()
  }
}
</script>

<style scoped>
/* =================================================================== */
/* SECTION 1: COMPONENT-SPECIFIC STYLES                              */
/* Purpose: Custom styles that override or extend Tailwind classes   */
/* =================================================================== */

/* Primary brand color variants */
.bg-primary-50 { background-color: #f5f7ff; }
.bg-primary-600 { background-color: #6366f1; }
.hover\:bg-primary-700:hover { background-color: #4f46e5; }
.border-primary-600 { border-color: #6366f1; }
.text-primary-600 { color: #6366f1; }

.section-fade-enter-active, .section-fade-leave-active {
  transition: opacity 0.7s cubic-bezier(.4,0,.2,1);
}
.section-fade-enter-from, .section-fade-leave-to {
  opacity: 0;
}
.section-fade-enter-to, .section-fade-leave-from {
  opacity: 1;
}

.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.7s cubic-bezier(.4,0,.2,1);
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(40px) scale(0.98);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: none;
}
.fade-slide-leave-from {
  opacity: 1;
  transform: none;
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(40px) scale(0.98);
}
</style> 