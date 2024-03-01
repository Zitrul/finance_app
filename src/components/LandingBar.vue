<template>
    <nav>
        <v-toolbar color="surface">
            
        </v-toolbar>
        <v-toolbar color="surface" class="fixed-bar">
            <v-row>
            <v-col class="ml-3">
                <v-img
                :src="require('@/assets/img/logo.png')"
                width="3em"
                cover
                aspect-ratio="1/1">
                </v-img>
            </v-col>
            <v-col></v-col>
            </v-row>
            
            <v-spacer></v-spacer>
            <v-btn color="primary">
                <font-awesome-icon :icon="['fas', 'arrow-right-to-bracket']"/>
                <p class="text-h6 ml-2 white--text">Войти в аккаунт</p>
            </v-btn>
        </v-toolbar>
        <!-- <v-navigation-drawer :height="10" location="top" class="d-flex justify-space-between">
            <v-img
            :src="require('@/assets/img/logo.png')"
            :height="40"
            contain
            aspect-ratio="1/1">
            </v-img>

            <v-img
            :src="require('@/assets/img/logo.png')"
            :height="40"
            contain
            aspect-ratio="1/1">
            </v-img>
        </v-navigation-drawer> -->
    </nav>
</template>
  
<script>
import * as fun from '@/functions.js'

export default {
    name: 'LandingBar',
}
</script>

<style scoped>
.fixed-bar {
  position: fixed;
  top: 0;
  z-index: 5;
}
</style>