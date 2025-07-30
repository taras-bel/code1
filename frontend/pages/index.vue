<!-- =============================================================================== -->
<!-- FILE: pages/index.vue                                                        -->
<!-- =============================================================================== -->
<!-- PURPOSE:                                                                      -->
<!-- Main landing page for NoaMetrics that showcases the AI-powered CV analysis   -->
<!-- platform. Implements a conversion-optimized layout with strategic CTAs,      -->
<!-- social proof, feature demonstrations, and user engagement elements.          -->
<!--                                                                               -->
<!-- OPERATING PRINCIPLE:                                                          -->
<!-- - Sequential content sections designed for optimal conversion funnel         -->
<!-- - Progressive disclosure of features and benefits                            -->
<!-- - Multiple touchpoints for user engagement and beta signup                   -->
<!-- - Social proof and trust indicators throughout the experience                -->
<!-- - Mobile-first responsive design with accessibility considerations           -->
<!-- =============================================================================== -->

<template>
  <div>
    <!-- =============================================================================== -->
    <!-- SECTION 1: HERO SECTION                                                     -->
    <!-- Purpose: Primary value proposition and main call-to-action                  -->
    <!-- =============================================================================== -->
    <HeroSection />

    <!-- =============================================================================== -->
    <!-- SECTION 2: AI VIDEO DEMONSTRATION                                           -->
    <!-- Purpose: Interactive product demo showing AI analysis capabilities          -->
    <!-- =============================================================================== -->
    <VideoAISection />

    <!-- =============================================================================== -->
    <!-- SECTION 3: PROBLEM STATISTICS                                               -->
    <!-- Purpose: Present hiring industry challenges with compelling statistics      -->
    <!-- =============================================================================== -->
    <StatsSection />

    <!-- =============================================================================== -->
    <!-- SECTION 4: SOLUTION BENEFITS                                                -->
    <!-- Purpose: Four-column feature showcase highlighting key platform benefits    -->
    <!-- =============================================================================== -->
    <BenefitsSection />

    <!-- =============================================================================== -->
    <!-- SECTION 5: PROCESS WORKFLOW                                                 -->
    <!-- Purpose: Step-by-step guide showing how the platform works                  -->
    <!-- =============================================================================== -->
    <ProcessSection />

    <!-- =============================================================================== -->
    <!-- SECTION 6: SOCIAL PROOF                                                     -->
    <!-- Purpose: Customer testimonials and success stories for credibility          -->
    <!-- =============================================================================== -->
    <ClientsSection />

    <!-- =============================================================================== -->
    <!-- SECTION 7: PERFORMANCE METRICS                                              -->
    <!-- Purpose: Additional statistics and platform performance indicators          -->
    <!-- =============================================================================== -->
    <MetricsSection />

    <!-- =============================================================================== -->
    <!-- SECTION 8: FREQUENTLY ASKED QUESTIONS                                       -->
    <!-- Purpose: Address common concerns and provide detailed information           -->
    <!-- =============================================================================== -->
    <FAQSection />

    <!-- =============================================================================== -->
    <!-- SECTION 9: FINAL CALL-TO-ACTION                                             -->
    <!-- Purpose: Last conversion opportunity before footer                           -->
    <!-- =============================================================================== -->
    <CTASection />
    
    <!-- =================================================================== -->
    <!-- SECTION 2: GLOBAL DRAWER INTEGRATION                              -->
    <!-- Purpose: Beta signup modal accessible from any section            -->
    <!-- =================================================================== -->
    <JoinBetaDrawer 
      :is-open="isOpen" 
      @close="close" 
    />
  </div>
</template>

<script setup>
// ==============================================================================
// SCRIPT SETUP SECTION
// ==============================================================================
// PURPOSE: 
// Manages the main landing page state and integrates the global join-beta 
// drawer functionality. Provides clean separation between content sections 
// and modal state management.
//
// OPERATING PRINCIPLE:
// - Uses composable for drawer state management
// - Leverages Nuxt's auto-imports for components
// - Maintains clean component composition patterns
// ==============================================================================

// =================================================================== 
// SECTION 1: DRAWER STATE INTEGRATION
// Purpose: Connect to global drawer state management
// ===================================================================
// Import drawer state and control methods from composable
const { isOpen, close } = useJoinBetaDrawer()
</script> 