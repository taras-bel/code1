<template>
  <button 
    @click="logout"
    class="text-gray-700 hover:text-red-600 font-medium transition-colors"
  >
    Выйти
  </button>
</template>

<script setup>
const logout = () => {
  // Удаляем токен
  localStorage.removeItem('access_token')
  
  // Уведомляем другие компоненты об изменении токена
  window.dispatchEvent(new StorageEvent('storage', {
    key: 'access_token',
    newValue: null
  }))
  
  // Перенаправляем на главную страницу
  window.location.href = '/'
}
</script> 