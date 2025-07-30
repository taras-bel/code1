<template>
  <Transition name="section-fade" appear>
    <section id="benefits" class="py-16 md:py-20 bg-white">
      <div class="container-custom">
        <!-- Features Grid -->
        <TransitionGroup name="card-fade" tag="div" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-12 mb-12 md:mb-16">
          <div v-for="(feature, idx) in features" :key="idx" class="text-left bg-gray-50 rounded-lg card-fade-item">
            <div class="w-full h-48 md:h-56 bg-gray-300 rounded-lg mb-6 flex items-center justify-center">
              <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h3 class="text-lg md:text-xl font-bold text-gray-900 mb-2 px-2 py-2">
              {{ feature }}
            </h3>
          </div>
        </TransitionGroup>
        <!-- CTA Button -->
        <div class="text-center">
          <button class="bg-gray-900 hover:bg-black text-white px-8 md:px-12 py-4 rounded-lg font-semibold text-base md:text-lg transition-all duration-200 shadow-lg hover:shadow-xl">
            <span class="mr-3">▷</span>
            TBD: Play 90-sec Product Walk-Through
          </button>
        </div>
      </div>
    </section>
  </Transition>
</template>

<script setup>
const features = [
  'Match candidates 94% faster',
  'Catch fake resumes before interviews',
  'See your best candidates at a glance',
  'Trigger auto-screen calls or add to video AI.'
]
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
.card-fade-enter-active, .card-fade-leave-active {
  transition: all 0.6s cubic-bezier(.4,0,.2,1);
}
.card-fade-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
.card-fade-enter-to {
  opacity: 1;
  transform: none;
}
.card-fade-leave-from {
  opacity: 1;
  transform: none;
}
.card-fade-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
</style> 