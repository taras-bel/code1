<template>
  <Transition name="section-fade" appear>
    <section class="py-20 bg-white">
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">
            Frequently asked questions
          </h2>
          <p class="text-xl text-gray-600">
            Everything you need to know about NoaMetrics
          </p>
        </div>
        
        <div class="max-w-3xl mx-auto">
          <div class="space-y-4">
            <!-- FAQ Item 1 -->
            <div class="border border-gray-200 rounded-lg">
              <button 
                @click="toggleFAQ(0)"
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-semibold text-gray-900">How does NoaMetrics detect fraude?</span>
                <svg 
                  class="w-5 h-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': openItems[0] }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <Transition name="faq-fade">
                <div v-if="openItems[0]" class="px-6 pb-4">
                  <p class="text-gray-600">
                    NoaMetrics uses advanced AI algorithms that analyze multiple factors including facial micro-expressions, 
                    voice patterns, and video consistency. Our system is trained on millions of authentic and deepfake videos, 
                    achieving a 99.5% accuracy rate in detecting synthetic media.
                  </p>
                </div>
              </Transition>
            </div>
            
            <!-- FAQ Item 2 -->
            <div class="border border-gray-200 rounded-lg">
              <button 
                @click="toggleFAQ(1)"
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-semibold text-gray-900">Is the service secure?</span>
                <svg 
                  class="w-5 h-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': openItems[1] }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <Transition name="faq-fade">
                <div v-if="openItems[1]" class="px-6 pb-4">
                  <p class="text-gray-600">
                    Yes, absolutely. NoaMetrics follows enterprise-grade security standards with end-to-end encryption, 
                    SOC 2 compliance, and GDPR adherence. All candidate data is encrypted at rest and in transit, 
                    and we never share or sell any personal information.
                  </p>
                </div>
              </Transition>
            </div>
            
            <!-- FAQ Item 3 -->
            <div class="border border-gray-200 rounded-lg">
              <button 
                @click="toggleFAQ(2)"
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-semibold text-gray-900">Do you already analyze the interview video?</span>
                <svg 
                  class="w-5 h-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': openItems[2] }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <Transition name="faq-fade">
                <div v-if="openItems[2]" class="px-6 pb-4">
                  <p class="text-gray-600">
                    Yes, our AI analyzes interview videos in real-time. The system evaluates verbal responses, body language, 
                    facial expressions, and voice patterns to provide comprehensive insights. You'll receive detailed reports 
                    including confidence scores, authenticity verification, and behavioral assessments immediately after each interview.
                  </p>
                </div>
              </Transition>
            </div>
            
            <!-- FAQ Item 4 -->
            <div class="border border-gray-200 rounded-lg">
              <button 
                @click="toggleFAQ(3)"
                class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span class="font-semibold text-gray-900">Will this replace recruiters?</span>
                <svg 
                  class="w-5 h-5 text-gray-500 transition-transform"
                  :class="{ 'rotate-180': openItems[3] }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <Transition name="faq-fade">
                <div v-if="openItems[3]" class="px-6 pb-4">
                  <p class="text-gray-600">
                    No, NoaMetrics is designed to augment and empower recruiters, not replace them. Our AI handles the 
                    time-consuming tasks of initial screening and fraud detection, allowing recruiters to focus on 
                    high-value activities like building relationships and making final hiring decisions based on cultural fit 
                    and team dynamics.
                  </p>
                </div>
              </Transition>
            </div>
          </div>
        </div>
      </div>
    </section>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'

const openItems = ref({})

const toggleFAQ = (index) => {
  openItems.value[index] = !openItems.value[index]
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
.faq-fade-enter-active, .faq-fade-leave-active {
  transition: all 0.4s cubic-bezier(.4,0,.2,1);
}
.faq-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.faq-fade-enter-to {
  opacity: 1;
  transform: none;
}
.faq-fade-leave-from {
  opacity: 1;
  transform: none;
}
.faq-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style> 