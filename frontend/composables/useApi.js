// frontend/composables/useApi.js
import { getApiUrl } from '../config/api.js'

export function useApiFactory() {
  return async function useApi(url, options = {}) {
    const isAbsolute = /^https?:\/\//.test(url)
    
    // Определяем полный URL
    let fullUrl
    if (isAbsolute) {
      fullUrl = url
    } else {
      fullUrl = getApiUrl(url)
    }

    const token = (typeof window !== 'undefined') ? localStorage.getItem('access_token') : null
    const headers = {
      'Accept': 'application/json',
      ...(options.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    }

    let body
    if (options.json) {
      body = JSON.stringify(options.json)
      headers['Content-Type'] = 'application/json'
    } else if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
      body = JSON.stringify(options.body)
      headers['Content-Type'] = 'application/json'
    } else {
      body = options.body
    }

    // Не передаём options.body и options.json в fetch!
    const fetchOptions = {
      method: options.method || 'GET',
      headers,
      body,
      ...Object.fromEntries(
        Object.entries(options).filter(([key]) => !['body', 'json'].includes(key))
      ),
    }

    try {
      console.log('[useApi] Making request to:', fullUrl)
      const response = await fetch(fullUrl, fetchOptions)
      const contentType = response.headers.get('content-type') || ''
      let data = null
      if (contentType.includes('application/json')) {
        data = await response.json()
      } else {
        data = await response.text()
      }
      if (!response.ok) {
        const errorMsg = (data && data.detail) ? data.detail : response.statusText
        console.error('[useApi] API error:', response.status, errorMsg)
        throw new Error(errorMsg)
      }
      return data
    } catch (error) {
      console.error('[useApi] API error:', error)
      
      // Fallback responses for common endpoints
      if (url === '/health' || url === '/') {
        return {
          status: "offline",
          message: "Backend is currently unavailable",
          timestamp: new Date().toISOString(),
          version: "1.0.0",
          server: "fallback"
        }
      }
      
      if (url === '/api/v1/status') {
        return {
          status: "offline",
          services: {
            backend: "unavailable",
            database: "unavailable",
            ai: "unavailable"
          },
          uptime: "0 seconds",
          server: "fallback"
        }
      }
      
      // For other endpoints, show offline message
      throw new Error('Backend is currently unavailable. Please try again later.')
    }
  }
} 