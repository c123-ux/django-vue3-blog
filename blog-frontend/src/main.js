import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

app.config.errorHandler = (err, instance, info) => {
  console.error('[Vue Error]', info, err)
}

app.config.warnHandler = (msg, instance, trace) => {
  console.warn('[Vue Warn]', msg)
}

window.addEventListener('unhandledrejection', (event) => {
  console.error('[Unhandled Promise]', event.reason)
})

app.use(pinia)
app.use(router)
app.mount('#app')
