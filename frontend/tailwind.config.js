// ==============================================================================
// CONFIGURATION: tailwind.config.js
// ==============================================================================
// PURPOSE: 
// Tailwind CSS configuration file that customizes the utility-first CSS 
// framework for the NoaMetrics landing page. Defines custom colors, fonts, 
// spacing, and responsive breakpoints to match the design system.
//
// OPERATING PRINCIPLE:
// - Extends Tailwind's default configuration with custom theme values
// - Defines brand-specific color palette and typography
// - Configures content paths for efficient CSS purging
// - Sets up custom utility classes and component variants
// ==============================================================================

/** @type {import('tailwindcss').Config} */
module.exports = {
  // =================================================================== 
  // SECTION 1: CONTENT CONFIGURATION
  // Purpose: Define file paths for CSS class detection and purging
  // ===================================================================
  content: [
    "./components/**/*.{js,vue,ts}",    // Vue components
    "./layouts/**/*.vue",               // Nuxt layouts
    "./pages/**/*.vue",                 // Nuxt pages
    "./plugins/**/*.{js,ts}",           // Nuxt plugins
    "./app.vue",                        // Main app file
    "./error.vue"                       // Error page
  ],
  
  // =================================================================== 
  // SECTION 2: THEME CUSTOMIZATION
  // Purpose: Extend default Tailwind theme with custom values
  // ===================================================================
  theme: {
    extend: {
      // =============================================================== 
      // SECTION 2.1: CUSTOM COLOR PALETTE
      // Purpose: Define brand-specific colors for consistent design
      // =============================================================== 
      colors: {
        primary: {
          50: '#eff6ff',    // Very light blue
          100: '#dbeafe',   // Light blue
          200: '#bfdbfe',   // Medium light blue
          300: '#93c5fd',   // Medium blue
          400: '#60a5fa',   // Medium bright blue
          500: '#3b82f6',   // Standard blue
          600: '#2563eb',   // Primary brand blue
          700: '#1d4ed8',   // Dark blue
          800: '#1e40af',   // Darker blue
          900: '#1e3a8a',   // Very dark blue
        }
      },
      
      // =============================================================== 
      // SECTION 2.2: TYPOGRAPHY CONFIGURATION
      // Purpose: Define custom font families and text styling
      // =============================================================== 
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],  // Primary font stack
      },
      
      // =============================================================== 
      // SECTION 2.3: SPACING AND SIZING
      // Purpose: Custom spacing values for consistent layout
      // =============================================================== 
      spacing: {
        '18': '4.5rem',   // Custom spacing value
        '88': '22rem',    // Custom large spacing
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  
  // =================================================================== 
  // SECTION 3: PLUGINS CONFIGURATION
  // Purpose: Include additional Tailwind plugins for enhanced functionality
  // ===================================================================
  plugins: [
    // Add plugins here as needed (e.g., @tailwindcss/forms, @tailwindcss/typography)
  ],
} 