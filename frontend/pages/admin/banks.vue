<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'

const { $get } = useApi()

type Errors = Record<string, string>

const items = ref<any[]>([])
const loading = ref(false)
const toast = reactive<{ type:'success'|'error'|null, text:string }>(
  { type:null, text:'' }
)

const form = reactive({ 
  name:'', 
  bic:'', 
  country:'KZ', 
  city:'', 
  rating:'', 
  swift:'', 
  license_number:'', 
  site:'' 
})

const errors = reactive<Errors>({})               
const generalErrors = ref<string[]>([])          

async function load() {
  const data:any = await $get('/banks/')
  items.value = data.results
}

async function isBicExists(bic:string) {
  if (!bic) return false
  const data:any = await $get('/banks/', { params: { search: bic } })
  return data.results.some((b:any) => String(b.bic).toLowerCase() === bic.toLowerCase())
}

function validate(): { fieldErrors: Errors; list: string[] } {
  const field: Errors = {}
  const list: string[] = []

  if (!form.name.trim()) field.name = "Название обязательно"

  if (!/^[A-Z0-9]{8,11}$/i.test(form.bic)) {
    field.bic = "BIC должен быть 8–11 символов (только буквы и цифры)"
  }

  if (form.rating !== '') {
    const n = Number(form.rating)
    if (Number.isNaN(n) || n < 0 || n > 100) {
      field.rating = "Рейтинг должен быть не длинее 2-х символов"
    }
  }

  if (form.license_number && form.license_number.length > 32) {
    field.license_number = "Лицензия слишком длинная (макс 32)"
  }

  Object.values(field).forEach(msg => list.push(msg))
  return { fieldErrors: field, list }
}

function parseServerErrors(payload:any) {
  const field: Errors = {}
  const list: string[] = []

  if (payload && typeof payload === 'object') {
    for (const [k, v] of Object.entries(payload)) {
      if (Array.isArray(v)) {
        const msg = v.join(' ')
        if (k === 'non_field_errors') list.push(msg)
        else field[k] = msg
      } else if (typeof v === 'string') {
        if (k === 'non_field_errors') list.push(v)
        else field[k] = v
      }
    }
  } else {
    list.push('Не удалось создать запись')
  }

  return { field, list }
}

function showToast(type:'success'|'error', text:string, ms=2500) {
  toast.type = type
  toast.text = text
  setTimeout(() => { toast.type = null; toast.text = '' }, ms)
}

async function create() {
  Object.keys(errors).forEach(k => delete errors[k])
  generalErrors.value = []

  const { fieldErrors, list } = validate()
  Object.assign(errors, fieldErrors)
  generalErrors.value = [...list]

  if (list.length) return

  loading.value = true
  try {
    if (await isBicExists(form.bic)) {
      errors.bic = "Банк с таким BIC уже существует"
      generalErrors.value.push(errors.bic)
      return
    }

    const body = {
      name: form.name.trim(),
      bic: form.bic.trim(),
      country: form.country || null,
      city: form.city || null,
      rating: form.rating === '' ? null : Number(form.rating),
      swift: form.swift || null,
      license_number: form.license_number || null,
      site: form.site || null,
    }

    await $get('/banks/', { method:'POST', body })

    form.name = ''
    form.bic = ''
    form.country = 'KZ'
    form.city = ''
    form.rating = ''
    form.swift = ''
    form.license_number = ''
    form.site = ''

    await load()
    showToast('success', 'Банк успешно создан')
  } catch (e:any) {
    const data = e?.response?._data
    if (data) {
      const { field, list } = parseServerErrors(data)
      Object.assign(errors, field)
      generalErrors.value = list
      showToast('error', 'Исправьте ошибки в форме')
    } else {
      generalErrors.value = ['Не удалось создать запись']
      showToast('error', 'Ошибка сети или сервера')
    }
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="admin-container">
    <h1>Админ / Банки</h1>

    <div v-if="generalErrors.length" class="alert alert--error" role="alert" aria-live="assertive">
      <strong>Проверьте форму:</strong>
      <ul>
        <li v-for="(msg,i) in generalErrors" :key="i">{{ msg }}</li>
      </ul>
    </div>

    <div class="form-grid">
      <div class="field">
        <input
          v-model="form.name"
          placeholder="название"
          :class="{'input--invalid': !!errors.name}"
          aria-invalid="true"
          aria-describedby="err-name"
        />
        <p v-if="errors.name" id="err-name" class="field__error">{{ errors.name }}</p>
      </div>

      <div class="field">
        <input
          v-model="form.bic"
          placeholder="BIC"
          :class="{'input--invalid': !!errors.bic}"
          aria-invalid="true"
          aria-describedby="err-bic"
        />
        <p v-if="errors.bic" id="err-bic" class="field__error">{{ errors.bic }}</p>
      </div>

      <div class="field">
        <input v-model="form.country" placeholder="страна" />
      </div>

      <div class="field">
        <input v-model="form.city" placeholder="город" />
      </div>

      <div class="field">
        <input
          v-model="form.rating"
          placeholder="рейтинг (0-100)"
          :class="{'input--invalid': !!errors.rating}"
          aria-invalid="true"
          aria-describedby="err-rating"
          inputmode="numeric"
        />
        <p v-if="errors.rating" id="err-rating" class="field__error">{{ errors.rating }}</p>
      </div>

      <div class="field">
        <input v-model="form.swift" placeholder="SWIFT" />
      </div>

      <div class="field">
        <input
          v-model="form.license_number"
          placeholder="лицензия"
          :class="{'input--invalid': !!errors.license_number}"
          aria-invalid="true"
          aria-describedby="err-license"
        />
        <p v-if="errors.license_number" id="err-license" class="field__error">{{ errors.license_number }}</p>
      </div>

      <div class="field field--full">
        <input v-model="form.site" placeholder="сайт" />
      </div>
    </div>

    <button class="create-btn" :disabled="loading" @click="create">
      <span v-if="!loading">Создать</span>
      <span v-else>Сохраняю…</span>
    </button>

    <ul class="bank-list">
      <li v-for="b in items" :key="b.id">{{ b.name }} ({{ b.bic }})</li>
    </ul>

    <div v-if="toast.type" class="toast" :class="{'toast--success': toast.type==='success','toast--error': toast.type==='error'}" role="status" aria-live="polite">
      {{ toast.text }}
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  max-width: 760px;
  margin: 24px auto;
  padding: 16px;
}
.alert {
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 12px;
  border: 1px solid transparent;
  background: #fff4f4;
  border-color: #ffd4d4;
  color: #8a1f1f;
}
.alert ul { margin: 6px 0 0; padding-left: 18px; }

.form-grid {
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 10px;
  margin: 12px 0 6px;
}
.field { display: flex; flex-direction: column; }
.field--full { grid-column: 1 / -1; }

.form-grid input {
  padding: 8px 10px;
  border: 1px solid #cfd3d8;
  border-radius: 8px;
  outline: none;
  transition: border-color .15s ease, box-shadow .15s ease;
}
.form-grid input:focus {
  border-color: #5b8df7;
  box-shadow: 0 0 0 3px rgba(91,141,247,.15);
}
.input--invalid {
  border-color: #e05252 !important;
  box-shadow: 0 0 0 3px rgba(224,82,82,.12);
}
.field__error {
  color: #c0392b;
  font-size: 12px;
  margin: 6px 2px 0;
}

.create-btn {
  padding: 10px 14px;
  margin-top: 8px;
  border: none;
  background: #0070f3;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}
.create-btn:hover { background: #0059c1; }
.create-btn:disabled {
  opacity: .6;
  cursor: not-allowed;
}

.bank-list {
  margin-top: 16px;
  list-style: none;
  padding: 0;
}
.bank-list li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

/* toast */
.toast {
  position: fixed;
  right: 16px;
  bottom: 16px;
  padding: 10px 14px;
  border-radius: 10px;
  background: #333;
  color: #fff;
  box-shadow: 0 8px 24px rgba(0,0,0,.15);
  z-index: 9999;
}
.toast--success { background: #1ea160; }
.toast--error { background: #c93a3a; }
</style>
