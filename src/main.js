import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCookies from 'vue-cookies';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

library.add(fas);
loadFonts()
/* eslint-disable */

const app = createApp(App)
app.config.globalProperties.axios = axios;
app.use(VueCookies);

app.use(router)
  .use(vuetify)
  .component('fa', FontAwesomeIcon)
  .mount('#app');

// axios.defaults.headers['admin_pass'] = `${app.$cookies.get('pass')}`;