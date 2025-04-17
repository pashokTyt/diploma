// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import MonitoringPage from '../components/MonitoringPage.vue';
import StatisticsPage from '../components/StatisticsPage.vue';
import StatNew from '../components/trash.vue';

/* тут указываются пути, по которым переходить надо */
const routes = [
  { path: '/', component: HomePage },
  { path: '/monitoring', component: MonitoringPage },
  { path: '/statistics', component: StatNew },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
