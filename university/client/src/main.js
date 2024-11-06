// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'  // Импортируйте ваш роутер
import store from './store'    // Подключите Vuex, если используется

createApp(App)
  .use(router)  // Используйте ваш роутер
  .use(store)
  .mount('#app')