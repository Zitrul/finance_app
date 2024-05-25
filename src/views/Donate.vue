<template>
    <ContentWrapper>
        <v-row cols="12" class="d-flex flex-row justify-center">
          <v-col class="d-flex flex-column ">
            <iframe src="https://yoomoney.ru/quickpay/fundraise/button?billNumber=128DVDF9SVC.240421&" width="330" height="50" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
            <img :src="require('@/assets/img/poor_coder.jpg')" style="max-height: calc(100vh - 500px);">
          </v-col>
        </v-row>
    </ContentWrapper>
</template>

<script setup>
import { useDisplay } from 'vuetify'

// Destructure only the keys you want to use
const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
</script>

<script>
import UsualBar from '@/components/UsualBar.vue'
import ContentWrapper from '@/components/ContentWrapper.vue'
import * as fun from "@/functions.js";

export default {
  name: "News",
  components: {
    ContentWrapper,
  },
  data() {
    return {
    };
  },
  mounted() {
  },
};
</script>

<style scoped>
</style>