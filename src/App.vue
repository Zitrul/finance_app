<template>
  <v-app>
    <UsualBar v-if="current_route != '/'">{{ route_name }}</UsualBar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import LandingBar from '@/components/LandingBar.vue'
import UsualBar from '@/components/UsualBar.vue'
import * as fun from '@/functions.js'

export default {
  name: 'App',
  components: {
    LandingBar,
    UsualBar
  },
  data () {
    return {
    }
  },
  computed: {
    current_route(){
      return this.$router.currentRoute.value.fullPath
    },
    route_name(){
      return this.$router.currentRoute.value.name
    },
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

.message-error{
    position: fixed;
    top: 10vh;
    right: -200px;
    background-color: #ff2d1f;
    color: white;
    padding: 10px;
    transition: transform 0.5s, opacity 0.5s;
}
.message-success{
    position: fixed;
    top: 10vh;
    right: -200px;
    background-color: green;
    color: white;
    padding: 10px;
    transition: transform 0.5s, opacity 0.5s;
}
</style>