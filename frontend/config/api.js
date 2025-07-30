// API Configuration for different environments
const config = {
  development: {
    apiBaseUrl: 'https://localhost',
    apiTimeout: 10000
  },
  production: {
    // Production API URL - используем HTTPS
    apiBaseUrl: 'https://localhost',
    apiTimeout: 15000
  }
}

// Get current environment
const env = process.env.NODE_ENV || 'development'

// Dynamic API URL detection
function getDynamicApiUrl() {
  // If we're in the browser, use the current origin
  if (typeof window !== 'undefined') {
    const currentOrigin = window.location.origin
    // If accessing via HTTPS, use HTTPS for API
    if (currentOrigin.startsWith('https://')) {
      return currentOrigin
    }
    // If accessing via HTTP, use HTTP for API (for development)
    if (currentOrigin.startsWith('http://')) {
      return currentOrigin
    }
  }
  
  // Fallback to config
  return config[env].apiBaseUrl
}

// Export current config with dynamic URL
export const apiConfig = {
  ...config[env],
  apiBaseUrl: getDynamicApiUrl()
}

// Helper function to get full API URL
export function getApiUrl(endpoint) {
  // Remove leading slash if present
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint
  
  return `${apiConfig.apiBaseUrl}/${cleanEndpoint}`
}

export default apiConfig 