// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'


const myDarkTheme = {
  dark: true,
  colors: {
    background: '#0c1d27',
    surface: '#0c1d27',
    primary: '#d5573b',
    text_title: '#9cbbc6',
    sell: '#bc2402',
  },
  variables: {
    'border-color': '#d5573b',
  }
}

export default createVuetify({
  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
  theme: {
    defaultTheme: 'myDarkTheme',
    themes: {
      myDarkTheme
    }
  }
})
