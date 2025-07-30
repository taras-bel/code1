// ==============================================================================
// CONFIGURATION: nuxt.config.ts
// ==============================================================================
// PURPOSE: 
// Main Nuxt.js configuration file that defines the application setup, build 
// settings, styling integration, and development environment configuration. 
// Configures Tailwind CSS integration and sets up the development server.
//
// OPERATING PRINCIPLE:
// - Defines Nuxt 3 application configuration using TypeScript
// - Integrates Tailwind CSS for utility-first styling
// - Sets up development server with custom host/port settings
// - Configures build and deployment optimization settings
// ==============================================================================

// =================================================================== 
// SECTION 1: NUXT CONFIGURATION EXPORT
// Purpose: Define and export the main Nuxt configuration object
// ===================================================================
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  
  app: {
    head: {
      title: 'NoaMetrics - Stop Guessing. Hire the Real Talent.',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { 
          key: 'description', 
          name: 'description', 
          content: 'Watch how our cutting-edge AI video analysis spots Interview fraud and alert fraud with instant CV fraud & AI scoring.' 
        },
        { name: 'format-detection', content: 'telephone=no' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },

  // =================================================================== 
  // SECTION 3: STYLING AND CSS CONFIGURATION
  // Purpose: Setup Tailwind CSS and custom styles
  // ===================================================================
  css: ['~/assets/css/main.css'],  // Global CSS file with Tailwind imports

  // =================================================================== 
  // SECTION 4: MODULE INTEGRATIONS
  // Purpose: Configure Nuxt modules and third-party integrations
  // ===================================================================
  modules: [
    '@nuxtjs/tailwindcss',  // Tailwind CSS module for utility-first styling
    '@nuxt/image',
    '@nuxt/eslint'
  ],

  // =================================================================== 
  // SECTION 5: RUNTIME CONFIGURATION
  // Purpose: Configure runtime environment variables
  // ===================================================================
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000'
    }
  },

  // =================================================================== 
  // SECTION 6: DEVELOPMENT CONFIGURATION
  // Purpose: Configure development server and build settings
  // ===================================================================
  devServer: {
    port: 3000,
    host: '0.0.0.0'
  },

  // Disable service worker in development
  experimental: {
    payloadExtraction: false
  }
})