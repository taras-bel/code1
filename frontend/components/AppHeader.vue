<!--
==============================================================================
COMPONENT: AppHeader.vue
==============================================================================
PURPOSE: 
Main navigation header component that provides site navigation, branding, and 
access to the beta signup functionality. Implements responsive design with 
mobile hamburger menu and integrates with the global drawer state management.

OPERATING PRINCIPLE:
- Sticky positioning for persistent navigation access
- Responsive design with desktop navigation and mobile menu
- Integration with join-beta drawer through composable
- Keyboard accessibility and proper ARIA attributes
- Auto-closing mobile menu on navigation
==============================================================================
-->

<template>
  <Transition name="header-fade" appear>
    <header class="bg-white shadow-sm sticky top-0 z-50">
      <!-- Mobile Menu Backdrop -->
      <div 
        v-if="mobileMenuOpen" 
        class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
        @click="mobileMenuOpen = false"
      ></div>
      <!-- Mobile Menu Panel -->
      <Transition name="mobile-menu-fade-slide">
        <div 
          v-if="mobileMenuOpen" 
          class="fixed top-0 left-0 w-full h-full z-50 md:hidden"
          style="pointer-events: none;"
        >
          <div 
            class="mobile-menu-content bg-white shadow-2xl w-full h-full p-0 overflow-y-auto relative z-50"
            style="pointer-events: auto; max-height: 100vh;"
            @click.stop
          >
            <div class="flex items-center justify-between px-6 pt-6 pb-2">
              <span class="text-xl font-bold text-primary-600">NoaMetrics</span>
              <button @click="mobileMenuOpen = false" class="p-2 rounded-full hover:bg-gray-100 focus:outline-none">
                <svg class="w-7 h-7 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <nav class="flex flex-col space-y-2 px-6 pb-6">
              <NuxtLink 
                to="#benefits" 
                @click="mobileMenuOpen = false"
                class="text-gray-700 hover:text-primary-600 font-medium py-2 px-2 rounded-md hover:bg-gray-50 transition-colors"
                scroll-to
              >
                Features
              </NuxtLink>
              <NuxtLink v-if="isLoggedIn && route.path !== '/dashboard'" to="/dashboard" @click="mobileMenuOpen = false"
                class="text-gray-700 hover:text-primary-600 font-medium py-2 px-2 rounded-md hover:bg-gray-50 transition-colors"
              >
                Dashboard
              </NuxtLink>
              <button v-if="isLoggedIn && route.path === '/dashboard'" @click="logout(); mobileMenuOpen = false"
                class="text-gray-700 hover:text-red-600 font-medium py-2 px-2 rounded-md hover:bg-gray-50 transition-colors text-left"
              >
                Logout
              </button>
              <button 
                v-if="!isLoggedIn"
                @click="handleMobileJoinBetaClick"
                class="w-full py-3 bg-primary-600 text-white text-base font-semibold rounded-lg transition-all duration-200 flex items-center justify-center gap-2 mt-2 mb-2 shadow hover:bg-primary-700"
              >
                Join Beta
              </button>
              <NuxtLink 
                to="#video-ai" 
                @click="mobileMenuOpen = false"
                class="btn-primary text-sm w-full py-3 mt-2"
                scroll-to
              >
                🎯 Start & CV's Free
              </NuxtLink>
            </nav>
          </div>
        </div>
      </Transition>
      <div class="container-custom">
        <div class="flex justify-between items-center py-3 md:py-4">
          <!-- =============================================================== -->
          <!-- SECTION 1.1: BRAND LOGO                                      -->
          <!-- Purpose: Company branding and home page navigation           -->
          <!-- =============================================================== -->
          <NuxtLink to="/" class="flex items-center">
            <h1 class="text-xl md:text-2xl font-bold text-primary-600">NoaMetrics</h1>
          </NuxtLink>
          
          <!-- =============================================================== -->
          <!-- SECTION 1.2: DESKTOP NAVIGATION                              -->
          <!-- Purpose: Main navigation items for desktop screens           -->
          <!-- =============================================================== -->
          <nav class="hidden md:flex items-center space-x-6 lg:space-x-8">
            <!-- Features Link -->
            <NuxtLink to="#benefits" class="text-gray-700 hover:text-primary-600 font-medium transition-colors" scroll-to>
              Features
            </NuxtLink>
            <!-- Dashboard Link (visible if logged in and not on dashboard) -->
            <NuxtLink v-if="isLoggedIn && route.path !== '/dashboard'" to="/dashboard" class="text-gray-700 hover:text-primary-600 font-medium transition-colors">
              Dashboard
            </NuxtLink>
            <!-- Logout Button (visible if logged in and on dashboard) -->
            <button v-if="isLoggedIn && route.path === '/dashboard'" @click="logout" class="text-gray-700 hover:text-red-600 font-medium transition-colors">
              Logout
            </button>
            <!-- Join Beta Button (hidden if logged in or on dashboard) -->
            <button 
              v-if="!isLoggedIn && route.path !== '/dashboard'"
              @click="handleJoinBetaClick"
              class="text-gray-700 hover:text-primary-600 font-medium transition-colors"
            >
              Join Beta
            </button>
            <!-- Primary CTA Button -->
            <NuxtLink to="#video-ai" class="btn-primary text-sm px-4 py-2" scroll-to>
              🎯 Start & CV's Free
            </NuxtLink>
          </nav>
          
          <!-- =============================================================== -->
          <!-- SECTION 1.3: MOBILE MENU TOGGLE                              -->
          <!-- Purpose: Hamburger menu button for mobile navigation         -->
          <!-- =============================================================== -->
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen" 
            class="md:hidden p-2 rounded-md hover:bg-gray-100 transition-colors"
            :aria-expanded="mobileMenuOpen"
            aria-label="Toggle mobile menu"
          >
            <!-- Hamburger/Close Icon -->
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path 
                v-if="!mobileMenuOpen"
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M4 6h16M4 12h16M4 18h16" 
              />
              <path 
                v-else
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M6 18L18 6M6 6l12 12" 
              />
            </svg>
          </button>
        </div>
        
        <!-- =============================================================== -->
        <!-- SECTION 1.4: MOBILE NAVIGATION MENU                          -->
        <!-- Purpose: Collapsible mobile navigation with full menu items   -->
        <!-- =============================================================== -->
        <div 
          v-if="mobileMenuOpen" 
          class="mobile-menu-content md:hidden py-4 border-t border-gray-200 bg-white relative z-50"
        >
          <nav class="flex flex-col space-y-4">
            <!-- Features Link -->
            <NuxtLink 
              to="#benefits" 
              @click="mobileMenuOpen = false"
              class="text-gray-700 hover:text-primary-600 font-medium py-2 px-2 rounded-md hover:bg-gray-50 transition-colors"
              scroll-to
            >
              Features
            </NuxtLink>
            <!-- Dashboard Link (если не на dashboard) -->
            <NuxtLink v-if="isLoggedIn && route.path !== '/dashboard'" to="/dashboard" @click="mobileMenuOpen = false"
              class="text-gray-700 hover:text-primary-600 font-medium py-2 px-2 rounded-md hover:bg-gray-50 transition-colors"
            >
              Dashboard
            </NuxtLink>
            <!-- Logout Button (если на dashboard) -->
            <button v-if="isLoggedIn && route.path === '/dashboard'" @click="logout(); mobileMenuOpen = false"
              class="text-gray-700 hover:text-red-600 font-medium py-2 px-2 rounded-md hover:bg-gray-50 transition-colors text-left"
            >
              Logout
            </button>
            
            <!-- Join Beta Button (hidden if logged in) -->
            <button 
              v-if="!isLoggedIn"
              @click="handleMobileJoinBetaClick"
              class="text-gray-700 hover:text-primary-600 font-medium py-2 px-2 rounded-md hover:bg-gray-50 transition-colors text-left"
            >
              Join Beta
            </button>
            
            <!-- Primary CTA Button -->
            <NuxtLink 
              to="#video-ai" 
              @click="mobileMenuOpen = false"
              class="btn-primary text-sm w-full py-3 mt-2"
              scroll-to
            >
              🎯 Start & CV's Free
            </NuxtLink>
          </nav>
        </div>
      </div>
    </header>
  </Transition>
</template>

<script setup>
// ==============================================================================
// SCRIPT SETUP SECTION
// ==============================================================================
// PURPOSE: 
// Manages header navigation state, mobile menu functionality, and integration 
// with the global join-beta drawer. Handles keyboard interactions and proper 
// cleanup of event listeners for optimal performance.
//
// OPERATING PRINCIPLE:
// - Uses Vue 3 Composition API with reactive refs
// - Integrates with global composable for drawer control
// - Implements keyboard accessibility patterns
// - Manages mobile menu state and auto-closing behavior
// ==============================================================================

import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useJoinBetaDrawer } from '~/composables/useJoinBetaDrawer'
import { useToast } from '~/composables/useToast'
const toast = useToast()

const isLoggedIn = ref(false)
onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('access_token')
})
const route = useRoute()
// Убираю useRouter
// const router = useRouter()
const { open } = useJoinBetaDrawer()

// =================================================================== 
// SECTION 1: DRAWER INTEGRATION
// Purpose: Connect to global drawer state management
// ===================================================================

// =================================================================== 
// SECTION 2: MOBILE MENU STATE
// Purpose: Control mobile navigation menu visibility
// ===================================================================
const mobileMenuOpen = ref(false)

// --- AUTH STATE ---

function checkAuth() {
  isLoggedIn.value = !!localStorage.getItem('access_token')
}

// Remove useRouter import
// Notify other components about token change
// Redirect to home page
// Filter hidden analyses
// Make the function global for calling from other components
// Add the logout function back for the 'Logout' button
function handleStorageChange(e) {
  if (e.key === 'access_token') {
    checkAuth()
  }
}

// =================================================================== 
// SECTION 3: KEYBOARD INTERACTION HANDLERS
// Purpose: Handle escape key for closing mobile menu
// ===================================================================
const closeOnEscape = (e) => {
  if (e.key === 'Escape') {
    mobileMenuOpen.value = false
  }
}

// =================================================================== 
// SECTION 4: LIFECYCLE HOOKS
// Purpose: Setup and cleanup event listeners
// ===================================================================
onMounted(() => {
  checkAuth()
  window.addEventListener('storage', handleStorageChange)
  document.addEventListener('keydown', closeOnEscape)
})

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange)
  document.removeEventListener('keydown', closeOnEscape)
})

// Add the logout function back for the 'Logout' button
function logout() {
  localStorage.removeItem('access_token')
  isLoggedIn.value = false
  window.dispatchEvent(new StorageEvent('storage', {
    key: 'access_token',
    newValue: null
  }))
  window.location.href = '/'
}

function handleJoinBetaClick() {
  if (isLoggedIn.value) {
    toast?.show('You have already joined the beta!')
  } else {
    open()
  }
}

function handleMobileJoinBetaClick() {
  handleJoinBetaClick()
  mobileMenuOpen.value = false
}


</script> 

<style scoped>
.header-fade-enter-active, .header-fade-leave-active {
  transition: opacity 0.7s cubic-bezier(.4,0,.2,1);
}
.header-fade-enter-from, .header-fade-leave-to {
  opacity: 0;
}
.header-fade-enter-to, .header-fade-leave-from {
  opacity: 1;
}
.mobile-slide-enter-active, .mobile-slide-leave-active {
  transition: all 0.5s cubic-bezier(.4,0,.2,1);
}
.mobile-slide-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.mobile-slide-enter-to {
  opacity: 1;
  transform: none;
}
.mobile-slide-leave-from {
  opacity: 1;
  transform: none;
}
.mobile-slide-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
/* Mobile menu fade + slide-down transition */
.mobile-menu-fade-slide-enter-active, .mobile-menu-fade-slide-leave-active {
  transition: opacity 0.3s cubic-bezier(.4,0,.2,1), transform 0.3s cubic-bezier(.4,0,.2,1);
}
.mobile-menu-fade-slide-enter-from, .mobile-menu-fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-32px);
}
.mobile-menu-fade-slide-enter-to, .mobile-menu-fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style> 