import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

const el = document.getElementById('app')
if (el) {
    console.log(el.dataset)
    const data = {...el.dataset}  // < removed duplicate keys and gets all values out of an object into another object
    console.log(data)
    // <App :token="abc" "user="some-user" />
    createApp(App, data).mount('#app')
}
