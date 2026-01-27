import './assets/main.css'
import 'primeicons/primeicons.css'

import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import ToastService from 'primevue/toastservice'

import App from './App.vue'

const el = document.getElementById('app')
if (el) {
    const data = {...el.dataset}
    const app = createApp(App, data)

    app.use(PrimeVue, {
        theme: {
            preset: Aura,
            options: {
                darkModeSelector: '.dark-mode'
            }
        }
    })
    app.use(ToastService)

    app.mount('#app')
}
