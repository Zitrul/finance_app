<template>
  <v-app>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import LandingBar from '@/components/LandingBar.vue'
import * as fun from '@/functions.js'

export default {
  name: 'App',
  components: {
    LandingBar
  },
  data () {
    return {
    }
  },
  mounted () {
    fun.check_auth(this).then(response => {
      if((!response) && this.$router.currentRoute.value.fullPath != "/"){
        this.$router.push('/');
      }
    })
  }
}
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

.text_title_color{
  color: #9cbbc6;
}
</style>