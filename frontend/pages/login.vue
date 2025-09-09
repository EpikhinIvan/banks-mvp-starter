<script setup lang="ts">
const username = ref('')
const password = ref('')
const { $get, setToken } = useApi()
async function login() {
  try {
    const data:any = await $get('/auth/token/', {
      method: 'POST',
      body: { username: username.value, password: password.value }
    })
    setToken(data.access)
    await navigateTo('/banks')
  } catch (e:any) {
    alert('Ошибка входа')
  }
}
</script>

<template>
  <div class="auth-container">
    <h1>Вход</h1>
    <input v-model="username" placeholder="username" />
    <input v-model="password" type="password" placeholder="password" />
    <button @click="login">Войти</button>
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
  background: #0070f3;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}
.auth-container button:hover {
  background: #0059c1;
}
</style>
