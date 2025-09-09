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

async function exportBanks() {
  try {
    const blob = await $get('/banks/export/', { responseType: 'blob' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'banks.xlsx'
    a.click()
    URL.revokeObjectURL(url)
  } catch (e:any) {
    alert("Ошибка экспорта: " + e.message)
  }
}

</script>

<template>
  <div class="banks">
    <div class="banks__head">
      <h1>Банки</h1>

      <div class="banks__filters">
        <input v-model="q.search" placeholder="Поиск…" />
        <select v-model="q.ordering" aria-label="Сортировка">
          <option value="name">Название</option>
          <option value="-rating">Рейтинг ⬇</option>
          <option value="rating">Рейтинг ⬆</option>
        </select>
        <input v-model="q.country" placeholder="Страна" />
        <input v-model="q.min_rating" placeholder="Мин. рейтинг" />
        <input v-model="q.max_rating" placeholder="Макс. рейтинг" />
        <button class="btn btn--ghost" @click="exportBanks">Экспорт</button>
      </div>
    </div>

    <div class="table-wrap">
      <table class="tbl">
        <thead>
          <tr>
            <th style="width:48%">Название</th>
            <th style="width:28%">Страна</th>
            <th style="width:24%" class="th--right">Рейтинг</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in banks.results" :key="b.id">
            <td class="td--name">
              <NuxtLink :to="`/banks/${b.id}`" class="link">{{ b.name }}</NuxtLink>
              <div class="td-sub" v-if="b.city">{{ b.city }}</div>
            </td>
            <td>{{ b.country || '—' }}</td>
            <td class="td--right">{{ b.rating ?? '—' }}</td>
          </tr>

          <tr v-if="banks.results.length === 0">
            <td colspan="3" class="td--empty">Ничего не найдено по текущим фильтрам</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pager">
      <button class="btn" :disabled="q.page<=1" @click="q.page--">Назад</button>
      <span class="pager__info">
        Стр. {{ q.page }} · всего {{ banks.count || 0 }}
      </span>
      <button class="btn" :disabled="banks.count<=q.page*10" @click="q.page++">Вперёд</button>
    </div>

    <div v-if="!token" class="notice">* Для полной информации войдите</div>
  </div>
</template>

<style scoped>

.banks { 
  max-width: 960px; 
  margin: 24px auto; 
  padding: 12px; 
}

.banks__head h1 { 
  font-size: 28px; 
  margin: 0 0 12px; 
}

.banks__filters { 
  display: grid; 
  grid-template-columns: 1fr 180px 1fr 1fr 1fr auto; 
  gap: 8px; 
}

@media (max-width: 820px) {
  .banks__filters { 
    grid-template-columns: 1fr 1fr; 
  }
}

.banks__filters input, .banks__filters select {
  height: 36px; 
  padding: 0 10px; 
  border: 1px solid #dcdfe4; 
  border-radius: 8px; 
  background: #fff;
  outline: none; 
  transition: border .15s, box-shadow .15s;
}

.banks__filters input:focus, .banks__filters select:focus {
  border-color: #7aa8ff; 
  box-shadow: 0 0 0 3px rgba(122,168,255,.2);
}

.btn {
  display:inline-flex; 
  align-items:center; 
  gap:6px;
  padding: 8px 14px; 
  border-radius: 8px; 
  border: 1px solid #1a73e8;
  background:#1a73e8; 
  color:#fff; 
  cursor:pointer; 
  font-weight:500;
}

.btn:disabled { 
  opacity:.45; 
  cursor:not-allowed; 
}

.btn--ghost { 
  background:#fff; 
  color:#1a73e8; 
  border-color:#c9dbff; 
}

.btn--ghost:hover { 
  background:#f5f8ff; 
}

.table-wrap { 
  margin-top: 14px; 
  border: 1px solid #eceff3; 
  border-radius: 12px; 
  overflow: hidden; 
  box-shadow: 0 1px 2px rgba(0,0,0,.03); 
}

.tbl { 
  width: 100%; 
  border-collapse: collapse; 

}
.tbl thead th {
  text-align: left; 
  font-weight: 600; 
  font-size: 13px; 
  color: #4b5563;
  background: linear-gradient(#f9fafb, #f1f5f9); 
  padding: 12px 14px; 
  position: sticky; 
  top: 0; 
  z-index: 1;
  border-bottom: 1px solid #e5e7eb;
}

.tbl tbody td { 
  padding: 12px 14px; 
  border-bottom: 1px solid #f2f4f7; 
  vertical-align: middle; 
}


.tbl tbody tr:hover { 
  background: #fafcff; 
}

.th--right, .td--right { 
  text-align: right; 
}

.td--name { 
  font-weight: 600; 

}

.td-sub { 
  font-weight: 400; 
  font-size: 12px; 
  color: #6b7280; 
  margin-top: 2px; 
}

.td--empty { 
  text-align: center; 
  color: #6b7280; 
  padding: 28px 12px; 
}


.link { 
  color:#1a73e8; 
  text-decoration:none; 
}
.link:hover { 
  text-decoration: underline; 

}


.pager { 
  display:flex; 
  align-items:center; 
  gap:10px; 
  margin-top: 14px; 

}

.pager__info { 
  font-size: 13px; 
  color:#6b7280; 
}
.table-wrap { 
  overflow-x: auto; 
}

.tbl { 
  min-width: 560px; 
}
.notice { 
  margin-top: 12px; 
  color:#6b7280; 
  font-style: italic; 
  }

</style>
