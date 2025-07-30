<template>
  <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
    <!-- Header -->
    <div class="flex justify-between items-start mb-6">
      <div>
        <h3 class="text-xl font-bold text-gray-900">{{ candidate.name }}</h3>
        <p class="text-gray-600 mt-1">{{ candidate.summary }}</p>
      </div>
      <div class="text-right">
        <div class="text-3xl font-bold" :class="getScoreTextColor(candidate.overall_score)">
          {{ candidate.overall_score }}/100
        </div>
        <div class="text-sm text-gray-500">Overall Score</div>
      </div>
    </div>

    <!-- Score Bars -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <div class="space-y-3">
        <div>
          <div class="flex justify-between text-sm mb-1">
            <span class="font-medium">Skills Score</span>
            <span class="font-bold" :class="getScoreTextColor(candidate.skills_score)">
              {{ candidate.skills_score }}/100
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getScoreColor(candidate.skills_score)"
              :style="{ width: `${candidate.skills_score}%` }"
            ></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between text-sm mb-1">
            <span class="font-medium">Experience Score</span>
            <span class="font-bold" :class="getScoreTextColor(candidate.experience_score)">
              {{ candidate.experience_score }}/100
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getScoreColor(candidate.experience_score)"
              :style="{ width: `${candidate.experience_score}%` }"
            ></div>
          </div>
        </div>

        <div>
          <div class="flex justify-between text-sm mb-1">
            <span class="font-medium">Education Score</span>
            <span class="font-bold" :class="getScoreTextColor(candidate.education_score)">
              {{ candidate.education_score }}/100
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getScoreColor(candidate.education_score)"
              :style="{ width: `${candidate.education_score}%` }"
            ></div>
          </div>
        </div>

        <div v-if="candidate.match_score">
          <div class="flex justify-between text-sm mb-1">
            <span class="font-medium">Match Score</span>
            <span class="font-bold" :class="getScoreTextColor(candidate.match_score)">
              {{ candidate.match_score }}/100
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getScoreColor(candidate.match_score)"
              :style="{ width: `${candidate.match_score}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Experience Info -->
      <div class="space-y-3">
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Experience</h4>
          <div class="text-2xl font-bold text-blue-600">{{ candidate.experience_years }} years</div>
          <div class="text-sm text-gray-600">Total experience</div>
        </div>

        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Recommendation</h4>
          <div class="text-sm text-gray-700">{{ candidate.recommendation }}</div>
        </div>
      </div>
    </div>

    <!-- Skills Section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div>
        <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
          <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
          Technical Skills
        </h4>
        <div class="space-y-2">
          <span 
            v-for="skill in candidate.technical_skills" 
            :key="skill"
            class="inline-block bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium mr-2 mb-2"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <div>
        <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
          <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
          Soft Skills
        </h4>
        <div class="space-y-2">
          <span 
            v-for="skill in candidate.soft_skills" 
            :key="skill"
            class="inline-block bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium mr-2 mb-2"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <div>
        <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
          <span class="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
          Languages
        </h4>
        <div class="space-y-2">
          <span 
            v-for="language in candidate.languages" 
            :key="language"
            class="inline-block bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium mr-2 mb-2"
          >
            {{ language }}
          </span>
        </div>
      </div>
    </div>

    <!-- Strengths & Weaknesses -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
          <span class="w-2 h-2 bg-emerald-500 rounded-full mr-2"></span>
          Strengths
        </h4>
        <ul class="space-y-2">
          <li 
            v-for="strength in candidate.strengths" 
            :key="strength"
            class="flex items-start"
          >
            <span class="text-emerald-500 mr-2">✓</span>
            <span class="text-sm text-gray-700">{{ strength }}</span>
          </li>
        </ul>
      </div>

      <div>
        <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
          <span class="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
          Areas for Improvement
        </h4>
        <ul class="space-y-2">
          <li 
            v-for="weakness in candidate.weaknesses" 
            :key="weakness"
            class="flex items-start"
          >
            <span class="text-orange-500 mr-2">⚠</span>
            <span class="text-sm text-gray-700">{{ weakness }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Score Breakdown -->
    <div v-if="candidate.score_breakdown" class="mt-6 pt-6 border-t border-gray-200">
      <h4 class="font-semibold text-gray-900 mb-4">Detailed Score Breakdown</h4>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div 
          v-for="(score, key) in candidate.score_breakdown" 
          :key="key"
          class="text-center"
        >
          <div class="text-lg font-bold" :class="getScoreTextColor(score)">
            {{ score }}/100
          </div>
          <div class="text-xs text-gray-600 capitalize">
            {{ key.replace(/_/g, ' ') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Candidate {
  id: string
  name: string
  summary: string
  overall_score: number
  skills_score: number
  experience_score: number
  education_score: number
  match_score?: number
  experience_years: number
  recommendation: string
  technical_skills: string[]
  soft_skills: string[]
  languages: string[]
  strengths: string[]
  weaknesses: string[]
  score_breakdown?: Record<string, number>
}

interface Props {
  candidate: Candidate
}

const props = defineProps<Props>()

// Utility functions for score colors
function getScoreColor(score: number): string {
  if (score >= 90) return 'bg-emerald-500'
  if (score >= 70) return 'bg-blue-500'
  if (score >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

function getScoreTextColor(score: number): string {
  if (score >= 90) return 'text-emerald-600'
  if (score >= 70) return 'text-blue-600'
  if (score >= 50) return 'text-yellow-600'
  return 'text-red-600'
}
</script>

<style scoped>
/* Additional styles if needed */
</style> 