<!--
==============================================================================
COMPONENT: JoinBetaDrawer.vue
==============================================================================
PURPOSE: 
A slide-out drawer component for beta program registration that appears as an 
overlay modal. Implements a multi-field form with file upload capability, 
form validation, and success state handling. Uses Vue's Teleport for proper 
DOM positioning and Transition API for smooth animations.

OPERATING PRINCIPLE:
- Renders as a full-height drawer sliding from the right side
- Uses absolute positioning with high z-index to overlay all content
- Implements reactive form state with two-way data binding
- Handles file uploads via drag-and-drop and click interactions
- Manages loading states and success feedback
- Communicates with parent via props/events pattern
==============================================================================
-->

<template>
  <Teleport to="body">
    <!-- =================================================================== -->
    <!-- SECTION 1: BACKDROP OVERLAY                                       -->
    <!-- Purpose: Semi-transparent background that closes drawer on click   -->
    <!-- =================================================================== -->
    <Transition
      enter-active-class="transition-opacity ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black bg-opacity-50 z-40"
        @click="closeDrawer"
      ></div>
    </Transition>

    <!-- =================================================================== -->
    <!-- SECTION 2: MAIN DRAWER CONTAINER                                  -->
    <!-- Purpose: The actual drawer that slides in from the right          -->
    <!-- =================================================================== -->
    <Transition
      enter-active-class="transition-transform ease-out duration-300"
      enter-from-class="translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition-transform ease-in duration-200"
      leave-from-class="translate-x-0"
      leave-to-class="translate-x-full"
    >
      <div
        v-if="isOpen"
        class="fixed top-0 right-0 h-full w-full max-w-2xl bg-white shadow-2xl z-[60] flex flex-col"
      >
        <!-- =============================================================== -->
        <!-- SECTION 2.1: FIXED HEADER                                     -->
        <!-- Purpose: Always visible header with branding and close button -->
        <!-- =============================================================== -->
        <div class="absolute top-0 left-0 right-0 bg-white px-10 pt-8 pb-4 border-b border-gray-100 flex flex-col items-center shadow-sm" style="height: 140px; z-index: 10;">
          <!-- Close Icon -->
          <button
            @click="closeDrawer"
            class="absolute right-4 top-4 p-2 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            aria-label="Close drawer"
          >
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          <!-- Company Logo -->
          <div class="w-14 h-14 bg-primary-600 rounded-xl flex items-center justify-center mb-3">
            <svg class="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          
          <!-- Header Text and Badges -->
          <h2 class="text-2xl font-bold text-gray-900 mb-1">Join Our Beta Program</h2>
          <p class="text-gray-600 text-base mb-3 text-center max-w-lg">Be among the first to experience revolutionary interview analytics</p>
          <div class="flex gap-2 mb-2">
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">★ Early Access</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">Free Beta Period</span>
          </div>
          <div class="mt-10"></div>
        </div>

        <!-- =============================================================== -->
        <!-- SECTION 2.2: FORM CONTENT AREA                               -->
        <!-- Purpose: Main form interface with validation and UX enhancements -->
        <!-- =============================================================== -->
        <div v-if="!isSuccess" class="px-6 py-6">
          <!-- Form Header -->
          <div class="text-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Join Our Beta Program</h2>
            <p class="text-gray-600">Get early access to NoaMetrics and revolutionize your hiring process</p>
          </div>

          <!-- Progress Indicator -->
          <div class="mb-6">
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${formProgress}%` }"
              ></div>
            </div>
            <p class="text-xs text-gray-500 mt-1 text-center">
              {{ Math.round(formProgress) }}% Complete
            </p>
          </div>

          <!-- Error Summary (if form has errors) -->
          <div v-if="hasErrors && showErrorSummary" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center">
              <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <span class="text-sm text-red-700 font-medium">Please fix the following errors:</span>
            </div>
            <ul class="mt-2 text-sm text-red-600 list-disc list-inside">
              <li v-for="error in currentErrors" :key="error.field">{{ error.error }}</li>
            </ul>
          </div>

          <!-- Network Error Display -->
          <div v-if="networkError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <span class="text-sm text-red-700">{{ networkError }}</span>
              </div>
              <button 
                @click="retrySubmission" 
                class="text-sm text-red-600 underline hover:text-red-800"
              >
                Retry
              </button>
            </div>
          </div>

          <form @submit.prevent="handleSubmit" novalidate>
            <!-- Full Name Field -->
            <div class="mb-4">
              <label for="fullName" class="block text-sm font-medium text-gray-700 mb-1">
                Full Name <span class="text-red-500">*</span>
              </label>
              <input
                id="fullName"
                v-model="form.fullName"
                @blur="validateField('fullName', form.fullName)"
                @input="onFieldInput('fullName', $event.target.value)"
                type="text"
                placeholder="John Doe"
                class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                :class="getFieldClasses('fullName')"
                autocomplete="name"
              />
              <div v-if="shouldShowError('fullName')" class="mt-1 text-sm text-red-600 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                {{ getFieldError('fullName') }}
              </div>
            </div>

            <!-- Email Field -->
            <div class="mb-4">
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                Email Address <span class="text-red-500">*</span>
              </label>
              <input
                id="email"
                v-model="form.email"
                @blur="validateField('email', form.email)"
                @input="onFieldInput('email', $event.target.value)"
                type="email"
                placeholder="john@company.com"
                class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                :class="getFieldClasses('email')"
                autocomplete="email"
              />
              <div v-if="shouldShowError('email')" class="mt-1 text-sm text-red-600 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                {{ getFieldError('email') }}
              </div>
            </div>

            <!-- Phone Field -->
            <div class="mb-4">
              <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">
                Phone Number <span class="text-red-500">*</span>
              </label>
              <input
                id="phone"
                v-model="form.phone"
                @blur="validateField('phone', form.phone)"
                @input="onFieldInput('phone', $event.target.value)"
                type="tel"
                placeholder="+1 (555) 123-4567"
                class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                :class="getFieldClasses('phone')"
                autocomplete="tel"
              />
              <div v-if="shouldShowError('phone')" class="mt-1 text-sm text-red-600 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                {{ getFieldError('phone') }}
              </div>
            </div>

            <!-- Company Name Field -->
            <div class="mb-4">
              <label for="companyName" class="block text-sm font-medium text-gray-700 mb-1">
                Company Name <span class="text-red-500">*</span>
              </label>
              <input
                id="companyName"
                v-model="form.companyName"
                @blur="validateField('companyName', form.companyName)"
                @input="onFieldInput('companyName', $event.target.value)"
                type="text"
                placeholder="Acme Corp"
                class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                :class="getFieldClasses('companyName')"
                autocomplete="organization"
              />
              <div v-if="shouldShowError('companyName')" class="mt-1 text-sm text-red-600 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                {{ getFieldError('companyName') }}
              </div>
            </div>

            <!-- Role Field -->
            <div class="mb-4">
              <label for="role" class="block text-sm font-medium text-gray-700 mb-1">
                Your Role <span class="text-red-500">*</span>
              </label>
              <select
                id="role"
                v-model="form.role"
                @blur="validateField('role', form.role)"
                @change="onFieldInput('role', $event.target.value)"
                class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                :class="getFieldClasses('role')"
              >
                <option value="">Select your role</option>
                <option v-for="roleOption in VALID_ROLES" :key="roleOption" :value="roleOption">
                  {{ roleOption }}
                </option>
              </select>
              <div v-if="shouldShowError('role')" class="mt-1 text-sm text-red-600 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                {{ getFieldError('role') }}
              </div>
            </div>

            <!-- Consent Checkbox -->
            <div class="mb-6">
              <div class="flex items-start">
                <input
                  id="consent"
                  v-model="form.consent"
                  @change="validateField('consent', form.consent)"
                  type="checkbox"
                  class="mt-1 h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                  :class="{ 'border-red-500': shouldShowError('consent') }"
                />
                <label for="consent" class="ml-2 text-sm text-gray-700 select-none">
                  I agree to receive updates about NoaMetrics and accept the
                  <a href="#" class="text-primary-600 underline">Terms of Service</a> and
                  <a href="#" class="text-primary-600 underline">Privacy Policy</a>
                  <span class="text-red-500">*</span>
                </label>
              </div>
              <div v-if="shouldShowError('consent')" class="mt-1 text-sm text-red-600 flex items-center">
                <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                {{ getFieldError('consent') }}
              </div>
            </div>
            
            <!-- Submit Button with Enhanced Loading State -->
            <button
              type="submit"
              :disabled="isSubmitting || (!isFormValid && hasAttemptedSubmit)"
              class="w-full py-3 bg-primary-600 text-white text-base font-semibold rounded-lg transition-all duration-200 flex items-center justify-center gap-2"
              :class="getSubmitButtonClasses()"
            >
              <span v-if="!isSubmitting">
                {{ isFormValid ? 'Join Beta Program' : 'Complete Required Fields' }}
              </span>
              <span v-else>Processing...</span>
              
              <!-- Loading Spinner -->
              <svg v-if="isSubmitting" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              
              <!-- Success Icon -->
              <svg v-else-if="isFormValid" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </button>
            
            <!-- Form Validation Summary -->
            <div class="mt-3 text-xs text-gray-500 text-center">
              <span v-if="!isFormValid && hasFilledFields">
                Please complete all required fields to continue
              </span>
              <span v-else-if="isFormValid">
                All fields validated ✓ Ready to submit
              </span>
            </div>
            
            <!-- Footer Information Icons -->
            <div class="flex items-center justify-between text-xs text-gray-400 mt-4">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c0-1.657-1.343-3-3-3s-3 1.343-3 3c0 1.657 1.343 3 3 3s3-1.343 3-3zm0 0c0-1.657 1.343-3 3-3s3 1.343 3 3c0 1.657-1.343 3-3 3s-3-1.343-3-3z"/></svg>
                Secure & Private
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-blue-500" fill="currentColor" viewBox="0 0 20 20"><path d="M13 7H7v6h6V7z"/><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-3-9a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H8a1 1 0 01-1-1V9z" clip-rule="evenodd"/></svg>
                500+ Beta Users
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a8 8 0 100 16 8 8 0 000-16zm1 11H9v-2h2v2zm0-4H9V7h2v2z"/></svg>
                2 Min Setup
              </div>
            </div>
            
            <!-- Sign In Link -->
            <div class="text-center text-xs text-gray-500 mt-3">
              Already have access? <a href="#" class="text-primary-600 underline">Sign in here</a>
            </div>
          </form>
        </div>

        <!-- =============================================================== -->
        <!-- SECTION 2.3: SUCCESS STATE OVERLAY                           -->
        <!-- Purpose: Confirmation screen shown after successful submission -->
        <!-- =============================================================== -->
        <div v-if="isSuccess" class="px-6 py-6 text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          
          <!-- Simple thank you (if no files in localStorage) -->
          <div v-if="!hasPendingFiles" class="space-y-4">
            <div class="mt-10 flex justify-center items-center min-h-[200px] md:min-h-[240px]">
              <div class="text-center w-full max-w-md mx-auto mb-4 flex flex-col items-center justify-center">
                <p class="text-gray-600 text-lg">
                  Welcome to NoaMetrics! We're glad you joined us.
                </p>
              </div>
            </div>
            <!-- Badges removed from here -->
            <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <p class="text-sm text-green-800">
                <strong>Registration completed!</strong> You can now upload resumes and analyze candidates on the dashboard.
              </p>
            </div>
            <button
              @click="closeDrawer"
              class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Close
            </button>
          </div>
          
          <!-- File processing (if there are files in localStorage) -->
          <div v-else class="space-y-4">
            <div class="mt-10 flex justify-center items-center min-h-[200px] md:min-h-[240px]">
              <div class="text-center w-full max-w-md mx-auto mb-4 flex flex-col items-center justify-center">
                <p class="text-gray-600 text-lg whitespace-pre-line break-words">
                  Welcome to NoaMetrics!<br>We're glad you joined us.
                </p>
              </div>
            </div>
            <!-- Badges removed from here -->
            <p class="text-gray-600 mb-6">
              Processing your uploaded files and analyzing candidates... This may take several minutes.
            </p>
            <div class="flex items-center justify-center mb-6">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
              <span class="ml-2 text-sm text-gray-600">Analyzing candidates...</span>
            </div>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <p class="text-sm text-blue-800">
                <strong>What's next?</strong> After the analysis is complete, you will be redirected to the dashboard where you can view the results and manage your analyses.
              </p>
            </div>
            <button
              @click="closeDrawer"
              class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
// ==============================================================================
// SCRIPT SETUP SECTION
// ==============================================================================
// PURPOSE: 
// Enhanced form management with comprehensive validation, error handling, 
// user experience improvements, and real-time feedback. Integrates with 
// validation composable for robust form validation.
//
// OPERATING PRINCIPLE:
// - Uses Vue 3 Composition API with validation composable
// - Real-time field validation with user-friendly error messages
// - Enhanced loading states and error handling
// - Form progress tracking and user experience optimization
// ==============================================================================

// =================================================================== 
// SECTION 1: IMPORTS AND COMPOSABLES
// Purpose: Import validation logic and form state management
// ===================================================================
const { useFormValidation } = await import('~/composables/useFormValidation.js')
import { useApiFactory } from '~/composables/useApi'
import { ref } from 'vue'
// Remove useRouter
// import { useRouter } from 'vue-router'
// const router = useRouter()

// Initialize validation composable
const {
  validateField,
  validateAllFields,
  markFieldAsTouched,
  clearFieldError,
  resetValidation,
  getFieldError,
  isFieldValid,
  isFieldTouched,
  shouldShowError,
  isFormValid,
  hasErrors,
  currentErrors,
  VALID_ROLES
} = useFormValidation()

const useApi = useApiFactory()

// Add files ref for drag-and-drop uploads
const files = ref([])

// =================================================================== 
// SECTION 2: COMPONENT INTERFACE (PROPS & EVENTS)
// Purpose: Define component inputs and outputs
// ===================================================================
defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

// =================================================================== 
// SECTION 3: REACTIVE STATE MANAGEMENT
// Purpose: Component's internal state and form data
// ===================================================================
const isSubmitting = ref(false)
const isSuccess = ref(false)
const hasAttemptedSubmit = ref(false)
const showErrorSummary = ref(false)
const networkError = ref(null)

// Form data reactive object
const form = ref({
  fullName: '',
  email: '',
  phone: '',
  companyName: '',
  role: '',
  consent: false
})

// =================================================================== 
// SECTION 4: COMPUTED PROPERTIES
// Purpose: Dynamic form state calculations
// ===================================================================

// Calculate form completion progress
const formProgress = computed(() => {
  const fields = ['fullName', 'email', 'phone', 'companyName', 'role', 'consent']
  const completedFields = fields.filter(field => {
    if (field === 'consent') return form.value[field] === true
    return form.value[field] && form.value[field].toString().trim().length > 0
  }).length
  return (completedFields / fields.length) * 100
})

// Check if user has started filling the form
const hasFilledFields = computed(() => {
  return Object.values(form.value).some(value => {
    if (typeof value === 'boolean') return value
    return value && value.toString().trim().length > 0
  })
})

// Check if there are pending files in localStorage
const hasPendingFiles = computed(() => {
  if (process.client) {
    const pendingFiles = localStorage.getItem('pending_files')
    const pendingAnalysisIds = localStorage.getItem('pending_analysis_ids')
    return !!(pendingFiles || pendingAnalysisIds)
  }
  return false
})

const MAX_CANDIDATE_FILES = 5
const candidateFiles = computed(() => files.value.filter(f => !f.name.toLowerCase().includes('job_description')))
const jobDescriptionFile = computed(() => files.value.find(f => f.name.toLowerCase().includes('job_description')))
const fileUploadError = ref('')
const uploadProgress = ref(0)

function onFilesSelected(newFiles) {
  // Ограничиваем до 5 кандидатов
  const candidateCount = newFiles.filter(f => !f.name.toLowerCase().includes('job_description')).length
  if (candidateCount > MAX_CANDIDATE_FILES) {
    fileUploadError.value = 'Можно загрузить не более 5 резюме-кандидатов за раз.'
    return
  }
  fileUploadError.value = ''
  files.value = newFiles
}

async function uploadAllCandidatesAndJD() {
  isSubmitting.value = true
  uploadProgress.value = 0
  fileUploadError.value = ''
  try {
    // 1. Загрузить JD (если есть)
    let jdAnalysisId = null
    if (jobDescriptionFile.value) {
      const jdAnalysisResp = await useApi('/api/v1/analysis', {
        method: 'POST',
        json: { job_description: 'JD file' }
      })
      jdAnalysisId = jdAnalysisResp.id
      // Загрузить сам JD-файл
      const formData = new FormData()
      formData.append('file', jobDescriptionFile.value)
      formData.append('analysis_id', jdAnalysisId)
      await useApi('/api/v1/files/upload', {
        method: 'POST',
        body: formData
      })
    }
    // 2. Для каждого кандидата создать анализ и загрузить файл
    let completed = 0
    for (const f of candidateFiles.value) {
      const analysisResp = await useApi('/api/v1/analysis', {
        method: 'POST',
        json: { job_description: jdAnalysisId ? 'job_description.pdf' : '' }
      })
      const analysisId = analysisResp.id
      const formData = new FormData()
      formData.append('file', f)
      formData.append('analysis_id', analysisId)
      await useApi('/api/v1/files/upload', {
        method: 'POST',
        body: formData
      })
      completed++
      uploadProgress.value = Math.round((completed / candidateFiles.value.length) * 100)
    }
    files.value = []
    uploadProgress.value = 100
    isSuccess.value = true
    setTimeout(() => closeDrawer(), 3000)
  } catch (e) {
    fileUploadError.value = e.message || 'Ошибка загрузки файлов.'
  } finally {
    isSubmitting.value = false
  }
}

// Функция запуска анализа для списка analysisIds
async function startAnalysis(analysisIds) {
  const { useApiFactory } = await import('~/composables/useApi')
  const useApi = useApiFactory()
  for (const id of analysisIds) {
    try {
      await useApi(`http://localhost:8000/api/v1/analysis/${id}/run`, {
        method: 'POST'
      })
    } catch (e) {
      // Можно показать ошибку, но продолжаем
    }
  }
}

function base64ToUint8Array(base64) {
  const binary = atob(base64)
  const len = binary.length
  const bytes = new Uint8Array(len)
  for (let i = 0; i < len; i++) {
    bytes[i] = binary.charCodeAt(i)
  }
  return bytes
}

async function processPendingFiles(filesData) {
  const { useApiFactory } = await import('~/composables/useApi')
  const useApi = useApiFactory()
  
  console.log('processPendingFiles: filesData =', filesData)
  // Получаем токен доступа
  const accessToken = localStorage.getItem('access_token')
  if (!accessToken) {
    throw new Error('Токен доступа не найден')
  }
  
  // Находим job description
  const jdFile = filesData.find(f => f.type === 'jd')
  if (!jdFile) {
    throw new Error('Job description не найден')
  }
  
  // Создаем анализ для JD
  let jdAnalysisId = null
  try {
    const data = await useApi('http://localhost:8000/api/v1/analysis/', {
      method: 'POST',
      json: { job_description: '' }
    })
    jdAnalysisId = data.id
  } catch (e) {
    throw new Error(`Ошибка создания анализа для JD: ${e.message}`)
  }
  
  // Загружаем JD файл на сервер (оригинальный)
  try {
    const jdBytes = base64ToUint8Array(jdFile.base64)
    const jdFileObj = new File([jdBytes], jdFile.name, { type: jdFile.mime })
    const formData = new FormData()
    formData.append('file', jdFileObj)
    formData.append('analysis_id', jdAnalysisId)
    await new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', 'http://localhost:8000/api/v1/files/upload')
      xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken)
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve()
        } else {
          reject(new Error(`Ошибка загрузки JD: ${xhr.responseText}`))
        }
      }
      xhr.onerror = () => reject(new Error('Ошибка загрузки JD'))
      xhr.send(formData)
    })
  } catch (e) {
    console.error('Ошибка загрузки JD файла:', e)
  }
  
  // Обрабатываем файлы кандидатов
  const candidateFiles = filesData.filter(f => f.type === 'cv')
  const candidateAnalysisIds = []
  
  for (const fileData of candidateFiles) {
    console.log('Обрабатываем файл кандидата:', fileData)
    try {
      // Создаем анализ для кандидата
      const data = await useApi('http://localhost:8000/api/v1/analysis/', {
        method: 'POST',
        json: { job_description: '' }
      })
      const candidateAnalysisId = data.id
      candidateAnalysisIds.push(candidateAnalysisId)
      
      // Загружаем файл кандидата на сервер (оригинальный)
      const cvBytes = base64ToUint8Array(fileData.base64)
      const cvFileObj = new File([cvBytes], fileData.name, { type: fileData.mime })
      const formData = new FormData()
      formData.append('file', cvFileObj)
      formData.append('analysis_id', candidateAnalysisId)
      await new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest()
        xhr.open('POST', 'http://localhost:8000/api/v1/files/upload')
        xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken)
        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve()
          } else {
            reject(new Error(`Ошибка загрузки файла ${fileData.name}: ${xhr.responseText}`))
          }
        }
        xhr.onerror = () => reject(new Error(`Ошибка загрузки файла ${fileData.name}`))
        xhr.send(formData)
      })
      // Запускаем анализ
      await useApi(`http://localhost:8000/api/v1/analysis/${candidateAnalysisId}/run`, {
        method: 'POST'
      })
    } catch (e) {
      console.error(`Ошибка обработки файла ${fileData.name}:`, e)
    }
  }
  
  // Сохраняем analysis_ids для отслеживания
  localStorage.setItem('last_uploaded_analysis_ids', JSON.stringify(candidateAnalysisIds))
  
  // Ждем завершения всех анализов
  await waitForAllAnalysesToComplete(candidateAnalysisIds)
}

// Функция ожидания завершения всех анализов
async function waitForAllAnalysesToComplete(analysisIds) {
  const { useApiFactory } = await import('~/composables/useApi')
  const useApi = useApiFactory()
  
  console.log('Ожидание завершения анализов:', analysisIds)
  
  return new Promise((resolve) => {
    const checkInterval = setInterval(async () => {
      try {
        let allCompleted = true
        
        for (const id of analysisIds) {
          const data = await useApi(`http://localhost:8000/api/v1/analysis/${id}`)
          console.log(`Анализ ${id}: статус ${data.status}`)
          
          if (data.status !== 'completed') {
            allCompleted = false
            break
          }
        }
        
        if (allCompleted) {
          console.log('Все анализы завершены!')
          clearInterval(checkInterval)
          resolve()
        }
      } catch (e) {
        console.error('Ошибка проверки статуса анализов:', e)
        // Продолжаем проверку даже при ошибке
      }
    }, 3000) // Проверяем каждые 3 секунды
    
    // Таймаут на случай, если анализы не завершатся за разумное время
    setTimeout(() => {
      clearInterval(checkInterval)
      console.log('Таймаут ожидания анализов')
      resolve()
    }, 300000) // 5 минут таймаут
  })
}

// =================================================================== 
// SECTION 5: VALIDATION AND UX METHODS
// Purpose: Form validation and user experience helpers
// ===================================================================

// Handle real-time field validation with debouncing
const fieldValidationTimeout = ref({})

const onFieldInput = (fieldName, value) => {
  // Clear existing timeout for this field
  if (fieldValidationTimeout.value[fieldName]) {
    clearTimeout(fieldValidationTimeout.value[fieldName])
  }
  
  // Clear error when user starts typing
  if (shouldShowError(fieldName)) {
    clearFieldError(fieldName)
  }
  
  // Debounced validation after user stops typing
  fieldValidationTimeout.value[fieldName] = setTimeout(() => {
    validateField(fieldName, value)
  }, 500)
}

// Get CSS classes for form fields based on validation state
const getFieldClasses = (fieldName) => {
  const baseClasses = 'border-gray-300'
  const validClasses = 'border-green-500 bg-green-50'
  const errorClasses = 'border-red-500 bg-red-50'
  
  if (!isFieldTouched(fieldName)) return baseClasses
  if (shouldShowError(fieldName)) return errorClasses
  if (isFieldValid(fieldName)) return validClasses
  return baseClasses
}

// Get CSS classes for submit button based on form state
const getSubmitButtonClasses = () => {
  if (isSubmitting.value) {
    return 'opacity-75 cursor-not-allowed'
  }
  if (isFormValid.value) {
    return 'hover:bg-primary-700 transform hover:scale-[1.02]'
  }
  if (hasAttemptedSubmit.value) {
    return 'bg-gray-400 cursor-not-allowed'
  }
  return 'hover:bg-primary-700'
}

// =================================================================== 
// SECTION 6: DRAWER CONTROL METHODS
// Purpose: Handle opening/closing and state reset
// ===================================================================
const closeDrawer = () => {
  emit('close')
  setTimeout(() => {
    // Reset all form state
    isSuccess.value = false
    hasAttemptedSubmit.value = false
    showErrorSummary.value = false
    networkError.value = null
    resetValidation()
    
    // Reset form data
    form.value = {
      fullName: '',
      email: '',
      phone: '',
      companyName: '',
      role: '',
      consent: false
    }
    
    // Clear validation timeouts
    Object.keys(fieldValidationTimeout.value).forEach(key => {
      if (fieldValidationTimeout.value[key]) {
        clearTimeout(fieldValidationTimeout.value[key])
      }
    })
    fieldValidationTimeout.value = {}
  }, 300)
}

// =================================================================== 
// SECTION 7: FORM SUBMISSION HANDLER
// Purpose: Process form data and manage submission states
// ===================================================================
const handleSubmit = async () => {
  hasAttemptedSubmit.value = true
  networkError.value = null

  // Validate all fields
  const validation = validateAllFields(form.value)
  if (!validation.isValid) {
    showErrorSummary.value = true
    Object.keys(form.value).forEach(fieldName => markFieldAsTouched(fieldName))
    return
  }

  isSubmitting.value = true
  showErrorSummary.value = false

  try {
    // Формируем payload для backend
    const payload = {
      full_name: form.value.fullName,
      email: form.value.email,
      phone: form.value.phone,
      company_name: form.value.companyName,
      role: form.value.role,
      consent: form.value.consent
    }

    // Заменяем fetch на useApi
    const data = await useApi('/api/v1/auth/beta-register', {
      method: 'POST',
      json: payload
    })

    // Если backend вернул токен (логин), сохраняем его
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token)
      if (typeof window !== 'undefined' && typeof window.checkAuth === 'function') {
        window.checkAuth();
      }
      // Отправляем событие для обновления состояния в других компонентах
      window.dispatchEvent(new StorageEvent('storage', {
        key: 'access_token',
        newValue: data.access_token
      }))
      // Дополнительное событие для компонентов
      window.dispatchEvent(new CustomEvent('auth-changed'))
    }

    isSuccess.value = true
    
    // Проверяем, есть ли pending files для обработки
    if (hasPendingFiles.value) {
      const pendingFiles = localStorage.getItem('pending_files')
      if (pendingFiles) {
        try {
          const filesData = JSON.parse(pendingFiles)
          // Очищаем pending_files
          localStorage.removeItem('pending_files')
          // Обрабатываем файлы после регистрации и ждем завершения всех анализов
          await processPendingFiles(filesData)
          // Закрываем drawer и переходим на дашборд только после завершения всех анализов
          setTimeout(() => {
            closeDrawer()
            if (process.client) {
              window.location.href = '/dashboard'
            }
          }, 2000)
          return
        } catch (e) {
          console.error('Ошибка обработки файлов после регистрации:', e)
        }
      }
      
      // Проверяем, есть ли pending analysis_ids для запуска анализа (старая логика)
      const pendingAnalysisIds = localStorage.getItem('pending_analysis_ids')
      if (pendingAnalysisIds) {
        try {
          const analysisIds = JSON.parse(pendingAnalysisIds)
          // Очищаем pending_analysis_ids
          localStorage.removeItem('pending_analysis_ids')
          // Запускаем анализ
          await startAnalysis(analysisIds)
          // Закрываем drawer и переходим на дашборд
          setTimeout(() => {
            closeDrawer()
            if (process.client) {
              window.location.href = '/dashboard'
            }
          }, 2000)
          return
        } catch (e) {
          console.error('Ошибка запуска анализа после регистрации:', e)
        }
      }
    }
    
    // Если нет pending files, просто закрываем drawer через 3 секунды
    setTimeout(() => closeDrawer(), 3000)
  } catch (error) {
    networkError.value = error.message || 'Unable to submit your application. Please try again.'
    console.error('Form submission error:', error)
  } finally {
    isSubmitting.value = false
  }
}

// Retry submission after network error
const retrySubmission = () => {
  networkError.value = null
  handleSubmit()
}

// =================================================================== 
// SECTION 8: FORM PERSISTENCE (OPTIONAL)
// Purpose: Save form data to prevent loss on accidental close
// ===================================================================

// Auto-save form data to localStorage
watch(form, (newForm) => {
  if (import.meta.client && hasFilledFields.value) {
    try {
      localStorage.setItem('noa-beta-form-draft', JSON.stringify(newForm))
    } catch (error) {
      console.warn('Failed to save form draft:', error)
    }
  }
}, { deep: true })

// Load saved form data on component mount
onMounted(() => {
  if (import.meta.client) {
    try {
      const savedDraft = localStorage.getItem('noa-beta-form-draft')
      if (savedDraft) {
        const parsedDraft = JSON.parse(savedDraft)
        // Only restore if form is currently empty
        if (!hasFilledFields.value) {
          form.value = { ...form.value, ...parsedDraft }
        }
      }
    } catch (error) {
      console.warn('Failed to load form draft:', error)
    }
  }
})

// Clear saved draft when form is successfully submitted
watch(isSuccess, (newValue) => {
  if (newValue && import.meta.client) {
    try {
      localStorage.removeItem('noa-beta-form-draft')
    } catch (error) {
      console.warn('Failed to clear form draft:', error)
    }
  }
})
</script>

<style scoped>
:deep(.bg-primary-600) {
  background-color: #0284c7 !important;
}
.text-primary-600 {
  color: #0284c7 !important;
}
.border-primary-500 {
  border-color: #0ea5e9 !important;
}
.focus\:ring-primary-500:focus {
  --tw-ring-color: #0ea5e9 !important;
}
.hover\:bg-primary-700:hover {
  background-color: #0369a1 !important;
}
.shadow-sm {
  box-shadow: 0 1px 6px 0 rgba(0,0,0,0.04), 0 1.5px 4px 0 rgba(0,0,0,0.04);
}
</style> 