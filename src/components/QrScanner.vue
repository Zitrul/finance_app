<template>
    <v-container class="d-flex flex-column align-center pa-10 bg-surface rounded-xl" style="max-height: 80vh; overflow-y: scroll;">
        <v-container class="d-flex flex-row align-center justify-space-between pa-0" fluid>
            <p class="text-h5">Сканирование QR-кода с чека</p>
            <font-awesome-icon :icon="['fas', 'xmark']" @click="close_form()" class="text-h4 cursor-pointer"/>
        </v-container>
        
        <div class="w-full mt-8">
            <qrcode-drop-zone
            @detect="onDetect"
            >
                <div class="flex items-center justify-center w-full">
                    <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-30 pa-4 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
                        <div class="flex flex-col items-center justify-center pt-2 pb-2">
                            <svg class="w-8 h-8 mb-1 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                            </svg>
                            <p class="mb-1 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Кликните для загрузки фото</span>{{ smAndDown ? "" : " или просто перетащите его сюда" }}</p>
                        </div>
                        
                        <qrcode-capture
                        @detect="onDetect"
                        id="dropzone-file" class="hidden"
                        />
                    </label>
                </div>
            </qrcode-drop-zone>
        </div>

        <p class="text-h4 mt-8 text-primary">или</p>

        <v-btn
        class="mt-8"
        size="large"
        v-if="!camera_enabled"
        @click="camera_enabled = true">
            <v-icon
            icon="mdi-camera-outline"
            start
            ></v-icon>
            Распознать камерой
        </v-btn>

        <div class="camera_container mt-8" v-if="camera_enabled">
            <qrcode-stream :track="paintBoundingBox" @detect="onDetect" @error="onError"></qrcode-stream>
        </div>

        <!-- <v-overlay
        :model-value="loading"
        class="align-center justify-center"
        >
            <v-progress-circular
                color="primary"
                size="64"
                indeterminate
            ></v-progress-circular>
        </v-overlay> -->

        <v-dialog
        v-model="loading"
        max-width="320"
        persistent
        >
        <v-list
            class="py-2"
            color="primary"
            elevation="12"
            rounded="lg"
        >
            <v-list-item
            prepend-icon="mdi-creation"
            title="Обрабатываем ваш QR"
            >
            <template v-slot:prepend>
                <div class="pe-4">
                <v-icon color="primary" size="x-large"></v-icon>
                </div>
            </template>

            <template v-slot:append>
                <v-progress-circular
                color="primary"
                indeterminate="disable-shrink"
                size="16"
                width="2"
                ></v-progress-circular>
            </template>
            </v-list-item>
        </v-list>
        </v-dialog>
    </v-container>
    
</template>

<script setup>
import { useDisplay } from 'vuetify'

// Destructure only the keys you want to use
const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
</script>

<script>
import * as fun from '@/functions.js'
import { useDisplay } from 'vuetify'
import '@/assets/tailwind.css'

export default {
    name: 'QrScanner',
    data(){
        return {
            result: "",
            error: this.$refs[''],
            camera_enabled: false,
            loading: false,
        }
    },
    methods: {
        close_form(){
            this.$emit('closed');
        },
        paintBoundingBox(detectedCodes, ctx) {
            const top_left = detectedCodes["topLeftCorner"];
            const top_right = detectedCodes["topRightCorner"];
            const bottom_left = detectedCodes["bottomLeftCorner"];
            const bottom_right = detectedCodes["bottomRightCorner"];

            // ctx.strokeStyle = 'green';
            // ctx.beginPath();
            // ctx.moveTo(top_left.x, top_left.y);
            ctx.lineWidth = 5;
            ctx.strokeStyle = '#d5573b';
            ctx.strokeRect(top_left.x, top_left.y, top_right.x - top_left.x, bottom_left.y - top_left.y);
        },
        onError(err) {
            this.error.value = `[${err.name}]: `

            if (err.name === 'NotAllowedError') {
                this.error.value += 'you need to grant camera access permission'
                getUserMedia({
                    video: true,
                    audio: false
                })
            } else if (err.name === 'NotFoundError') {
                this.error.value += 'no camera on this device'
            } else if (err.name === 'NotSupportedError') {
                this.error.value += 'secure context required (HTTPS, localhost)'
            } else if (err.name === 'NotReadableError') {
                this.error.value += 'is the camera already in use?'
            } else if (err.name === 'OverconstrainedError') {
                this.error.value += 'installed cameras are not suitable'
            } else if (err.name === 'StreamApiNotSupportedError') {
                this.error.value += 'Stream API is not supported in this browser'
            } else if (err.name === 'InsecureContextError') {
                this.error.value += 'Camera access is only permitted in secure context. Use HTTPS or localhost rather than HTTP.'
            } else {
                this.error.value += err.message
            }
        },
        onDetect(detectedCodesPromise) {
            detectedCodesPromise.then(detectedCodes => {
                this.result = detectedCodes["content"];
                this.sendQrResults(detectedCodes);
            }).catch(error => {
                console.error('Error while processing detected codes:', error);
            });
        },
        sendQrResults(detectedCodes){
            // setTimeout(() => { this.loading = true; }, 500);
            this.loading = true;
            this.axios({
                method: 'post',
                url: `${fun.SERVER_URL}/transactions/scan-detected-qr`,
                data: {
                    data: detectedCodes["content"],
                }
            }).then((response) => {
                console.log(response);
                this.loading = false;
                if(response.status == 200) {
                    fun.show(this, 'Успешно добавлено', true);
                    this.close_form();
                }
                else{
                    fun.show(this, 'Произошла неизвестная ошибка');
                }
            }).catch((error) => {
                this.loading = false;
                fun.show(this, 'Произошла неизвестная ошибка');
            });
        }
    },
    mounted(){
    },
    setup() {
    }
}
</script>

<style scoped>
.camera_container{
    position: relative;
    height: 50vh;
    width: 40vw;
}
.scrollable{
    overflow-y: scroll;
}
@media (min-width: 769px) and (max-width: 1024px) {
    .camera_container {
        height: 50vh;
        width: 70vw;
    }
}
@media (max-width: 768px) {
    .camera_container {
        height: 60vh;
        width: 90vw;
    }
}
</style>