<template>
  <Transition name="section-fade" appear>
    <section class="py-20">
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">
            Our happy clients
          </h2>
          <p class="text-xl text-gray-600">
            Lorem ipsum dolor sit amet consectetur. Condimentum sed cursus aliquam cum et morbi. Sagittis nulla
          </p>
        </div>
        <TransitionGroup name="card-fade" tag="div" class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <div v-for="client in clients" :key="client.name" class="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow card-fade-item">
            <div class="flex items-center mb-4">
              <div class="w-14 h-14 rounded-full bg-gray-300 mr-4 flex items-center justify-center">
                <span class="text-2xl font-bold text-gray-600">{{ client.initials }}</span>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">{{ client.name }}</h4>
                <p class="text-sm text-gray-600">{{ client.position }}</p>
              </div>
            </div>
            <p class="text-gray-700 leading-relaxed">
              {{ client.text }}
            </p>
          </div>
        </TransitionGroup>
        <!-- Trust Indicators -->
        <div class="mt-12 text-center">
          <p class="text-gray-600 mb-4">Trusted by leading companies</p>
          <div class="flex justify-center items-center space-x-8 opacity-50">
            <div class="w-32 h-12 bg-gray-300 rounded"></div>
            <div class="w-32 h-12 bg-gray-300 rounded"></div>
            <div class="w-32 h-12 bg-gray-300 rounded"></div>
            <div class="w-32 h-12 bg-gray-300 rounded"></div>
          </div>
        </div>
      </div>
    </section>
  </Transition>
</template>

<script setup>
const clients = [
  {
    initials: 'BW',
    name: 'Benjamin Wright',
    position: 'Director of Recruiting at Upwork',
    text: '"NoaMetrics has been invaluable for our recruiting process. Their AI-powered screening helped us save countless hours and improved our quality of hire dramatically."'
  },
  {
    initials: 'MC',
    name: 'Michael Chen',
    position: 'VP of People at TechCorp',
    text: '"Our team has saved countless hours with NoaMetrics. The fraud detection and candidate insights are a game changer for us!"'
  }
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