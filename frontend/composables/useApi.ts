export const useApi = () => {
  const config = useRuntimeConfig()
  const token = useState<string | null>('token', () => null)
  const user  = useState<any | null>('user', () => null)

  const decodeJWT = (t: string) => {
    try {
      const payload = t.split('.')[1]
      const json = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
      return JSON.parse(json)
    } catch {
      return null
    }
  }

  const ensureFromStorage = () => {
    if (!token.value) {
      const c = useCookie<string | null>('token').value
      if (c) token.value = c
    }
    if (process.client && !token.value) {
      const ls = localStorage.getItem('token')
      if (ls) token.value = ls
    }
    if (token.value && !user.value) {
      user.value = decodeJWT(token.value)
    }
  }

  const setToken = (t: string | null) => {
    token.value = t
    user.value  = t ? decodeJWT(t) : null

    const cookie = useCookie<string | null>('token', { sameSite: 'lax', httpOnly: false })
    cookie.value = t

    if (process.client) {
      if (t) localStorage.setItem('token', t)
      else   localStorage.removeItem('token')
    }
  }

  const logout = () => setToken(null)

  const $get = async (url: string, opts: any = {}) => {
    const isBlob = opts.responseType === 'blob'
    const auth = token.value ? { Authorization: `Bearer ${token.value}` } : {}
    const extra = opts.headers || {}

    if (isBlob) {
      const res = await fetch(config.public.apiBase + url, {
        method: opts.method || 'GET',
        headers: { ...auth, ...extra },
      })
      if (!res.ok) throw new Error(`Ошибка экспорта: ${res.status}`)
      return await res.blob()
    }

    return await $fetch(url, {
      baseURL: config.public.apiBase,
      credentials: 'include',
      headers: { ...auth, ...extra },
      ...opts,
    })
  }

  return { $get, setToken, logout, token, user, ensureFromStorage }
}
