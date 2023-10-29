import { createApp, configureCompat } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'

import VueApexCharts from 'vue3-apexcharts'

import PrimeVue from 'primevue/config';
import Sidebar from 'primevue/sidebar'
import 'primevue/resources/themes/lara-light-teal/theme.css'


const app = createApp(App)

app.use(router)
app.use(PrimeVue);

app.component('apexchart', VueApexCharts)
app.component('Sidebar', Sidebar);

app.mount('#app')
