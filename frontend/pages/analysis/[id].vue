<template>
  <div class="container-custom py-12">
    <div v-if="loading" class="text-center py-12 text-lg text-gray-500">
      Loading analysis...
    </div>
    
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-600 text-xl mb-4">❌ {{ error }}</div>
      <button 
        @click="goBack"
        class="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition"
      >
        Go Back
      </button>
    </div>
    
    <div v-else-if="analysis">
      <!-- Header -->
      <div class="mb-8">
        <button 
          @click="goBack"
          class="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition"
        >
          <span class="mr-2">←</span>
          Back to Dashboard
        </button>
        
        <div class="flex justify-between items-start">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
              Candidate Analysis
            </h1>
            <p class="text-gray-600">
              Analysis ID: {{ analysis.id }}
            </p>
            <p class="text-gray-600">
              Created: {{ formatDate(analysis.created_at) }}
            </p>
          </div>
          
          <div class="text-right">
            <div class="text-sm text-gray-500 mb-1">Status</div>
            <span 
              class="px-3 py-1 rounded-full text-sm font-semibold"
              :class="getStatusColor(analysis.status)"
            >
              {{ analysis.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- Job Description -->
      <div v-if="analysis.job_description" class="bg-blue-50 rounded-2xl p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Job Description</h2>
        <div class="text-gray-700 whitespace-pre-wrap">{{ analysis.job_description }}</div>
      </div>

      <!-- Analysis Results -->
      <div v-if="analysis.results && analysis.status === 'completed'">
        <!-- Overall Score Card -->
        <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-8 mb-8 text-white">
          <div class="text-center">
            <h2 class="text-2xl font-bold mb-2">Overall Assessment</h2>
            <div class="text-6xl font-bold mb-4">{{ analysis.results.overall_score }}/100</div>
            <div class="text-xl opacity-90">{{ getScoreDescription(analysis.results.overall_score) }}</div>
          </div>
        </div>

        <!-- Candidate Analysis Card -->
        <CandidateAnalysisCard :candidate="candidateData" />

        <!-- Detailed Analysis -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Experience Details -->
          <div v-if="analysis.results.experience" class="bg-white rounded-2xl shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4">Work Experience</h3>
            <div class="space-y-4">
              <div 
                v-for="(exp, index) in analysis.results.experience" 
                :key="index"
                class="border-l-4 border-blue-500 pl-4"
              >
                <div class="font-semibold text-gray-900">{{ exp.position }}</div>
                <div class="text-blue-600">{{ exp.company }}</div>
                <div class="text-sm text-gray-600 mb-2">{{ exp.duration }}</div>
                <ul class="text-sm text-gray-700 space-y-1">
                  <li 
                    v-for="(resp, respIndex) in exp.responsibilities" 
                    :key="respIndex"
                    class="flex items-start"
                  >
                    <span class="text-blue-500 mr-2">•</span>
                    <span>{{ resp }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Education Details -->
          <div v-if="analysis.results.education" class="bg-white rounded-2xl shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4">Education</h3>
            <div class="space-y-4">
              <div 
                v-for="(edu, index) in analysis.results.education" 
                :key="index"
                class="border-l-4 border-green-500 pl-4"
              >
                <div class="font-semibold text-gray-900">{{ edu.degree }}</div>
                <div class="text-green-600">{{ edu.institution }}</div>
                <div class="text-sm text-gray-600">{{ edu.year }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Additional Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
          <div v-if="analysis.results.salary_expectation" class="bg-white rounded-2xl shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4">Salary Expectations</h3>
            <div class="text-gray-700">{{ analysis.results.salary_expectation }}</div>
          </div>

          <div v-if="analysis.results.availability" class="bg-white rounded-2xl shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-900 mb-4">Availability</h3>
            <div class="text-gray-700">{{ analysis.results.availability }}</div>
          </div>
        </div>

        <!-- Analysis Metadata -->
        <div v-if="analysis.results.analysis_metadata" class="mt-8 bg-gray-50 rounded-2xl p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-4">Analysis Details</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600">{{ analysis.results.analysis_metadata.total_files }}</div>
              <div class="text-sm text-gray-600">Files Analyzed</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600">{{ analysis.results.analysis_metadata.file_types.join(', ') }}</div>
              <div class="text-sm text-gray-600">File Types</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-purple-600">{{ analysis.processing_time || 'N/A' }}s</div>
              <div class="text-sm text-gray-600">Processing Time</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-orange-600">
                {{ analysis.results.analysis_metadata.job_description_provided ? 'Yes' : 'No' }}
              </div>
              <div class="text-sm text-gray-600">Job Description Provided</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="analysis.error_message" class="bg-red-50 rounded-2xl p-6">
        <h3 class="text-xl font-bold text-red-900 mb-4">Analysis Error</h3>
        <div class="text-red-700">{{ analysis.error_message }}</div>
        <button 
          @click="retryAnalysis"
          class="mt-4 bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
        >
          Retry Analysis
        </button>
      </div>

      <!-- Processing State -->
      <div v-else-if="analysis.status === 'processing'" class="text-center py-12">
        <div class="text-lg text-gray-500 mb-4">Analysis in progress...</div>
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      </div>

      <!-- Pending State -->
      <div v-else-if="analysis.status === 'pending'" class="text-center py-12">
        <div class="text-lg text-gray-500 mb-4">Analysis pending...</div>
        <button 
          @click="runAnalysis"
          class="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition"
        >
          Start Analysis
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApiFactory } from '~/composables/useApi'

const route = useRoute()
const router = useRouter()
const useApi = useApiFactory()

const loading = ref(true)
const error = ref('')
const analysis = ref<any>(null)

// Computed properties
const candidateData = computed(() => {
  if (!analysis.value?.results) return null
  
  const results = analysis.value.results
  return {
    id: analysis.value.id,
    name: results.summary?.split(' ').slice(0, 2).join(' ') || 'Candidate',
    summary: results.summary || '',
    overall_score: results.overall_score || 0,
    skills_score: results.skills_score || 0,
    experience_score: results.experience_score || 0,
    education_score: results.education_score || 0,
    match_score: results.match_score || 0,
    experience_years: results.experience_years || 0,
    recommendation: results.recommendation || '',
    technical_skills: results.skills?.technical || [],
    soft_skills: results.skills?.soft || [],
    languages: results.skills?.languages || [],
    strengths: results.strengths || [],
    weaknesses: results.weaknesses || [],
    score_breakdown: results.score_breakdown || {}
  }
})

// Load analysis data
onMounted(async () => {
  const analysisId = route.params.id as string
  
  try {
    const response = await useApi(`http://localhost:8000/api/v1/analysis/${analysisId}`)
    analysis.value = response
  } catch (e: any) {
    error.value = e.message || 'Failed to load analysis'
  } finally {
    loading.value = false
  }
})

// Utility functions
function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getStatusColor(status: string): string {
  switch (status) {
    case 'completed': return 'bg-green-100 text-green-700'
    case 'processing': return 'bg-blue-100 text-blue-700'
    case 'pending': return 'bg-yellow-100 text-yellow-700'
    case 'failed': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

function getScoreDescription(score: number): string {
  if (score >= 90) return 'Excellent - Highly Recommended'
  if (score >= 70) return 'Good - Recommended'
  if (score >= 50) return 'Average - Consider'
  return 'Below Average - Not Recommended'
}

function goBack() {
  router.push('/dashboard')
}

async function retryAnalysis() {
  if (!analysis.value) return
  
  try {
    await useApi(`http://localhost:8000/api/v1/analysis/${analysis.value.id}/retry`, {
      method: 'POST'
    })
    
    // Reload the analysis
    const response = await useApi(`http://localhost:8000/api/v1/analysis/${analysis.value.id}`)
    analysis.value = response
  } catch (e: any) {
    error.value = e.message || 'Failed to retry analysis'
  }
}

async function runAnalysis() {
  if (!analysis.value) return
  
  try {
    await useApi(`http://localhost:8000/api/v1/analysis/${analysis.value.id}/run`, {
      method: 'POST'
    })
    
    // Reload the analysis
    const response = await useApi(`http://localhost:8000/api/v1/analysis/${analysis.value.id}`)
    analysis.value = response
  } catch (e: any) {
    error.value = e.message || 'Failed to run analysis'
  }
}
</script>

<style scoped>
/* Additional styles if needed */
</style> 