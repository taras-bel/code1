<!-- =============================================================================== -->
<!-- FILE: app.vue                                                                -->
<!-- =============================================================================== -->
<!-- PURPOSE:                                                                      -->
<!-- Root application component for the NoaMetrics landing page. Serves as the    -->
<!-- entry point for the entire Nuxt.js application, providing the base structure -->
<!-- for layout rendering and page routing.                                       -->
<!--                                                                               -->
<!-- OPERATING PRINCIPLE:                                                          -->
<!-- - Acts as the top-level wrapper for all application content                  -->
<!-- - Integrates with Nuxt's built-in layout and routing system                  -->
<!-- - Provides consistent structure across all pages                             -->
<!-- - Automatically handles layout switching and page transitions               -->
<!-- =============================================================================== -->

<template>
  <!-- =============================================================================== -->
  <!-- SECTION 1: APPLICATION LAYOUT WRAPPER                                       -->
  <!-- Purpose: Wraps entire application with Nuxt layout system                   -->
  <!-- =============================================================================== -->
  <NuxtLayout>
    <!-- =============================================================================== -->
    <!-- SECTION 2: PAGE CONTENT RENDERER                                            -->
    <!-- Purpose: Renders the current page component based on routing                -->
    <!-- =============================================================================== -->
    <NuxtPage />
    <Toast v-model="toastVisible" :message="toastMessage" />
  </NuxtLayout>
</template>

<script setup>
import Toast from '~/components/Toast.vue'
import { useToast } from '~/composables/useToast'
const { toastMessage, toastVisible } = useToast() || { toastMessage: '', toastVisible: false }
</script>
