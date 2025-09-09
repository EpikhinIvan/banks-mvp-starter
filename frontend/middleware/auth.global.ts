export default defineNuxtRouteMiddleware((to) => {
  const { token, user, ensureFromStorage } = useApi()
  ensureFromStorage()

  const cookieTok = useCookie<string | null>('token').value
  const hasAuth   = !!(token.value || cookieTok)
  const isStaff   = !!(user.value?.is_staff)

  if (!hasAuth && to.path.startsWith('/admin')) {
    return navigateTo('/login')
  }

  if (hasAuth && (to.path === '/login' || to.path === '/register')) {
    return navigateTo('/banks')
  }

})
