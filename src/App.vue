<template>
  <v-app>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import LandingBar from '@/components/LandingBar.vue'

export default {
  name: 'App',
  components: {
    LandingBar
  },
  data () {
    return {
    }
  }
}
</script>

<style>
.text_title_color{
  color: #9cbbc6;
}
</style>