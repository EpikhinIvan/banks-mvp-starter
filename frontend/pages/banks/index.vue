<script setup lang="ts">
const q = reactive({ page:1, search:'', ordering:'name', country:'', min_rating:'', max_rating:'' })
const { $get, token } = useApi()
const banks = ref<any>({ results:[], count:0 })

async function load() {
  const params:any = { page:q.page, ordering:q.ordering }
  if (q.search) params.search = q.search
  if (q.country) params.country = q.country
  if (q.min_rating) params.min_rating = q.min_rating
  if (q.max_rating) params.max_rating = q.max_rating
  banks.value = await $get('/banks/', { params })
}
watch(q, load, { deep:true })
onMounted(load)
</script>

<template>
  <div class="banks-container">
    <h1 class="banks-title">Banks</h1>

    <div class="banks-filters">
      <input v-model="q.search" placeholder="Поиск..." />
      <select v-model="q.ordering">
        <option value="name">Name</option>
        <option value="-rating">Rating ⬇</option>
        <option value="rating">Rating ⬆</option>
      </select>
      <input v-model="q.country" placeholder="Country" />
      <input v-model="q.min_rating" placeholder="Min rating" />
      <input v-model="q.max_rating" placeholder="Max rating" />
    </div>

    <ul class="banks-list">
      <li v-for="b in banks.results" :key="b.id" class="banks-item">
        <NuxtLink :to="`/banks/${b.id}`" class="bank-link">{{ b.name }}</NuxtLink>
        <span class="bank-meta">· {{ b.country }} · rating: {{ b.rating ?? '-' }}</span>
      </li>
    </ul>

    <div class="banks-pagination">
      <button :disabled="q.page<=1" @click="q.page--">Prev</button>
      <button :disabled="banks.count<=q.page*10" @click="q.page++">Next</button>
    </div>

    <div v-if="!token" class="banks-warning">
      * Для полной информации войдите
    </div>
  </div>
</template>

<style scoped>
.banks-container {
  max-width: 760px;
  margin: 24px auto;
  padding: 16px;
}

.banks-title {
  font-size: 26px;
  margin-bottom: 16px;
}

.banks-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.banks-filters input,
.banks-filters select {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  flex: 1;
  min-width: 120px;
}

.banks-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.banks-item {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.bank-link {
  font-weight: 500;
  color: #0070f3;
  text-decoration: none;
}

.bank-link:hover {
  text-decoration: underline;
}

.bank-meta {
  margin-left: 8px;
  color: #555;
  font-size: 14px;
}

.banks-pagination {
  margin-top: 16px;
  display: flex;
  gap: 8px;
}

.banks-pagination button {
  padding: 6px 12px;
  border: none;
  background: #0070f3;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
}

.banks-pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.banks-warning {
  margin-top: 16px;
  color: #666;
  font-style: italic;
}
</style>
