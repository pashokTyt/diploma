import { createApp } from 'vue';

/* import PrimeVue from 'primevue/config';
import { Aura } from '@primevue/themes'; */
/* 
import Button from 'primevue/button';
import '/home/pavel/Рабочий стол/project2/frontend/node_modules/@primevue/themes/aura'
import 'primevue/resources/primevue.min.css'; // Основные стили PrimeVue
import 'primeicons/primeicons.css'; // Иконки PrimeIcons */


import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import VueApexCharts from 'vue3-apexcharts';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import ru from 'element-plus/es/locale/lang/ru';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import VueAxios from 'vue-axios';


axios.defaults.baseURL = 'http://127.0.0.1:8000';
const app = createApp(App);

/* чет не хочет робить, потом разобраться */
/* app.use(PrimeVue, {
  theme: {
      preset: Aura
  }
}); */
/* 
app.component('Button', Button); */


const pinia = createPinia();
app.use(ElementPlus, {
  locale: ru,
});
app.use(router);
app.use(VueAxios, axios);
app.use(VueApexCharts);
app.use(pinia);

app.mount('#app');
