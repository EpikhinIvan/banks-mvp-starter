<script setup lang="ts">
const { $get } = useApi()
const items = ref<any[]>([])
const form = reactive({ name:'', bic:'', country:'KZ', city:'', rating:'', swift:'', license_number:'', site:'' })

async function load(){
  const data:any = await $get('/banks/')
  items.value = data.results
}
async function create(){
  await $get('/banks/', { method:'POST', body: form })
  Object.keys(form).forEach(k => (form as any)[k] = '')
  await load()
}
onMounted(load)
</script>

<template>
  <div class="admin-container">
    <h1>Admin / Banks</h1>

    <div class="form-grid">
      <input v-model="form.name" placeholder="name" />
      <input v-model="form.bic" placeholder="bic" />
      <input v-model="form.country" placeholder="country" />
      <input v-model="form.city" placeholder="city" />
      <input v-model="form.rating" placeholder="rating" />
      <input v-model="form.swift" placeholder="swift" />
      <input v-model="form.license_number" placeholder="license" />
      <input v-model="form.site" placeholder="site" />
    </div>

    <button class="create-btn" @click="create">Create</button>

    <ul class="bank-list">
      <li v-for="b in items" :key="b.id">{{ b.name }} ({{ b.bic }})</li>
    </ul>
  </div>
</template>

<style scoped>
.admin-container {
  max-width: 760px;
  margin: 24px auto;
  padding: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 8px;
  margin: 12px 0;
}

.form-grid input {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.create-btn {
  padding: 8px 12px;
  margin-top: 8px;
  border: none;
  background: #0070f3;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
}
.create-btn:hover {
  background: #0059c1;
}

.bank-list {
  margin-top: 16px;
  list-style: none;
  padding: 0;
}
.bank-list li {
  padding: 6px 0;
  border-bottom: 1px solid #eee;
}
</style>
