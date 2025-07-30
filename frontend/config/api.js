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

// Export current config
export const apiConfig = config[env]

// Helper function to get full API URL
export function getApiUrl(endpoint) {
  // Remove leading slash if present
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint
  
  return `${apiConfig.apiBaseUrl}/${cleanEndpoint}`
}

export default apiConfig 