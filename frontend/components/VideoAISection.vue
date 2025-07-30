<!-- =============================================================================== -->
<!-- FILE: components/VideoAISection.vue                                          -->
<!-- =============================================================================== -->
<!-- PURPOSE:                                                                      -->
<!-- Interactive product demonstration section that showcases the core AI         -->
<!-- analysis capabilities. Features a dual-column layout with benefits           -->
<!-- checklist and file upload simulation to engage users with the product.       -->
<!--                                                                               -->
<!-- OPERATING PRINCIPLE:                                                          -->
<!-- - Two-column responsive layout with benefits and upload areas                -->
<!-- - Visual checklist highlighting key deliverables and value propositions     -->
<!-- - Simulated file upload interface to demonstrate product interaction         -->
<!-- - Mobile-first design with progressive enhancement for larger screens        -->
<!-- - Trust indicators (no signup, no credit card) to reduce friction           -->
<!-- =============================================================================== -->

<template>
  <!-- =============================================================================== -->
  <!-- SECTION 1: MAIN CONTAINER                                                   -->
  <!-- Purpose: Section wrapper with proper spacing and background                 -->
  <!-- =============================================================================== -->
  <section id="video-ai" class="py-12 md:py-16 bg-white">
    <div class="container-custom">
      <!-- =============================================================================== -->
      <!-- SECTION 2: SECTION HEADER                                                   -->
      <!-- Purpose: Title and description introducing the demo experience              -->
      <!-- =============================================================================== -->
      <div class="text-center mb-8 md:mb-12 px-4">
        <h2 class="text-2xl md:text-3xl lg:text-4xl font-extrabold text-gray-900 mb-3 md:mb-4">
          Before the Video AI Agent Arrives
        </h2>
        <p class="text-sm md:text-base lg:text-lg text-gray-500 max-w-2xl mx-auto">
          Allow CV upload + job description for full demo experience
        </p>
      </div>

      <!-- =============================================================================== -->
      <!-- SECTION 3: DEMO INTERFACE CONTAINER                                         -->
      <!-- Purpose: Main card container for the interactive demo                       -->
      <!-- =============================================================================== -->
      <div class="flex justify-center px-4">
        <div class="bg-white rounded-3xl shadow-2xl flex flex-col md:flex-row w-full max-w-6xl p-6 md:p-8 lg:p-10 gap-6 md:gap-8 border border-gray-100">
          
          <!-- =============================================================================== -->
          <!-- SECTION 3.1: BENEFITS CHECKLIST (LEFT COLUMN)                              -->
          <!-- Purpose: Highlight key deliverables and value propositions                  -->
          <!-- =============================================================================== -->
          <div class="flex-1 flex flex-col justify-center p-2 md:p-4 lg:p-8">
            <h3 class="text-xl md:text-2xl lg:text-3xl font-bold text-gray-900 mb-4 md:mb-6 text-center md:text-left">
              In &lt; 60 seconds you'll receive:
            </h3>
            <ul class="space-y-3 md:space-y-4 lg:space-y-5">
              <!-- Benefit Item 1: A-Player Score -->
              <li class="flex items-start gap-3 text-sm md:text-base lg:text-lg text-gray-900">
                <div class="w-6 h-6 md:w-7 md:h-7 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 md:w-4 md:h-4 text-green-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M16.704 6.29a1 1 0 010 1.42l-6.004 6a1 1 0 01-1.416 0l-2.99-2.996a1 1 0 111.416-1.414l2.282 2.287 5.296-5.293a1 1 0 011.416 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>"A" Player Engineer likelihood score</span>
              </li>
              
              <!-- Benefit Item 2: Skills Match -->
              <li class="flex items-start gap-3 text-sm md:text-base lg:text-lg text-gray-900">
                <div class="w-6 h-6 md:w-7 md:h-7 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 md:w-4 md:h-4 text-green-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M16.704 6.29a1 1 0 010 1.42l-6.004 6a1 1 0 01-1.416 0l-2.99-2.996a1 1 0 111.416-1.414l2.282 2.287 5.296-5.293a1 1 0 011.416 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>Skills &amp; Culture-fit Match</span>
              </li>
              
              <!-- Benefit Item 3: Interview Questions -->
              <li class="flex items-start gap-3 text-sm md:text-base lg:text-lg text-gray-900">
                <div class="w-6 h-6 md:w-7 md:h-7 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 md:w-4 md:h-4 text-green-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M16.704 6.29a1 1 0 010 1.42l-6.004 6a1 1 0 01-1.416 0l-2.99-2.996a1 1 0 111.416-1.414l2.282 2.287 5.296-5.293a1 1 0 011.416 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>Actionable Interview Questions</span>
              </li>
              
              <!-- Benefit Item 4: No Signup -->
              <li class="flex items-start gap-3 text-sm md:text-base lg:text-lg text-gray-900">
                <div class="w-6 h-6 md:w-7 md:h-7 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 md:w-4 md:h-4 text-green-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M16.704 6.29a1 1 0 010 1.42l-6.004 6a1 1 0 01-1.416 0l-2.99-2.996a1 1 0 111.416-1.414l2.282 2.287 5.296-5.293a1 1 0 011.416 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>No signup required</span>
              </li>
              
              <!-- Benefit Item 5: No Credit Card -->
              <li class="flex items-start gap-3 text-sm md:text-base lg:text-lg text-gray-900">
                <div class="w-6 h-6 md:w-7 md:h-7 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-3 h-3 md:w-4 md:h-4 text-green-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M16.704 6.29a1 1 0 010 1.42l-6.004 6a1 1 0 01-1.416 0l-2.99-2.996a1 1 0 111.416-1.414l2.282 2.287 5.296-5.293a1 1 0 011.416 0z" clip-rule="evenodd" />
                  </svg>
                </div>
                <span>No credit card required</span>
              </li>
            </ul>
          </div>
          
          <!-- =============================================================================== -->
          <!-- SECTION 3.2: FILE UPLOAD INTERFACE (RIGHT COLUMN)                          -->
          <!-- Purpose: Simulated file upload area for demo interaction                    -->
          <!-- =============================================================================== -->
          <div
            class="flex-1 flex flex-col justify-center items-center bg-gray-50 md:bg-gray-100 rounded-2xl md:rounded-3xl p-6 md:p-8 mt-6 md:mt-0 min-h-[200px] md:min-h-[280px] w-full border border-gray-200"
            @dragover.prevent="onDragOver"
            @dragleave.prevent="onDragLeave"
            @drop.prevent="onDrop"
            :class="{ 'ring-2 ring-primary-500': isDragActive }"
            @click="openFileDialog"
            style="cursor: pointer;"
          >
            <input
              ref="fileInput"
              type="file"
              multiple
              accept=".pdf,.doc,.docx"
              class="hidden"
              @change="onFileChange"
            />
            <div class="flex-1 flex flex-col justify-center items-center w-full">
              <!-- Upload Instructions -->
              <p class="text-center text-gray-600 text-sm md:text-base lg:text-lg mb-4 md:mb-6 px-2 select-none">
                [+] Drag & Drop here: Job Description (.pdf/.doc/.docx) & CVs<br/>
                <span class="text-xs text-gray-400">(Maximum 6 files: 1 JD + 5 CV, each ≤ 10 MB)</span>
              </p>
              <!-- Selected Files List -->
              <TransitionGroup name="file-fade" tag="ul" v-if="files.length" class="w-full max-w-xs mb-4 space-y-2">
                <li v-for="(file, idx) in files" :key="file.file.name" class="flex items-center justify-between bg-white rounded px-3 py-1 border border-gray-200 text-xs md:text-sm shadow-sm file-fade-item">
                  <span class="truncate max-w-[140px]" :title="file.file.name">{{ file.file.name }}</span>
                  <span class="ml-2 text-gray-400">({{ formatFileSize(file.file.size) }})</span>
                  <div v-if="isUploading" class="w-full h-2 bg-gray-200 rounded mt-1">
                    <div :style="{width: uploadProgresses[idx]?.progress + '%'}" class="h-2 bg-primary-500 rounded transition-all"></div>
                  </div>
                  <button @click.stop="removeFile(idx)" class="ml-2 text-red-500 hover:text-red-700 focus:outline-none transition-all duration-200 scale-100 hover:scale-125">✕</button>
                </li>
              </TransitionGroup>
              <!-- Error Message -->
              <div v-if="error" class="text-red-500 text-xs mb-2 text-center">{{ error }}</div>
              <!-- Upload Button -->
              <button
                class="bg-gray-900 hover:bg-black text-white px-6 md:px-8 py-3 rounded-xl font-semibold text-sm md:text-base mt-auto focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 transition-all duration-200 w-full max-w-xs shadow-lg hover:shadow-xl disabled:opacity-50"
                :disabled="!files.length || !!error || isUploading"
                @click.stop="onUpload"
              >
                {{ isUploading ? `Uploading (${uploadProgress}%)` : 'Upload' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- =============================================================================== -->
      <!-- SECTION 4: TRUST INDICATORS                                                 -->
      <!-- Purpose: Final reassurance about data security and no commitment required   -->
      <!-- =============================================================================== -->
      <div class="text-center text-gray-400 text-xs md:text-sm mt-4 px-4">
        No credit card. Data auto-deletes after 14 days.
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApiFactory } from '~/composables/useApi'
import { extractTextFromFile, formatFileSize } from '~/utils/fileUtils'

const files = ref([]) // [{file, type: 'cv'|'jd'}]
const error = ref('')
const isDragActive = ref(false)
const fileInput = ref(null)
const isUploading = ref(false)
const uploadProgress = ref(0)
const analysisId = ref(null)
const isAnalyzing = ref(false)
const analysisProgress = ref(0)
const router = useRouter()
const uploadProgresses = ref([]) // [{name, progress}]

const CV_EXTENSIONS = ['pdf', 'doc', 'docx']
const MAX_FILES = 6
const MAX_CV = 5
const MAX_JD = 1
const MAX_SIZE = 10 * 1024 * 1024 // 10 MB



function openFileDialog() {
  error.value = ''
  fileInput.value?.click()
}

function onFileChange(e) {
  handleFiles(e.target.files)
  e.target.value = '' // reset for re-upload
}

function onDragOver() {
  isDragActive.value = true
}
function onDragLeave() {
  isDragActive.value = false
}
function onDrop(e) {
  isDragActive.value = false
  handleFiles(e.dataTransfer.files)
}

function handleFiles(fileList) {
  error.value = ''
  let newFiles = Array.from(fileList)
  // Фильтрация по размеру и типу
  for (const file of newFiles) {
    if (file.size > MAX_SIZE) {
      error.value = `File ${file.name} exceeds 10 MB.`
      return
    }
    const ext = file.name.split('.').pop().toLowerCase()
    if (!CV_EXTENSIONS.includes(ext)) {
      error.value = `Invalid file format: ${file.name}`
      return
    }
    // Check for duplicate by name
    if (files.value.some(f => f.file.name === file.name)) {
      error.value = `File with name ${file.name} is already added.`
      return
    }
  }
  // Classification: JD or CV
  let currentJD = files.value.filter(f => f.type === 'jd').length
  let currentCV = files.value.filter(f => f.type === 'cv').length
  for (const file of newFiles) {
    const ext = file.name.split('.').pop().toLowerCase()
    // JD: if name contains 'job' or 'desc', otherwise CV
    let type = (/job|desc/i.test(file.name) && currentJD < MAX_JD) ? 'jd' : 'cv'
    if (type === 'jd') {
      if (currentJD >= MAX_JD) {
        error.value = 'You can upload only 1 job description.'
        return
      }
      currentJD++
    } else {
      if (currentCV >= MAX_CV) {
        error.value = 'You can upload maximum 5 CVs.'
        return
      }
      currentCV++
    }
  }
  // Check total limit
  if (files.value.length + newFiles.length > MAX_FILES) {
    error.value = `Maximum files: ${MAX_FILES}`
    return
  }
  // Add files
  for (const file of newFiles) {
    // Don't add duplicates by name
    if (files.value.some(f => f.file.name === file.name)) continue
    const ext = file.name.split('.').pop().toLowerCase()
    let type = (/job|desc/i.test(file.name) && files.value.filter(f => f.type === 'jd').length < MAX_JD) ? 'jd' : 'cv'
    files.value.push({ file, type })
  }
}

function removeFile(idx) {
  files.value.splice(idx, 1)
  error.value = ''
}

async function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result.split(',')[1])
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}


const useApi = useApiFactory()

async function onUpload() {
  if (!files.value.length) return
  error.value = ''
  
  const accessToken = localStorage.getItem('access_token')
  const isLoggedIn = !!accessToken

  // Если пользователь НЕ залогинен - открываем форму Join Beta
  if (!isLoggedIn) {
    // Сохраняем оригинальные файлы в base64
    const filesData = []
    for (const fileObj of files.value) {
      try {
        const base64 = await fileToBase64(fileObj.file)
        filesData.push({
          name: fileObj.file.name,
          mime: fileObj.file.type,
          type: fileObj.type,
          size: fileObj.file.size,
          base64: base64
        })
      } catch (e) {
        console.error(`Ошибка преобразования файла ${fileObj.file.name} в base64:`, e)
      }
    }
    console.log('Сохраняем в localStorage pending_files:', filesData)
    localStorage.setItem('pending_files', JSON.stringify(filesData))
    
    // Открываем форму Join Beta
    const { useJoinBetaDrawer } = await import('~/composables/useJoinBetaDrawer.js')
    const { open } = useJoinBetaDrawer()
    
    // Очищаем секцию drag and drop перед открытием формы
    files.value = []
    error.value = ''
    
    open()
    return
  }

  // Если пользователь залогинен - продолжаем с загрузкой
  isUploading.value = true
  uploadProgress.value = 0
  uploadProgresses.value = files.value.map(f => ({ name: f.file.name, progress: 0 }))

  // 1. Найти job description (JD)
  const jdFile = files.value.find(f => f.type === 'jd')
  if (!jdFile) {
    error.value = 'Не выбран файл job description.'
    isUploading.value = false
    return
  }
  // Прочитать JD как текст (для API)
  let jdText = ''
  try {
    jdText = await extractTextFromFile(jdFile.file)
  } catch (e) {
    error.value = 'Не удалось извлечь текст из файла job description.'
    isUploading.value = false
    return
  }
  if (!jdText.trim()) {
    error.value = 'Файл job description пустой или не содержит текста.'
    isUploading.value = false
    return
  }

  // 2. Создать analysis для JD и загрузить JD-файл
  let jdAnalysisId = null
  try {
    const data = await useApi('http://localhost:8000/api/v1/analysis/', {
      method: 'POST',
      json: { job_description: jdText }
    })
    jdAnalysisId = data.id
      } catch (e) {
      error.value = e.message || 'Ошибка создания анализа для JD'
      isUploading.value = false
      // Очищаем прогресс при ошибке
      uploadProgresses.value = []
      return
    }
  // Загрузить JD-файл
  try {
    const formData = new FormData()
    formData.append('file', jdFile.file)
    formData.append('analysis_id', jdAnalysisId)
    await new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open('POST', 'http://localhost:8000/api/v1/files/upload')
      if (isLoggedIn) {
        xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken)
      }
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve()
        } else {
          error.value = `Ошибка загрузки JD: ${xhr.responseText}`
          isUploading.value = false
          reject()
        }
      }
      xhr.onerror = () => {
        error.value = `Ошибка загрузки JD: ${xhr.responseText}`
        isUploading.value = false
        // Очищаем прогресс при ошибке
        uploadProgresses.value = []
        reject()
      }
      xhr.send(formData)
    })
  } catch (e) {
    return
  }

  // 3. Для каждого кандидата создать analysis и загрузить файл
  const candidateFiles = files.value.filter(f => f.type === 'cv')
  const candidateAnalysisIds = []
  
  for (let i = 0; i < candidateFiles.length; i++) {
    const f = candidateFiles[i]
    console.log(`Обрабатываем кандидата ${i + 1}/${candidateFiles.length}: ${f.file.name}`)
    
    let candidateAnalysisId = null
    try {
      const data = await useApi('http://localhost:8000/api/v1/analysis/', {
        method: 'POST',
        json: { job_description: jdText }
      })
      candidateAnalysisId = data.id
      candidateAnalysisIds.push(candidateAnalysisId)
      console.log(`Создан анализ для ${f.file.name}: ${candidateAnalysisId}`)
    } catch (e) {
      error.value = e.message || `Ошибка создания анализа для кандидата ${f.file.name}`
      isUploading.value = false
      // Очищаем прогресс при ошибке
      uploadProgresses.value = []
      return
    }
    
    // Загрузить файл кандидата
    try {
      const formData = new FormData()
      formData.append('file', f.file)
      formData.append('analysis_id', candidateAnalysisId)
      
      await new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest()
        xhr.open('POST', 'http://localhost:8000/api/v1/files/upload')
        if (isLoggedIn) {
          xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken)
        }
        
        xhr.upload.onprogress = (e) => {
          if (e.lengthComputable) {
            // Находим правильный индекс в uploadProgresses
            const progressIndex = uploadProgresses.value.findIndex(p => p.name === f.file.name)
            if (progressIndex !== -1) {
              uploadProgresses.value[progressIndex].progress = Math.round((e.loaded / e.total) * 100)
            }
          }
        }
        
        xhr.onload = () => {
          // Находим правильный индекс в uploadProgresses
          const progressIndex = uploadProgresses.value.findIndex(p => p.name === f.file.name)
          if (progressIndex !== -1) {
            uploadProgresses.value[progressIndex].progress = 100
          }
          
          if (xhr.status >= 200 && xhr.status < 300) {
            console.log(`Файл ${f.file.name} успешно загружен`)
            resolve()
          } else {
            error.value = `Ошибка загрузки файла ${f.file.name}: ${xhr.responseText}`
            isUploading.value = false
            reject()
          }
        }
        
        xhr.onerror = () => {
          error.value = `Ошибка загрузки файла ${f.file.name}: ${xhr.responseText}`
          isUploading.value = false
          // Очищаем прогресс при ошибке
          uploadProgresses.value = []
          reject()
        }
        
        xhr.send(formData)
      })
    } catch (e) {
      console.error(`Ошибка загрузки файла ${f.file.name}:`, e)
      return
    }
  }
  isUploading.value = false
  uploadProgress.value = 100

  // Сохраняем analysis_id последней загрузки кандидатов в localStorage
  localStorage.setItem('last_uploaded_analysis_ids', JSON.stringify(candidateAnalysisIds))

  // Очищаем секцию drag and drop после успешной загрузки
  files.value = []
  error.value = ''
  uploadProgresses.value = []
  
  // Показываем сообщение об успешной загрузке
  console.log('Все файлы успешно загружены и анализ запущен')

  // Запускаем анализ для всех кандидатов
  await startAnalysis(candidateAnalysisIds)
}

async function startAnalysis(analysisIds) {
  console.log(`Запускаем анализы для ${analysisIds.length} кандидатов:`, analysisIds)
  
  // 4. Запустить анализы для всех кандидатов
  for (let i = 0; i < analysisIds.length; i++) {
    const id = analysisIds[i]
    try {
      console.log(`Запускаем анализ ${i + 1}/${analysisIds.length}: ${id}`)
      await useApi(`http://localhost:8000/api/v1/analysis/${id}/run`, {
        method: 'POST'
      })
      console.log(`Анализ ${id} успешно запущен`)
    } catch (e) {
      console.error(`Ошибка запуска анализа ${id}:`, e)
      // Можно показать ошибку, но продолжаем
    }
  }
  
  console.log('Все анализы запущены, начинаем отслеживание статуса')
  pollAnalysisStatus(analysisIds)
}

function pollAnalysisStatus(ids) {
  console.log('Начинаем отслеживание статуса анализов:', ids)
  isAnalyzing.value = true
  analysisProgress.value = 0
  
  const interval = setInterval(async () => {
    try {
      // Проверяем статусы всех анализов
      let allDone = true
      let completedCount = 0
      
      for (const id of ids) {
        const data = await useApi(`http://localhost:8000/api/v1/analysis/${id}`)
        console.log(`Анализ ${id}: статус ${data.status}`)
        
        if (data.status === 'completed') {
          completedCount++
        } else {
          allDone = false
        }
      }
      
      // Обновляем прогресс
      analysisProgress.value = Math.round((completedCount / ids.length) * 100)
      console.log(`Прогресс анализа: ${completedCount}/${ids.length} завершено (${analysisProgress.value}%)`)
      
      if (allDone) {
        console.log('Все анализы завершены! Переходим на дашборд')
        isAnalyzing.value = false
        analysisProgress.value = 100
        clearInterval(interval)
        
        // Очищаем секцию drag and drop после завершения анализа
        files.value = []
        error.value = ''
        uploadProgresses.value = []
        
        router.push('/dashboard')
      }
    } catch (e) {
      console.error('Ошибка проверки статуса анализов:', e)
      // Можно показывать ошибку, но не сбрасываем polling
    }
  }, 3000)
}
</script> 

<style scoped>
/* Drag-and-drop highlight animation */
[data-v-cloak] { display: none; }

.ring-2 {
  transition: box-shadow 0.3s cubic-bezier(.4,0,.2,1), border-color 0.3s cubic-bezier(.4,0,.2,1);
  box-shadow: 0 0 0 4px #0ea5e933;
  border-color: #0ea5e9 !important;
}

/* File list animation */
.file-fade-enter-active, .file-fade-leave-active {
  transition: all 0.35s cubic-bezier(.4,0,.2,1);
}
.file-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}
.file-fade-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.file-fade-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
.file-fade-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}

/* Upload button animation */
button {
  transition: background 0.2s, box-shadow 0.2s, transform 0.18s cubic-bezier(.4,0,.2,1);
}
button:active {
  transform: scale(0.97);
}

/* Smooth section fade-in (optional, for main section) */
section {
  animation: section-fade-in 0.7s cubic-bezier(.4,0,.2,1);
}
@keyframes section-fade-in {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: none; }
}
</style> 