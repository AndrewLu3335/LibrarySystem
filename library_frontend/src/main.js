import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// axios.defaults.baseURL = 'http://localhost:5000' // 注释掉，使用 Vite 代理

const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')
