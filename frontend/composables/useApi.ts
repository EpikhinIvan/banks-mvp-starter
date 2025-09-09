export const useApi = () => {
  const config = useRuntimeConfig()
  const token = useState<string | null>('token', () => null)

  const $get = (url: string, opts: any = {}) =>
    $fetch(url, {
      baseURL: config.public.apiBase,
      credentials: 'include',
      headers: token.value ? { Authorization: `Bearer ${token.value}` } : {},
      ...opts
    })

  const setToken = (t: string | null) => token.value = t
  return { $get, setToken, token }
}
