<script setup lang="ts">
const username = ref('')
const email = ref('')
const password = ref('')
const { $get } = useApi()
async function register() {
  try {
    await $get('/auth/register/', { method: 'POST', body: { username: username.value, email: email.value, password: password.value } })
    alert('Готово, теперь войдите')
    await navigateTo('/login')
  } catch (e:any) {
    alert('Ошибка регистрации')
  }
}
</script>

<template>
  <div class="auth-container">
    <h1>Регистрация</h1>
    <input v-model="username" placeholder="username" />
    <input v-model="email" placeholder="email" />
    <input v-model="password" type="password" placeholder="password" />
    <button @click="register">Создать аккаунт</button>
  </div>
</template>

<style scoped>
.auth-container {
  max-width: 360px;
  margin: 40px auto;
  text-align: center;
}
.auth-container input {
  display: block;
  width: 100%;
  margin: 8px 0;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.auth-container button {
  padding: 8px 12px;
  border: none;
  background: #28a745;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}
.auth-container button:hover {
  background: #1f7d36;
}
</style>
