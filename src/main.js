import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCookies from 'vue-cookies';
import VueQrcodeReader from 'vue3-qrcode-reader'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

import './assets/tailwind.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

library.add(fas);
loadFonts()
/* eslint-disable */

const app = createApp(App)
app.use(VueCookies);

axios.defaults.headers['authorization'] = `Bearer ${app.$cookies.get('accessToken')}`;
axios.defaults.withCredentials = true;
app.config.globalProperties.axios = axios;

app.use(router)
  .use(vuetify)
  .use(VueQrcodeReader)
  .use(Toast)
  .component('font-awesome-icon', FontAwesomeIcon)
  .mount('#app');
