<!--
==============================================================================
LAYOUT: default.vue
==============================================================================
PURPOSE: 
Default layout template that provides the common structure for all pages in 
the application. Implements a standard header-main-footer layout pattern with 
proper semantic HTML and accessibility considerations.

OPERATING PRINCIPLE:
- Uses semantic HTML5 elements for proper document structure
- Provides consistent layout across all pages
- Integrates header and footer components automatically
- Maintains clean separation of layout and page content
- Implements responsive design patterns
==============================================================================
-->

<template>
  <!-- =================================================================== -->
  <!-- SECTION 1: PAGE CONTAINER                                         -->
  <!-- Purpose: Main page wrapper with full height and flex layout       -->
  <!-- =================================================================== -->
  <div class="min-h-screen flex flex-col">
    <!-- =============================================================== -->
    <!-- SECTION 1.1: SITE HEADER                                     -->
    <!-- Purpose: Global navigation and branding                      -->
    <!-- =============================================================== -->
    <AppHeader />
    
    <!-- =============================================================== -->
    <!-- SECTION 1.2: MAIN CONTENT AREA                               -->
    <!-- Purpose: Dynamic content slot for page-specific content      -->
    <!-- =============================================================== -->
    <main class="flex-1">
      <slot />
    </main>
    
    <!-- =============================================================== -->
    <!-- SECTION 1.3: SITE FOOTER                                     -->
    <!-- Purpose: Global footer with links and company information    -->
    <!-- =============================================================== -->
    <AppFooter />
  </div>
</template>

<script setup>
// ==============================================================================
// SCRIPT SETUP SECTION
// ==============================================================================
// PURPOSE: 
// Minimal layout script that leverages Nuxt's auto-import functionality for 
// header and footer components. Maintains clean separation between layout 
// structure and component logic.
//
// OPERATING PRINCIPLE:
// - Uses Nuxt 3 auto-imports for component registration
// - No additional logic required for basic layout functionality
// - Components are automatically resolved from the components directory
// ==============================================================================

// =================================================================== 
// SECTION 1: COMPONENT AUTO-IMPORTS
// Purpose: Nuxt automatically imports AppHeader and AppFooter components
// ===================================================================
// Note: Header and Footer components are auto-imported by Nuxt
// No explicit imports needed due to components/ directory auto-discovery
</script> 