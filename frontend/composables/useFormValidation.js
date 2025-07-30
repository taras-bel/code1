// ==============================================================================
// COMPOSABLE: useFormValidation.js
// ==============================================================================
// PURPOSE: 
// Comprehensive form validation composable providing real-time validation,
// error handling, and validation state management for the lead capture form.
// Supports email, phone, required fields, and custom validation rules.
//
// OPERATING PRINCIPLE:
// - Real-time validation with debounced input checking
// - Comprehensive validation rules for different field types
// - Error state management with user-friendly messages
// - International phone number support
// - Email format validation with domain checking
// ==============================================================================

// =================================================================== 
// SECTION 1: VALIDATION RULES AND PATTERNS
// Purpose: Define validation patterns and rules
// ===================================================================

// Email validation pattern (RFC 5322 compliant)
const EMAIL_PATTERN = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/

// Phone validation patterns for different formats
const PHONE_PATTERNS = {
  US: /^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$/,
  INTERNATIONAL: /^\+?[1-9]\d{1,14}$/,
  GENERAL: /^[+]?[1-9][\d]{0,15}$/
}

// Common domains for basic email validation (for future use)
// const COMMON_DOMAINS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'company.com']

// Role options for validation
const VALID_ROLES = [
  'HR Manager',
  'Recruiter', 
  'Talent Acquisition',
  'CEO/Founder',
  'CTO',
  'Engineering Manager',
  'Product Manager',
  'Operations',
  'Other'
]

// =================================================================== 
// SECTION 2: VALIDATION FUNCTIONS
// Purpose: Individual field validation functions
// ===================================================================

const validateEmail = (email) => {
  if (!email) {
    return { isValid: false, error: 'Email is required' }
  }
  
  if (!EMAIL_PATTERN.test(email)) {
    return { isValid: false, error: 'Please enter a valid email address' }
  }
  
  // Check for common typos in domain
  const domain = email.split('@')[1]?.toLowerCase()
  if (domain && domain.includes('gmial')) {
    return { isValid: false, error: 'Did you mean gmail.com?' }
  }
  
  return { isValid: true, error: null }
}

const validatePhone = (phone) => {
  if (!phone) {
    return { isValid: false, error: 'Phone number is required' }
  }
  
  // Remove all non-digit characters for validation
  const cleanPhone = phone.replace(/\D/g, '')
  
  if (cleanPhone.length < 10) {
    return { isValid: false, error: 'Phone number must be at least 10 digits' }
  }
  
  if (cleanPhone.length > 15) {
    return { isValid: false, error: 'Phone number is too long' }
  }
  
  // Test against international pattern
  if (!PHONE_PATTERNS.INTERNATIONAL.test(phone.replace(/\s/g, ''))) {
    return { isValid: false, error: 'Please enter a valid phone number' }
  }
  
  return { isValid: true, error: null }
}

const validateFullName = (name) => {
  if (!name || !name.trim()) {
    return { isValid: false, error: 'Full name is required' }
  }
  
  if (name.trim().length < 2) {
    return { isValid: false, error: 'Name must be at least 2 characters' }
  }
  
  if (name.trim().length > 50) {
    return { isValid: false, error: 'Name is too long (max 50 characters)' }
  }
  
  // Check for at least first and last name
  const nameParts = name.trim().split(' ').filter(part => part.length > 0)
  if (nameParts.length < 2) {
    return { isValid: false, error: 'Please enter your full name (first and last)' }
  }
  
  return { isValid: true, error: null }
}

const validateCompanyName = (company) => {
  if (!company || !company.trim()) {
    return { isValid: false, error: 'Company name is required' }
  }
  
  if (company.trim().length < 2) {
    return { isValid: false, error: 'Company name must be at least 2 characters' }
  }
  
  if (company.trim().length > 100) {
    return { isValid: false, error: 'Company name is too long (max 100 characters)' }
  }
  
  return { isValid: true, error: null }
}

const validateRole = (role) => {
  if (!role || !role.trim()) {
    return { isValid: false, error: 'Role is required' }
  }
  
  if (!VALID_ROLES.includes(role)) {
    return { isValid: false, error: 'Please select a valid role' }
  }
  
  return { isValid: true, error: null }
}

const validateConsent = (consent) => {
  if (!consent) {
    return { isValid: false, error: 'You must agree to the terms to continue' }
  }
  
  return { isValid: true, error: null }
}

// =================================================================== 
// SECTION 3: MAIN VALIDATION COMPOSABLE
// Purpose: Main composable function with reactive state
// ===================================================================

export const useFormValidation = () => {
  // Reactive validation state
  const validationState = ref({
    fullName: { isValid: false, error: null, touched: false },
    email: { isValid: false, error: null, touched: false },
    phone: { isValid: false, error: null, touched: false },
    companyName: { isValid: false, error: null, touched: false },
    role: { isValid: false, error: null, touched: false },
    consent: { isValid: false, error: null, touched: false }
  })
  
  // Overall form validity
  const isFormValid = computed(() => {
    return Object.values(validationState.value).every(field => field.isValid)
  })
  
  // Check if form has any errors
  const hasErrors = computed(() => {
    return Object.values(validationState.value).some(field => field.error !== null)
  })
  
  // Get list of all current errors
  const currentErrors = computed(() => {
    return Object.entries(validationState.value)
      .filter(([, field]) => field.error !== null)
      .map(([fieldName, field]) => ({ field: fieldName, error: field.error }))
  })
  
  // =================================================================== 
  // SECTION 4: VALIDATION METHODS
  // Purpose: Methods to validate individual fields and entire form
  // ===================================================================
  
  const validateField = (fieldName, value) => {
    let validation
    
    switch (fieldName) {
      case 'fullName':
        validation = validateFullName(value)
        break
      case 'email':
        validation = validateEmail(value)
        break
      case 'phone':
        validation = validatePhone(value)
        break
      case 'companyName':
        validation = validateCompanyName(value)
        break
      case 'role':
        validation = validateRole(value)
        break
      case 'consent':
        validation = validateConsent(value)
        break
      default:
        validation = { isValid: true, error: null }
    }
    
    // Update validation state
    validationState.value[fieldName] = {
      ...validation,
      touched: true
    }
    
    return validation
  }
  
  const validateAllFields = (formData) => {
    const results = {}
    
    Object.keys(formData).forEach(fieldName => {
      results[fieldName] = validateField(fieldName, formData[fieldName])
    })
    
    return {
      isValid: Object.values(results).every(result => result.isValid),
      errors: Object.entries(results)
        .filter(([, result]) => !result.isValid)
        .reduce((acc, [fieldName, result]) => {
          acc[fieldName] = result.error
          return acc
        }, {})
    }
  }
  
  const markFieldAsTouched = (fieldName) => {
    if (validationState.value[fieldName]) {
      validationState.value[fieldName].touched = true
    }
  }
  
  const clearFieldError = (fieldName) => {
    if (validationState.value[fieldName]) {
      validationState.value[fieldName].error = null
    }
  }
  
  const resetValidation = () => {
    Object.keys(validationState.value).forEach(fieldName => {
      validationState.value[fieldName] = {
        isValid: false,
        error: null,
        touched: false
      }
    })
  }
  
  // =================================================================== 
  // SECTION 5: HELPER METHODS
  // Purpose: Utility methods for form validation
  // ===================================================================
  
  const getFieldError = (fieldName) => {
    const field = validationState.value[fieldName]
    return field?.touched && field?.error ? field.error : null
  }
  
  const isFieldValid = (fieldName) => {
    return validationState.value[fieldName]?.isValid || false
  }
  
  const isFieldTouched = (fieldName) => {
    return validationState.value[fieldName]?.touched || false
  }
  
  const shouldShowError = (fieldName) => {
    const field = validationState.value[fieldName]
    return field?.touched && field?.error !== null
  }
  
  // =================================================================== 
  // SECTION 6: COMPOSABLE INTERFACE
  // Purpose: Return validation state and methods
  // ===================================================================
  
  return {
    // State
    validationState: readonly(validationState),
    isFormValid,
    hasErrors,
    currentErrors,
    
    // Validation methods
    validateField,
    validateAllFields,
    markFieldAsTouched,
    clearFieldError,
    resetValidation,
    
    // Helper methods
    getFieldError,
    isFieldValid,
    isFieldTouched,
    shouldShowError,
    
    // Constants for components
    VALID_ROLES
  }
} 