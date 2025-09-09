export default defineNuxtRouteMiddleware((to) => {
  const { token } = useApi()
  if (to.path.startsWith('/admin') && !token.value) {
    return navigateTo('/login')
  }
})
