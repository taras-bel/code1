<template>
  <div class="container-custom py-12">
    <!-- Confirmation Modal -->
    <div v-if="showConfirmModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-sm w-full text-center border border-gray-100" style="font-family: inherit;">
        <h2 class="text-2xl font-bold mb-3 text-gray-900">Clear Dashboard?</h2>
        <p class="mb-7 text-gray-600 text-base">Are you sure you want to clear the dashboard? This action cannot be undone.</p>
        <div class="flex justify-center gap-4">
          <button @click="onConfirmClear" class="px-6 py-2 bg-primary-600 text-white rounded-lg font-semibold text-base shadow hover:bg-primary-700 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500">Confirm</button>
          <button @click="onCancelClear" class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold text-base shadow hover:bg-gray-200 transition-colors focus:outline-none">Cancel</button>
        </div>
      </div>
    </div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-3xl md:text-4xl font-bold text-center flex-1">Candidate Analysis Dashboard</h1>
      <button
        @click="confirmClear"
        class="ml-4 flex items-center gap-2 px-4 py-2 rounded-lg bg-red-50 hover:bg-red-100 text-red-700 font-semibold shadow transition border border-red-200"
        title="Clear Dashboard"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M8 7V5a2 2 0 012-2h2a2 2 0 012 2v2" /></svg>
        <span>Clear</span>
      </button>
    </div>
    <transition name="fade" mode="out-in">
      <div>
        <div v-if="loading" class="flex flex-col items-center justify-center py-24">
          <svg class="animate-spin h-12 w-12 text-primary-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
          </svg>
          <div class="text-lg text-gray-500">Loading candidates...</div>
        </div>
        <div v-else>
          <!-- Tabs -->
          <div class="flex justify-center mb-8">
            <div class="inline-flex rounded-lg bg-gray-100 p-1">
              <button
                v-for="tab in tabs"
                :key="tab.key"
                @click="activeTab = tab.key"
                :class="[
                  'px-6 py-2 rounded-lg font-semibold focus:outline-none transition',
                  activeTab === tab.key ? 'bg-primary-600 text-white shadow' : 'text-gray-700 hover:bg-primary-50'
                ]"
              >
                <span v-if="tab.key === 'achievers'" class="mr-2">🏆</span>
                <span v-else-if="tab.key === 'requirements'" class="mr-2">📋</span>
                <span v-else-if="tab.key === 'differences'" class="mr-2">✨</span>
                {{ tab.name }}
              </button>
            </div>
          </div>
          <div v-if="activeTab === 'achievers'">
            <div v-if="!candidates.length" class="text-center text-gray-400 py-12">
              <span class="text-5xl block mb-4">🕵️‍♂️</span>
              <span class="text-lg">No candidates found</span>
            </div>
            <div v-else class="overflow-x-auto bg-white rounded-2xl shadow p-6 mb-8 animate-fade-in">
              <table class="min-w-full text-sm text-left">
                <thead>
                  <tr class="border-b">
                    <th class="py-2 px-4 font-semibold">
                      Full Name
                      <span class="ml-1 cursor-pointer" title="Candidate's full name">ℹ️</span>
                    </th>
                    <th class="py-2 px-4 font-semibold">
                      Relevance %
                      <span class="ml-1 cursor-pointer" title="How much the candidate matches the requirements">ℹ️</span>
                    </th>
                    <th class="py-2 px-4 font-semibold">
                      Payment
                      <span class="ml-1 cursor-pointer" title="Expected payment or salary">💵</span>
                    </th>
                    <th class="py-2 px-4 font-semibold">
                      Achievements
                      <span class="ml-1 cursor-pointer" title="Number of achievements">🏅</span>
                    </th>
                    <th class="py-2 px-4 font-semibold">
                      Skills
                      <span class="ml-1 cursor-pointer" title="Number of key skills">⭐</span>
                    </th>
                    <th class="py-2 px-4 font-semibold">
                      Growth
                      <span class="ml-1 cursor-pointer" title="Career growth (responsibility increases)">📈</span>
                    </th>
                    <th class="py-2 px-4 font-semibold">
                      Experience
                      <span class="ml-1 cursor-pointer" title="Total years of experience">⏳</span>
                    </th>
                    <th class="py-2 px-4 font-semibold">
                      Score
                      <span class="ml-1 cursor-pointer" title="Total candidate score">🎯</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in candidates" :key="c.full_name" class="border-b hover:bg-primary-50 transition duration-200">
                    <td class="py-2 px-4 font-medium truncate max-w-xs" :title="c.full_name">{{ c.full_name }}</td>
                    <td class="py-2 px-4">
                      <span
                        class="px-2 py-1 rounded text-xs font-semibold"
                        :class="getRelevanceBadgeColor(c.relevance_percent)"
                      >
                        {{ c.relevance_percent ? c.relevance_percent + '%' : '—' }}
                      </span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="px-2 py-1 rounded text-xs font-semibold bg-gray-100 text-gray-700">
                        {{ c.payment ? ('$' + c.payment) : '—' }}
                      </span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-700">{{ c.achievements }}</span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="px-2 py-1 rounded text-xs font-semibold bg-blue-100 text-blue-700">{{ c.skills }}</span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="px-2 py-1 rounded text-xs font-semibold bg-yellow-100 text-yellow-700">{{ c.growth }}</span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="px-2 py-1 rounded text-xs font-semibold bg-orange-100 text-orange-700">{{ c.experience }} yrs</span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="font-bold text-lg" :class="getScoreTextColor(c.score)">{{ c.score }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else-if="activeTab === 'differences'">
            <div v-if="!candidates.length" class="text-center text-gray-400 py-12">
              <span class="text-5xl block mb-4">✨</span>
              <span class="text-lg">No candidates found</span>
            </div>
            <div v-else class="overflow-x-auto bg-white rounded-2xl shadow p-6 mb-8 animate-fade-in">
              <table class="min-w-full text-sm text-left">
                <thead>
                  <tr class="border-b">
                    <th class="py-2 px-4 font-semibold">Candidate</th>
                    <th class="py-2 px-4 font-semibold">Unique Skills</th>
                    <th class="py-2 px-4 font-semibold">Certifications</th>
                    <th class="py-2 px-4 font-semibold">Education & Specialization</th>
                    <th class="py-2 px-4 font-semibold">Unique Experience</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in candidates" :key="c.full_name" class="border-b hover:bg-primary-50 transition duration-200">
                    <td class="py-2 px-4 font-medium truncate max-w-xs" :title="c.full_name">{{ c.full_name }}</td>
                    <td class="py-2 px-4">
                      <span v-for="s in (typeof c.unique_skills === 'string' ? c.unique_skills.split(',').map(s => s.trim()).filter(s => s) : [])" :key="s" class="inline-block bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-semibold mr-1 mb-1">{{ s }}</span>
                    </td>
                    <td class="py-2 px-4">
                      <span v-for="cert in (typeof c.certifications === 'string' ? c.certifications.split(',').map(s => s.trim()).filter(s => s) : [])" :key="cert" class="inline-block bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs font-semibold mr-1 mb-1">{{ cert }}</span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="inline-block bg-emerald-100 text-emerald-700 px-2 py-1 rounded text-xs font-semibold mr-1 mb-1">{{ c.education }}</span>
                      <span class="inline-block bg-cyan-100 text-cyan-700 px-2 py-1 rounded text-xs font-semibold mr-1 mb-1">{{ c.specialization }}</span>
                    </td>
                    <td class="py-2 px-4">
                      <span class="inline-block bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-semibold mr-1 mb-1">{{ c.unique_experience }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else-if="activeTab === 'requirements'">
            <div v-if="!candidates.length" class="text-center text-gray-400 py-12">
              <span class="text-5xl block mb-4">📋</span>
              <span class="text-lg">No candidates found</span>
            </div>
            <div v-else class="overflow-x-auto bg-white rounded-2xl shadow p-6 mb-8 animate-fade-in">
              <table class="min-w-full text-sm text-left">
                <thead>
                  <tr class="border-b">
                    <th class="py-2 px-4 font-semibold">Requirement</th>
                    <th v-for="c in candidates" :key="c.full_name" class="py-2 px-4 font-semibold">{{ c.full_name }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(req, reqKey) in Object.keys(requirements)" :key="reqKey" class="border-b hover:bg-primary-50 transition duration-200">
                    <td class="py-2 px-4 font-medium">{{ req }}</td>
                    <td v-for="c in candidates" :key="c.full_name" class="py-2 px-4">
                      <span class="px-2 py-1 rounded text-xs font-semibold border" :class="getRequirementBadgeColor(requirements[req]?.[c.full_name] || 0)">
                        {{ getRequirementScore(requirements[req]?.[c.full_name] || 0) }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Статистика -->
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mt-8">
            <div class="bg-green-50 rounded-xl p-6 flex flex-col items-center shadow animate-fade-in">
              <div class="text-3xl font-bold text-green-600 flex items-center gap-2">
                <span>👥</span>{{ candidates.length }}
              </div>
              <div class="text-gray-700 mt-2">Total Candidates</div>
            </div>
            <div class="bg-blue-50 rounded-xl p-6 flex flex-col items-center shadow animate-fade-in">
              <div class="text-3xl font-bold text-blue-600 flex items-center gap-2">
                <span>📊</span>{{ avgScore }}
              </div>
              <div class="text-gray-700 mt-2">Avg Score</div>
            </div>
            <div class="bg-purple-50 rounded-xl p-6 flex flex-col items-center shadow animate-fade-in">
              <div class="text-3xl font-bold text-purple-600 flex items-center gap-2">
                <span>🏆</span>{{ topScore }}
              </div>
              <div class="text-gray-700 mt-2">Top Performer</div>
            </div>
            <div class="bg-orange-50 rounded-xl p-6 flex flex-col items-center shadow animate-fade-in">
              <div class="text-3xl font-bold text-orange-600 flex items-center gap-2">
                <span>⏳</span>{{ avgExperience }}
              </div>
              <div class="text-gray-700 mt-2">Avg Experience</div>
            </div>
          </div>

        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Define types for better type safety
interface AnalysisResult {
  experience_summary: {
    full_name?: string
    payment_expectations?: string
    skills_1_plus_years?: string
    certifications?: string
    education_degree?: string
    education_major?: string
    education_university?: string
    desired_role?: string
    professional_summary?: string
    years_of_experience?: number
  }
  achievers_rating: {
    overall_score?: number
    achievements?: { score?: number }
    skills?: { score?: number }
    responsibilities?: { total_score?: number }
  }
  match_score?: number
}

interface Analysis {
  id: string
  status: string
  created_at: string
  results?: AnalysisResult
}

interface Candidate {
  id: string
  full_name: string
  score: number
  overall_score: number
  relevance_percent: number
  payment: string
  achievements: number
  skills: number
  growth: number
  experience: number
  experience_years: number
  unique_skills: string
  certifications: string
  education: string[]
  specialization: string
  unique_experience: string
}

const tabs = [
  { name: 'Achievers', key: 'achievers' },
  { name: 'Relevant for Requirements', key: 'requirements' },
  { name: 'Differences', key: 'differences' }
]
const activeTab = ref('achievers')
const loading = ref(true)
const candidates = ref<Candidate[]>([])
const requirements = ref<Record<string, Record<string, number>>>({})
const differences = ref<string[]>([])

const avgScore = ref(0)
const topScore = ref(0)
const avgExperience = ref(0)

async function fetchDashboardData() {
  loading.value = true
  try {
    // Get user token
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.error('No access token found')
      loading.value = false
      return
    }

    // 1. Get user's analyses from API using the working endpoint
    const config = useRuntimeConfig()
    const apiBaseUrl = config.public.apiBaseUrl
    
    const analysesRes = await fetch(`${apiBaseUrl}/api/v1/analysis/user/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    let analysesData
    if (!analysesRes.ok) {
      console.error('Failed to fetch analyses:', analysesRes.statusText)
      // Fallback to demo data if API is not available
      console.log('Using fallback demo data')
      analysesData = {
        analyses: [
          {
            id: "1",
            status: "completed",
            results: {
              experience_summary: {
                full_name: "John Doe",
                payment_expectations: "$80,000",
                skills_1_plus_years: "Python, React, AWS, Docker",
                certifications: "AWS Certified",
                education_degree: "BS",
                education_major: "Computer Science",
                education_university: "MIT",
                desired_role: "Software Engineering",
                professional_summary: "Startup experience",
                years_of_experience: 5
              },
              achievers_rating: {
                overall_score: 85,
                achievements: { score: 5 },
                skills: { score: 8 },
                responsibilities: { total_score: 3 }
              },
              match_score: 0.88
            }
          },
          {
            id: "2",
            status: "completed",
            results: {
              experience_summary: {
                full_name: "Jane Smith",
                payment_expectations: "$95,000",
                skills_1_plus_years: "Machine Learning, Data Science, Python, TensorFlow",
                certifications: "Google Cloud Certified",
                education_degree: "MS",
                education_major: "Data Science",
                education_university: "Stanford",
                desired_role: "Data Engineering",
                professional_summary: "Enterprise experience",
                years_of_experience: 7
              },
              achievers_rating: {
                overall_score: 92,
                achievements: { score: 7 },
                skills: { score: 10 },
                responsibilities: { total_score: 4 }
              },
              match_score: 0.95
            }
          }
        ]
      }
    } else {
      analysesData = await analysesRes.json()
    }
    
    // 2. Transform analyses data to candidates format for dashboard
    const analyses: Analysis[] = analysesData.analyses || []
    
    // Filter only completed CV analyses (exclude job descriptions)
    const completedAnalyses = analyses
      .filter((analysis: Analysis) => {
        // Must be completed and have results
        if (analysis.status !== 'completed' || !analysis.results) return false
        
        const results = analysis.results!
        const experience_summary = results.experience_summary || {}
        const achievers_rating = results.achievers_rating || {}
        
        // Must have experience_summary and achievers_rating (CV characteristics)
        if (!experience_summary || !achievers_rating) return false
        
        // Must have a valid full_name
        const candidateName = experience_summary.full_name
        if (!candidateName || candidateName === 'Unknown' || candidateName === 'Not specified' || candidateName.trim() === '') return false
        
        // Exclude job description-like names
        const nameLower = candidateName.toLowerCase()
        const jobKeywords = ['job', 'position', 'role', 'vacancy', 'opening', 'description', 'requirements', 'hiring']
        if (jobKeywords.some(keyword => nameLower.includes(keyword))) return false
        
        return true
      })
      .sort((a: Analysis, b: Analysis) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    
    // Take only the latest 5 analyses (or however many were just uploaded)
    const latestAnalyses = completedAnalyses.slice(0, 5)
    
    console.log(`Found ${completedAnalyses.length} total analyses, showing latest ${latestAnalyses.length}`)
    
    const transformedCandidates: Candidate[] = latestAnalyses.map((analysis: Analysis) => {
        const results = analysis.results!
        const experience_summary = results.experience_summary || {}
        const achievers_rating = results.achievers_rating || {}
        
        return {
          id: analysis.id,
          full_name: experience_summary.full_name || 'Unknown',
          score: achievers_rating.overall_score || 0,
          overall_score: achievers_rating.overall_score || 0,
          relevance_percent: results.match_score || 0,
          payment: experience_summary.payment_expectations || '',
          achievements: achievers_rating.achievements?.score || 0,
          skills: achievers_rating.skills?.score || 0,
          growth: achievers_rating.responsibilities?.total_score || 0,
          experience: Number(experience_summary.years_of_experience) || 6, // Fallback to 6 years if not specified
          experience_years: Number(experience_summary.years_of_experience) || 6, // Fallback to 6 years if not specified
          unique_skills: experience_summary.skills_1_plus_years || '',
          certifications: Array.isArray(experience_summary.certifications) ? experience_summary.certifications.join(', ') : (experience_summary.certifications || ''),
          education: [
            experience_summary.education_degree,
            experience_summary.education_major,
            experience_summary.education_university
          ].filter((item): item is string => Boolean(item)),
          specialization: experience_summary.desired_role || '',
          unique_experience: experience_summary.professional_summary || ''
        }
      })
    
    // 3. Generate requirements comparison and key differentiators
    const requirementsComparison: Record<string, Record<string, number>> = {}
    const keyDifferentiators: string[] = []
    
    // Initialize requirements comparison with all candidates
    transformedCandidates.forEach((candidate: Candidate) => {
      console.log(`Processing candidate: ${candidate.full_name}`)
      console.log(`Skills: ${candidate.unique_skills}`)
      console.log(`Score: ${candidate.overall_score}`)
      
      // Add skills to requirements comparison
      if (candidate.unique_skills && typeof candidate.unique_skills === 'string') {
        const skills = candidate.unique_skills.split(',').map((s: string) => s.trim()).filter((s: string) => s)
        console.log(`Parsed skills: ${skills}`)
        
        skills.forEach((skill: string) => {
          if (!requirementsComparison[skill]) {
            requirementsComparison[skill] = {}
          }
          requirementsComparison[skill][candidate.full_name] = candidate.overall_score || 0
          console.log(`Added skill ${skill} for ${candidate.full_name} with score ${candidate.overall_score}`)
        })
      } else {
        console.log(`No skills found for ${candidate.full_name}`)
      }
      
      // Add key differentiators
      if (candidate.unique_experience) {
        keyDifferentiators.push(`${candidate.full_name}: ${candidate.unique_experience.substring(0, 100)}...`)
      }
    })
    
    // Ensure all candidates have entries for all skills (even if they don't have that skill)
    const allSkills = Object.keys(requirementsComparison)
    const allCandidateNames = transformedCandidates.map(c => c.full_name)
    
    allSkills.forEach(skill => {
      allCandidateNames.forEach(candidateName => {
        if (!requirementsComparison[skill][candidateName]) {
          requirementsComparison[skill][candidateName] = 0
        }
      })
    })
    
    // 4. Set dashboard data
    candidates.value = transformedCandidates
    requirements.value = requirementsComparison
    differences.value = keyDifferentiators
    
    // Debug logging
    console.log('Dashboard data:', {
      candidates: transformedCandidates.length,
      candidateNames: transformedCandidates.map(c => c.full_name),
      requirements: Object.keys(requirementsComparison).length,
      requirementsKeys: Object.keys(requirementsComparison),
      differences: keyDifferentiators.length
    })
    
    // Debug requirements data
    console.log('Requirements comparison details:')
    Object.entries(requirementsComparison).forEach(([skill, candidates]) => {
      console.log(`Skill: ${skill}`, candidates)
    })
    
    // Debug candidate skills
    transformedCandidates.forEach(candidate => {
      console.log(`Candidate ${candidate.full_name} skills:`, candidate.unique_skills)
    })

    // 3. Calculate statistics
    const scores = candidates.value.map(c => Number(c.overall_score || c.score) || 0)
    avgScore.value = scores.length ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1) : 0
    topScore.value = scores.length ? Math.max(...scores) : 0
    // Debug experience calculation
    const experienceValues = candidates.value.map(c => {
      const exp = Number(c.experience_years || c.experience) || 0
      console.log(`Candidate ${c.full_name}: experience_years=${c.experience_years}, experience=${c.experience}, calculated=${exp}`)
      return exp
    })
    console.log('Experience values:', experienceValues)
    
    avgExperience.value = candidates.value.length ? (
      experienceValues.reduce((a, b) => a + b, 0) / candidates.value.length
    ).toFixed(1) : 0
    
    console.log('Avg Experience calculated:', avgExperience.value)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchDashboardData)

// Utility functions for score colors
function getScoreColor(score: number): string {
  if (score >= 90) return 'bg-emerald-500'
  if (score >= 70) return 'bg-blue-500'
  if (score >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

function getScoreTextColor(score: number): string {
  if (score >= 25) return 'text-emerald-600'
  if (score >= 15) return 'text-blue-600'
  if (score >= 10) return 'text-orange-600'
  return 'text-red-600'
}

function getScoreBadgeColor(score: number): string {
  if (score >= 25) return 'bg-emerald-100 text-emerald-700'
  if (score >= 15) return 'bg-blue-100 text-blue-700'
  if (score >= 10) return 'bg-orange-100 text-orange-700'
  return 'bg-red-100 text-red-700'
}

function getRequirementScore(score: number): string {
  if (score >= 15) return 'Strong Yes'
  if (score >= 10) return 'Yes'
  if (score >= 5) return 'Partial'
  if (score >= 1) return 'Weak'
  return 'No'
}

function getRequirementBadgeColor(score: number): string {
  if (score >= 15) return 'bg-emerald-100 text-emerald-700 border-emerald-200'
  if (score >= 10) return 'bg-blue-100 text-blue-700 border-blue-200'
  if (score >= 5) return 'bg-yellow-100 text-yellow-700 border-yellow-200'
  if (score >= 1) return 'bg-orange-100 text-orange-700 border-orange-200'
  return 'bg-red-100 text-red-700 border-red-200'
}

function getRelevanceBadgeColor(percent: number): string {
  if (percent >= 90) return 'bg-emerald-100 text-emerald-700'
  if (percent >= 70) return 'bg-blue-100 text-blue-700'
  if (percent >= 50) return 'bg-yellow-100 text-yellow-700'
  return 'bg-red-100 text-red-700'
}

function getNested(obj: any, path: string[], fallback: any = 0) {
  return path.reduce((acc, key) => (acc && acc[key] !== undefined ? acc[key] : undefined), obj) ?? fallback;
}

const showConfirm = ref(false)



const HIDDEN_ANALYSES_KEY = 'hidden_analyses_ids'

function getHiddenAnalyses() {
  try {
    const ids = localStorage.getItem(HIDDEN_ANALYSES_KEY)
    return ids ? JSON.parse(ids) : []
  } catch {
    return []
  }
}

function setHiddenAnalyses(ids: string[]) {
  localStorage.setItem(HIDDEN_ANALYSES_KEY, JSON.stringify(ids))
}

// Navigation function
function viewAnalysis(analysisId: string) {
  window.location.href = `/analysis/${analysisId}`
}

// --- Modal logic for dashboard clear confirmation ---
const showConfirmModal = ref(false)

function confirmClear() {
  showConfirmModal.value = true
}

function onConfirmClear() {
  showConfirmModal.value = false
  clearDashboard()
}

function onCancelClear() {
  showConfirmModal.value = false
}

async function clearDashboard() {
  // No window.confirm here, just clear
  const allIds = candidates.value.map(c => c.id)
  setHiddenAnalyses([...getHiddenAnalyses(), ...allIds])
  candidates.value = []
  requirements.value = []
}
</script>

<style scoped>
.bg-primary-50 { background-color: #f5f7ff; }
.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.animate-fade-in {
  animation: fadeIn 0.7s cubic-bezier(0.4,0,0.2,1);
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
</style> 