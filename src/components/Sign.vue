<template>
    <!-- <v-app>
        <v-container fluid fill-height v-if="signup_active">
            <v-row justify="center">
            <v-col></v-col>
            <v-col cols="12" sm="8" md="3">
                <v-card class="rounded-xl" color="#001a23">

                    <v-card-title class="text-h4 text-center my-4 title">Hello!</v-card-title>

                    <v-card-text>
                        <v-row justify="center">
                        <v-col>
                            <v-text-field class="rounded-pill" label="Full name"></v-text-field>
                            <v-text-field class="rounded-pill" label="Email"></v-text-field>
                            <v-text-field class="rounded-pill" label="Password" type="password"></v-text-field>
                            <v-btn block variant="flat" color="#d5573b" align="center" class="rounded-pill py-6">
                                Create an account
                            </v-btn>
                        </v-col>
                        </v-row>
                    </v-card-text>

                    <v-divider :thickness="2" class="border-opacity-100" color="#d5573b"></v-divider>

                    <v-card-text>
                        <v-row justify="center" class="my-2">
                            <p class="mx-1 text-subtitle-1">Already have an account?</p>
                            <p class="change_form mx-1 text-subtitle-1" @click="signin();">Sign in</p>
                        </v-row>
                    </v-card-text>

                </v-card>
            </v-col>
            <v-col>
                <font-awesome-icon :icon="['fas', 'xmark']" class="cross_icon" @click="emit_closing()"/>
            </v-col>
            </v-row>
        </v-container>
    </v-app> -->
    <v-container fluid justify="center" class="d-flex flex-row align-center" fill-height>
        <v-row justify="center" class="d-flex flex-row">
            <v-col></v-col>
            <v-col cols="12" sm8 md3>
                <v-card class="rounded-xl" color="#001a23" :style="`width: ${xs ? '90vw' : '500px'};`">
                    <div v-if="signup_active">
                        <v-card-title class="text-h4 text-center my-4 title">Здравствуйте!</v-card-title>

                        <v-card-text>
                            <v-row justify="center">
                            <v-col>
                                <v-text-field class="rounded-pill" label="Ваш никнейм" prefix="@" v-model="signup_form.username"></v-text-field>
                                <v-text-field class="rounded-pill" label="Email" v-model="signup_form.email"></v-text-field>
                                <v-text-field class="rounded-pill" label="Пароль" type="password" v-model="signup_form.password"></v-text-field>
                                <!-- <vue-recaptcha v-show="showRecaptcha" sitekey="6LdHluEpAAAAALKfNzf0z2ACB3a5ztj24p0GqqRv"
                                    size="normal" 
                                    theme="dark"
                                    :loading-timeout="loadingTimeout"
                                    @verify="recaptchaVerified"
                                    @expire="recaptchaExpired"
                                    @fail="recaptchaFailed"
                                    @error="recaptchaError"
                                    ref="vueRecaptcha">
                                </vue-recaptcha> -->
                                <v-btn block variant="flat" color="#d5573b" align="center" class="rounded-pill py-6" @click="signup();">
                                    Создать аккаунт
                                </v-btn>
                            </v-col>
                            </v-row>
                        </v-card-text>

                        <v-divider :thickness="2" class="border-opacity-100" color="#d5573b"></v-divider>

                        <v-card-text>
                            <v-row justify="center" class="my-2">
                                <p class="mx-1 text-subtitle-1">Уже есть аккаунт?</p>
                                <p class="change_form mx-1 text-subtitle-1" @click="change_form();">Войти</p>
                            </v-row>
                        </v-card-text>
                    </div>
                    <div v-else>
                        <v-card-title class="text-h4 text-center my-4 title">Войти</v-card-title>

                        <v-card-text>
                            <v-row justify="center">
                            <v-col>
                                <v-text-field class="rounded-pill" label="Никнейм или email" v-model="login.username"></v-text-field>
                                <v-text-field class="rounded-pill" label="Пароль" type="password" v-model="login.password"></v-text-field>
                                <v-btn block variant="flat" color="#d5573b" align="center" class="rounded-pill py-6" @click="signin();">
                                    Войти в аккаунт
                                </v-btn>
                            </v-col>
                            </v-row>
                        </v-card-text>

                        <v-divider :thickness="2" class="border-opacity-100" color="#d5573b"></v-divider>

                        <v-card-text>
                            <v-row justify="center" class="my-2">
                                <p class="mx-1 text-subtitle-1">Еще нет аккаунта?</p>
                                <p class="change_form mx-1 text-subtitle-1" @click="change_form();">Зарегистрироваться</p>
                            </v-row>
                        </v-card-text>
                    </div>
                </v-card>

            </v-col>
            <v-col></v-col>
            <!-- <v-col>
                <font-awesome-icon :icon="['fas', 'xmark']" class="cross_icon" @click="emit_closing()"/>
            </v-col> -->

            <v-overlay
            :model-value="loading"
            class="align-center justify-center"
            >
                <v-progress-circular
                    color="primary"
                    size="64"
                    indeterminate
                ></v-progress-circular>
            </v-overlay>
        </v-row>
    </v-container>
</template>

<script setup>
import { useDisplay } from 'vuetify'

// Destructure only the keys you want to use
const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
</script>
  
<script>
import * as fun from '@/functions.js'
import vueRecaptcha from 'vue3-recaptcha2';

export default {
    name: 'Sign',
    components: {
        vueRecaptcha
    },
    data() {
        return {
            recaptchaResponse: '',
            showRecaptcha: true,
		    loadingTimeout: 30000, // 30 seconds

            signup_active: false,
            loading: false,
            login: {
                username: '',
                password: '',
            },
            signup_form: {
                username: '',
                password: '',
                email: '',
            },
        }
    },
    methods: {
        emit_closing() {
            this.$emit('closed');
        },
        change_form() {
            this.signup_active = !(this.signup_active);
        },
        signin() {
            this.loading = true;
            this.axios({
                method: 'post',
                url: `${fun.SERVER_URL}/authentication/login`,
                data: {
                    username: this.login.username,
                    password: this.login.password
                }
            }).then((response) => {
                console.log(response);
                this.loading = false;

                this.$cookies.set('accessToken', response.data.accessToken);
                this.$cookies.set('refreshToken', response.data.refreshToken);
                fun.show(this, 'Успешный вход в аккаунт', true);
                // this.emit_closing();
                this.$router.push('/wallet');
            }).catch((error) => {
                fun.show(this, 'Введены некорректные данные');
            });
        },
        signup() {
            // if(recaptchaResponse && recaptchaResponse.length > 0){
                this.loading = true;
                this.axios({
                    method: 'post',
                    url: `${fun.SERVER_URL}/authentication/register`,
                    data: {
                        username: this.signup_form.username,
                        email: this.signup_form.email,
                        password: this.signup_form.password
                    }
                }).then((response) => {
                    console.log(response);
                    this.loading = false;
                    if(response.status == 200) {
                        fun.show(this, 'Успешная регистрация', true);
                        this.change_form();
                    }
                    else{
                        fun.show(this, 'Произошла неизвестная ошибка');
                    }
                }).catch((error) => {
                    fun.show(this, 'Произошла неизвестная ошибка');
                });
            // }
            // else{
            //     fun.show(this, 'Пожалуйста, подтвердите, что вы не робот');
            // }
        },

        recaptchaVerified(response) {
            this.recaptchaResponse = '';
        },
        recaptchaExpired() {
            this.$refs.vueRecaptcha.reset();
        },
        recaptchaFailed() {
            fun.show(this, "Произошла ошибка");
        },
        recaptchaError(reason) {
            fun.show(this, reason);
        },
    },
    mounted(){
        
    }
}
</script>

<style scoped>
.change_form{
    color: orange;
    cursor: pointer;
}
.change_form:hover{
    text-decoration: underline;
}
.bottom_texts_row{
    display: flex;
    flex-direction: row;
}
.title{
    color: #72949f;
}
.cross_icon{
    font-size: 1.7vw;
    cursor: pointer;
}
</style>