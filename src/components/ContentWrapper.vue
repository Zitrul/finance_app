<template>
    <v-app>
        <v-main>
            <v-container fluid :class="{'ml-16': lgAndUp, 'pl-16': true, 'ml-2': mdAndDown, 'd-flex': true, 'justify-center': true}">
                <slot></slot>
            </v-container>
        </v-main>
    </v-app>
</template>

<script setup>
import { useDisplay } from 'vuetify'

// Destructure only the keys you want to use
const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
</script>

<script>
import * as fun from '@/functions.js'
import { useDisplay } from 'vuetify'

export default {
    name: 'ContentWrapper',
    data(){
        return {
        }
    },
    methods: {
    },
    mounted(){
    },
}
</script>

<style scoped>
</style>