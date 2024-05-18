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
            <v-list-item prepend-icon="mdi-wallet" :class="{'text-primary': current_route == '/wallet'}" title="Мои Финансы" value="wallet" to="/wallet"></v-list-item>
            <v-list-item prepend-icon="mdi-briefcase-variant" :class="{'text-primary': current_route == '/investing'}" title="Инвестиции" value="investing" to="/investing"></v-list-item>
            <v-list-item prepend-icon="mdi-newspaper" :class="{'text-primary': current_route == '/news'}" title="Новости" value="news"to="/news"></v-list-item>
            <v-list-item prepend-icon="mdi-gift" :class="{'text-primary': current_route == '/donates'}" title="Поддержать" value="donates" to="/donates"></v-list-item>
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

        <v-btn @click="account_opened = true;">
            <font-awesome-icon :icon="['fas', 'user']"/>
            <p class="ml-3">{{ username }}</p>
        </v-btn>
        </v-toolbar>

        <v-dialog
        v-model="account_opened"
        max-width="400"
        persistent
        >
            <v-card
                prepend-icon="mdi-cog"
                title="Настройки аккаунта"
            >
                <v-card-text>
                    <p>Никнейм</p>
                    <v-text-field v-model="account.username" prefix="@" density="compact"></v-text-field>

                    <p>Имя</p>
                    <v-text-field v-model="account.first_name" density="compact"></v-text-field>

                    <p>Фамилия</p>
                    <v-text-field v-model="account.last_name" density="compact"></v-text-field>
                    
                    <p>Email</p>
                    <v-text-field v-model="account.email" density="compact"></v-text-field>
                    

                    <v-btn v-if="account.telegram_auth === true" variant="flat" color="red" block prepend-icon="mdi-account-remove" @click="reset_tg()">Отвзяать Telegram</v-btn>
                    <v-btn v-else variant="flat" elevation="2" block color="#0396de" target="_blank" :href="`https://t.me/MoneyMinderTGBot?start=${String(account.telegram_auth)}`">
                        <img :src="require('@/assets/img/telegram.png')" style="height: 20px;">
                        <p class="ml-2">Привязать Telegram</p>
                    </v-btn>

                    <v-btn variant="text" block color="red-darken-2" append-icon="mdi-logout-variant" density="compact" @click="logout()" class="mt-4">Выйти из аккаунта</v-btn>
                    <!-- <v-btn variant="text" block color="red-darken-2" append-icon="mdi-logout-variant" density="compact" @click="logout">Выйти из аккаунта на всех устройствах</v-btn> -->
                </v-card-text>
                <template v-slot:actions>

                    <v-btn @click="reset_account();">
                        Назад
                    </v-btn>
                    <v-spacer></v-spacer>

                    <v-btn @click="change_account()">
                        Сохранить
                    </v-btn>
                </template>
            </v-card>
        </v-dialog>
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
            account_opened: false,
            account: {},
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
        reset_account(){
            this.account_opened = false;
            this.axios({
                method: 'get',
                url: `${fun.SERVER_URL}/account/account-info`,
            }).then((response) => {
                if(response.status === 200) {
                    this.account = response.data;
                }
            }).catch((error) => {
                console.log(error)
            });
        },
        change_account(){
            this.axios({
                method: 'put',
                url: `${fun.SERVER_URL}/account/change-account-info`,
                data: this.account,
            }).then((response) => {
                if(response.status === 200) {
                    fun.show(this, "Данные успешно обновлены", true);
                    this.username = this.account.username;
                    this.account_opened = false;
                }
            }).catch((error) => {
                fun.show(this, "Такой email или никнейм уже занят");
                this.account_opened = false;
            });
        },
        reset_tg(){
            this.axios({
                method: 'post',
                url: `${fun.SERVER_URL}/account/reset-telegram`,
            }).then((response) => {
                if(response.status === 200) {
                    fun.show(this, "Telegram успешно отвязан", true);
                    this.get_account_info();
                }
            }).catch((error) => {
                fun.show(this, "Такой email или никнейм уже занят");
                this.account_opened = false;
            });
        },
        logout(){
            this.$cookies.keys().forEach(cookie => {
                this.$cookies.remove(cookie);
            })
            this.$router.push('/');
        },
        get_account_info(){
            this.axios({
                method: 'get',
                url: `${fun.SERVER_URL}/account/account-info`,
            }).then((response) => {
                this.account = response.data;
                console.log(this.account)
                this.username = response.data.username;
            }).catch((error) => {
                console.log(error)
            });
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

        this.get_account_info();
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