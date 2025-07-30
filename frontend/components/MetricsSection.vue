<template>
  <Transition name="section-fade" appear>
    <section class="py-16 md:py-20 bg-gray-50">
      <div class="container-custom">
        <!-- Metrics Grid -->
        <TransitionGroup name="card-fade" tag="div" class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 max-w-4xl mx-auto">
          <div v-for="metric in metrics" :key="metric.title" class="text-center md:text-left bg-white rounded-lg p-6 md:p-8 shadow-sm card-fade-item">
            <h3 class="text-xl md:text-2xl lg:text-2xl font-bold text-gray-900 mb-2">
              {{ metric.title }}
            </h3>
            <p class="text-gray-600 text-base md:text-lg">
              {{ metric.text }}
            </p>
          </div>
        </TransitionGroup>
      </div>
    </section>
  </Transition>
</template>

<script setup>
const metrics = [
  { title: '80% Less Screening Time', text: 'Reduced candidate screening time.' },
  { title: '4x Faster Short-List Creation', text: 'Faster short-list creation.' },
  { title: 'Up to 12% Drop in Mis-Hires', text: 'Fewer mis-hires.' },
  { title: 'Plug-and-Play with your ATS', text: 'Easy integration with your system.' }
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