// ==============================================================================
// COMPOSABLE: useJoinBetaDrawer.js
// ==============================================================================
// PURPOSE: 
// Global state management composable for the join-beta drawer component using 
// Nuxt's useState. Provides a centralized way to control drawer visibility 
// across multiple components without prop drilling or complex event chains.
//
// OPERATING PRINCIPLE:
// - Uses Nuxt's useState for server-side compatible reactive state
// - Provides readonly state access to prevent external mutations
// - Exposes simple open/close methods for state manipulation
// - Can be used in any component throughout the application
// - State persists during client-side navigation
// ==============================================================================

import { useState } from '#app'
import { readonly } from 'vue'

// =================================================================== 
// SECTION 1: STATE INITIALIZATION
// Purpose: Create reactive state using Nuxt's useState
// ===================================================================
export const useJoinBetaDrawer = () => {
  // Initialize drawer state - defaults to closed (false)
  const isOpen = useState('join-beta-drawer-open', () => false)

  // =================================================================== 
  // SECTION 2: STATE CONTROL METHODS
  // Purpose: Provide controlled access to state mutations
  // ===================================================================
  
  // Open the drawer
  const open = () => {
    isOpen.value = true
  }

  // Close the drawer
  const close = () => {
    isOpen.value = false
  }

  // =================================================================== 
  // SECTION 3: COMPOSABLE INTERFACE
  // Purpose: Return readonly state and control methods
  // ===================================================================
  return {
    isOpen: readonly(isOpen),  // Readonly to prevent external mutations
    open,                      // Method to open drawer
    close                      // Method to close drawer
  }
} 