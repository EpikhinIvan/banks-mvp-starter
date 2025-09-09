<template>
  <div class="home-container">
    <h2 class="home-title">Главная</h2>
    <nav class="home-nav">
      <NuxtLink to="/banks" class="nav-link">Список банков</NuxtLink>
      <NuxtLink to="/login" class="nav-link">Войти</NuxtLink>
      <NuxtLink to="/register" class="nav-link">Регистрация</NuxtLink>
    </nav>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 760px;
  margin: 40px auto;
  text-align: center;
  font-family: Arial, sans-serif;
}

.home-title {
  font-size: 28px;
  margin-bottom: 20px;
  color: #2c3e50;
}

.home-nav {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.nav-link {
  display: inline-block;
  padding: 10px 18px;
  border: 2px solid #3498db;
  border-radius: 8px;
  text-decoration: none;
  color: #3498db;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: #3498db;
  color: #fff;
}
</style>
