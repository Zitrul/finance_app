<template>
    <nav>

        <v-navigation-drawer
        v-model="drawer"
        :image="require('@/assets/img/money-bg.jpg')"
        :rail="rail"
        :expand-on-hover="mdAndUp"
        :permanent="mdAndUp"
        >
        <v-list 
        class="h-screen d-flex flex-column justify-end fixed-bar_no_z ml-n2"
        >
            <v-list-item>
                <v-list-item-content class="d-flex flex-row">
                    <img :src="require('@/assets/img/logo.png')" class="bottom_img_logo">
                    <div class="mx-5">
                        <v-list-item-title>Money Minder</v-list-item-title>
                        <v-list-item-subtitle>All rights reserved</v-list-item-subtitle>
                    </div>
                </v-list-item-content>
            </v-list-item>
        </v-list>

        <v-list-item
            v-if="smAndDown"
            nav
        >
            <template v-slot:append>
            <v-btn
                icon="mdi-chevron-left"
                variant="text"
                @click.stop="drawer = !drawer"
            ></v-btn>
            </template>
        </v-list-item>

        <v-divider v-if="smAndDown"></v-divider>

        <v-list nav>
            <v-list-item prepend-icon="mdi-wallet" :class="{'text-primary': current_route == '/wallet'}" title="Мои Финансы" value="wallet"></v-list-item>
            <v-list-item prepend-icon="mdi-briefcase-variant" title="Инвестиции" value="investments"></v-list-item>
            <v-list-item prepend-icon="mdi-poll" title="Аналитика" value="analytics"></v-list-item>
        </v-list>

        <v-spacer></v-spacer>

        
        </v-navigation-drawer>

        <v-toolbar color="surface"></v-toolbar>

        <v-toolbar
        class="fixed-bar"
        color="surface"
        >
        <v-app-bar-nav-icon @click="open_nav_drawer();"></v-app-bar-nav-icon>

        <v-spacer></v-spacer>
        <p class="font-weight-medium"><label><slot></slot></label></p>

        <v-spacer></v-spacer>

        <v-btn>
            <font-awesome-icon :icon="['fas', 'user']"/>
            <p class="ml-3">{{ username }}</p>
        </v-btn>
        </v-toolbar>

        
    </nav>
</template>


<script>
import * as fun from '@/functions.js'
import { useDisplay } from 'vuetify'

export default {
    name: 'UsualBar',
    data(){
        return {
            drawer: false,
            rail: false,
            username: "",
        }
    },
    methods: {
        open_nav_drawer() {
            this.drawer = true;
        },
        close_nav_drawer() {
            if(this.mdAndUp) this.rail = !this.rail;
            else this.drawer = false;
        },
    },
    computed: {
        current_route() {
            return this.$route.path;
        },
    },
    mounted(){
        this.drawer = this.smAndUp ? true : false;
        this.rail = this.smAndUp ? true : false;
        this.axios({
            method: 'get',
            url: `${fun.SERVER_URL}/token-test`,
        }).then((response) => {
            if(response.status === 200) {
                this.username = response.data.user.username;
            }
        }).catch((error) => {
            console.log(error)
        })
    },
    setup() {
        const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
        return {
            xs,
            sm,
            smAndDown,
            smAndUp,
            md,
            mdAndDown,
            mdAndUp,
            lg,
            lgAndDown,
            lgAndUp,
            xl,
            xlAndDown,
            xlAndUp,
            xxl
        }
    }
}
</script>

<style scoped>
.fixed-bar {
  position: fixed;
  top: 0;
  z-index: 5;
}
.fixed-bar_no_z {
  position: fixed;
  top: 0;
  z-index: 0;
}
.bottom_img_logo{
    width: 1.95em;
    height: 1.95em;
    background-size: cover;
}
</style>