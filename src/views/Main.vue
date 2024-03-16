<template>
    <v-app @scroll="handleScroll()" class="background_line">

    <LandingBar @sign_clicked="sign_form_opened = !sign_form_opened"></LandingBar>
    <v-overlay v-model="sign_form_opened" class="align-center justify-center">
      <Sign @closed="sign_form_opened = false"></Sign>
    </v-overlay>


        <v-container fluid :class="{'h-screen': mdAndUp, 'my-1': true}">
            <v-row wrap>
              <v-col xs12 md5>

                <p :class="{
                  'text-h2': xlAndUp,
                  'text-h3': lgAndDown,
                  'text-right': mdAndUp,
                  'text-center': smAndDown,
                  'text_title_color': true, 'font-weight-medium': true, 'ls-1': true, 'mb-16': true}">Money Minder</p>

                <v-row>
                  <v-spacer v-if="mdAndUp"></v-spacer>
                  <v-spacer v-if="mdAndUp"></v-spacer>
                  <v-spacer v-if="mdAndUp"></v-spacer>
                  <v-spacer v-if="mdAndUp"></v-spacer>

                  <v-spacer></v-spacer>
                  <v-img
                  :src="require('@/assets/img/landing_guy.png')"
                  :width="smAndDown ? '80vw' : '20vw'"
                  cover
                  aspect-ratio="1/1">
                  </v-img>
                  <v-spacer></v-spacer>
                </v-row>

              </v-col>
              <v-col :class="{'d-flex': true, 'flex-column': smAndDown, 'align-end': true}">

                <v-row :class="{ 'text-right': mdAndUp }">
                  <v-spacer v-if="mdAndUp"></v-spacer>
                  <p :class="{
                  'text-h1': xlAndUp,
                  'text-h2': lgAndDown,
                  'mt-8': smAndDown,
                  'text_title_color': true, 'font-weight-medium': true, 'ls-1': true, 'mb-16': true, 'text-bottom': true}">Как начать<br>здоровые<br>отношения<br>с деньгами?</p>
                  <v-spacer v-if="mdAndUp"></v-spacer>
                  <v-col cols="2" v-if="smAndDown"></v-col>
                </v-row>

              </v-col>
            </v-row>
        </v-container>

        <v-container fluid class="my-1">
            <v-row wrap>
              <v-col xs12 md5>
                
                <v-row>
                  <v-col cols="2" v-if="mdAndUp"></v-col>
                  <v-col>
                    <p :class="{
                    'text-h5': xlAndUp,
                    'text-h6': lgAndDown,
                    'mb-16': true, 'font-weight-light': true}"><span class="text-primary"><strong>Money Minder</strong></span> - это отличное приложение для тех, кто хочет<br><span class="text-primary">эффективно</span> управлять своими финансами. С его помощью пользователь может легко <span class="text-primary">отслеживать</span> все свои доходы и расходы, <span class="text-primary">контролировать</span> свои траты и планировать бюджет.</p>
                  </v-col>
                  
                </v-row>

                <v-row>
                  <v-spacer v-if="mdAndUp"></v-spacer>
                  <v-img
                  :src="require('@/assets/img/news_landing.png')"
                  :width="smAndDown ? '95vw' : '45vw'"
                  cover
                  aspect-ratio="1/1"
                  :class="{'mb-5': smAndDown}">
                  </v-img>
                </v-row>

              </v-col>
              <v-col :class="{'d-flex': true, 'flex-column': smAndDown, 'align-center': true}">

                <v-row>
                  <v-spacer></v-spacer>
                  <v-img
                  ref="image"
                  class="rotating_image"

                  :src="require('@/assets/img/tool_circle.png')"
                  :width="smAndDown ? '70vw' : '20vw'"
                  cover
                  aspect-ratio="1/1">
                  </v-img>
                  <v-spacer></v-spacer>
                </v-row>

              </v-col>
            </v-row>
        </v-container>
    </v-app>
    <div class="absolute_forms">
        
    </div>
</template>

<script setup>
import { useDisplay } from 'vuetify'

// Destructure only the keys you want to use
const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
</script>

<script>
import Sign from "@/components/Sign.vue";
import LandingBar from '@/components/LandingBar.vue'
import * as fun from "@/functions.js";

export default {
  name: "Main",
  components: {
    Sign,
    LandingBar,
  },
  data() {
    return {
      sign_form_opened: false,
    };
  },
  mounted() {
    fun.check_auth(this).then(response => {
      if(response){
        this.$router.push('/wallet')
      }
    })
  },
  methods: {
    handleScroll() {
      console.log(this.$refs.image);
      const scrollY = window.scrollY;
      const rotationAngle = scrollY / 10; // Устанавливаем угол поворота в зависимости от прокрутки

      const imageElement = this.$refs.image; // Проверяем существование элемента
      if (imageElement) {
        this.$refs.image.style.transform = `rotate(${ rotationAngle }deg)`;
      }
    },
  },
};
</script>

<style scoped>
.rotating_image{
  animation: rotate 15s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.background_line{
  background-image: url('../assets/img/landing_line.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}
.absolute_forms{
  position: fixed;
}
</style>