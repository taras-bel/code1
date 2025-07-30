<template>
  <Transition name="section-fade" appear>
    <section class="py-20 bg-gray-50">
      <div class="container-custom">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">
            Next Step: Blast Deepfake Interviews
          </h2>
          <p class="text-xl text-gray-600">
            Automated, AI-powered screening for authentic talent verification
          </p>
        </div>
        <!-- Process Flow -->
        <TransitionGroup name="step-fade" tag="div" class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div v-for="(step, idx) in 4" :key="idx" class="flex flex-col items-center text-center step-fade-item">
            <div :class="['w-20 h-20 rounded-full flex items-center justify-center text-white font-bold text-xl',
              idx===0?'bg-purple-500':idx===1?'bg-blue-500':idx===2?'bg-orange-500':'bg-green-500']">
              {{ idx===3 ? '✓' : idx+1 }}
            </div>
            <h3 class="font-semibold mt-4 mb-2">{{ ['Shortlist','AI Video','Verification','Easy Job'][idx] }}</h3>
            <p class="text-sm text-gray-600 max-w-xs">
              {{ [
                'AI analyzes CVs and creates initial candidate pool',
                'Candidates complete AI-powered video interviews',
                'AI detects fraude and verifies authenticity',
                'Get verified, qualified candidates ready for final interviews'
              ][idx] }}
            </p>
          </div>
        </TransitionGroup>
        
        <!-- Additional Info -->
        <div class="mt-12 grid md:grid-cols-3 gap-6">
          <div class="bg-purple-50 rounded-lg p-6 text-center">
            <div class="text-3xl font-bold text-purple-600 mb-2">$324</div>
            <p class="text-gray-700">Saved per candidate</p>
          </div>
          <div class="bg-blue-50 rounded-lg p-6 text-center">
            <div class="text-3xl font-bold text-blue-600 mb-2">87%</div>
            <p class="text-gray-700">Reduction in time-to-hire</p>
          </div>
          <div class="bg-green-50 rounded-lg p-6 text-center">
            <div class="text-3xl font-bold text-green-600 mb-2">99.5%</div>
            <p class="text-gray-700">Deepfake detection accuracy</p>
          </div>
        </div>
      </div>
    </section>
  </Transition>
</template>

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
.step-fade-enter-active, .step-fade-leave-active {
  transition: all 0.6s cubic-bezier(.4,0,.2,1);
}
.step-fade-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
.step-fade-enter-to {
  opacity: 1;
  transform: none;
}
.step-fade-leave-from {
  opacity: 1;
  transform: none;
}
.step-fade-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.97);
}
</style> 