<template>
    <!-- <v-app>
        <v-main> -->
        <v-container fluid fill-height v-if="signup_active">
            <v-row justify="center">
            <v-col></v-col>
            <v-col cols="12" sm="8" md="3">
                <v-card class="rounded-xl" color="#001a23">
                    <!-- <v-icon class="fa-solid fa-xmark"></v-icon> -->
                    <!-- <v-icon class="position-absolute top-0 start-0">mdi-close</v-icon> -->

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
                <fa :icon="['fas', 'xmark']" class="cross_icon"/>
            </v-col>
            </v-row>
        </v-container>
        <!-- </v-main>
    </v-app> -->
</template>
  
<script>
import * as fun from '@/functions.js'

export default {
    name: 'Sign',
    props: {
        place: Number,
        name: String,
        score: Number,
    },
    data() {
        return {
            signup_active: true,
        }
    },
    methods: {
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