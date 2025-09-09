<script setup lang="ts">
const route = useRoute()
const { $get } = useApi()
const bank = ref<any>(null)
onMounted(async () => bank.value = await $get(`/banks/${route.params.id}/`))
</script>

<template>
  <div v-if="bank" class="bank-detail">
    <h1>{{ bank.name }}</h1>
    <p><b>БИК:</b> {{ bank.bic }}</p>
    <p><b>Страна:</b> {{ bank.country }}</p>
    <p v-if="bank.swift"><b>SWIFT:</b> {{ bank.swift }}</p>
    <p v-if="bank.license_number"><b>Лицензия:</b> {{ bank.license_number }}</p>
    <p v-if="bank.site"><a :href="bank.site" target="_blank">Website</a></p>
  </div>
</template>

<style scoped>
.bank-detail {
  max-width: 760px;
  margin: 24px auto;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #fafafa;
}
.bank-detail h1 {
  margin-bottom: 16px;
}
.bank-detail a {
  color: #0070f3;
  text-decoration: none;
}
.bank-detail a:hover {
  text-decoration: underline;
}
</style>
