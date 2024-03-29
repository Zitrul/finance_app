<template>
    <v-container class="d-flex flex-column align-center pa-10 bg-surface rounded-xl">
        <v-container class="d-flex flex-row align-center justify-space-between pa-0" fluid>
            <p class="text-h5">{{edit_mode ? 'Редактировать' : 'Занесение трат'}}</p>
            <font-awesome-icon :icon="['fas', 'xmark']" @click="close_form()" class="text-h4 cursor-pointer"/>
        </v-container>
        
        <v-form ref="form" class="mt-8">
            <v-text-field
                v-model="name"
                :rules="nameRules"
                label="Наименование"
                required
            ></v-text-field>

            <v-select
                v-model="category_selected"
                :items="categories"
                :rules="[v => !!v || 'Необходимо выбрать категорию']"
                label="Категория"
                required
            ></v-select>
            <v-text-field
                v-if="category_selected == categories[0]"
                v-model="other_category"
                :rules="nameRules"
                label="Ваша категория"
                required
            ></v-text-field>
            
            <v-text-field
                v-model="price"
                :rules="priceRules"
                type="number"
                label="Стоимость"
                prefix="₽"
                required
            ></v-text-field>

            <v-checkbox
                v-model="checkbox"
                :rules="[v => !!v || 'У тебя нет выбора, чушпан']"
                label="Вы предоставляете разрешение нам и нашим партнерам разглашать абсолютно любую информацию, которую вы указываете"
                color="primary"
                required
            ></v-checkbox>

            <v-btn
            class="mt-4"
            color="primary"
            block
            @click="add()"
            >
            {{edit_mode ? 'Изменить' : 'Добавить'}}
            </v-btn>
        </v-form>

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

        <!-- <v-dialog
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
        </v-dialog> -->
    </v-container>
    
</template>


<script>
import * as fun from '@/functions.js'
import { useDisplay } from 'vuetify'

export default {
    name: 'TransactionForm',
    props: {
        edit_mode: {
            type: Boolean,
            default: false
        },
        Ename: {
            type: String,
            default: ''
        },
        Eprice: {
            type: String,
            default: '100.00'
        },
        Ecategory_selected: {
            type: String,
            default: 'Своя категория'
        },
        Eid: {
            type: Number,
            default: 0
        },
    },
    data(){
        return {
            name: '',
            nameRules: [
                v => !!v || 'Заполните поле',
                v => (v && v.length <= 40) || 'Длина не должна превышать 40 символов',
            ],
            priceRules: [
                v => !!v || 'Заполните поле',
                v => (v && parseFloat(v) && parseFloat(v) >= 0.01) || 'Укажите коррекную стоимость в формате xxx.yy',
            ],
            category_selected: 'Своя категория',
            categories: [
                'Своя категория',
                'Мясная гастрономия', 'Сладости и десерты', 'Сыры', 'Овощи и фрукты', 'Кулинария', 'Выпечка и хлеб',
                'Напитки', 'Замороженные полуфабрикаты', 'Товары для животных', 'Алкоголь', 'Косметика средства гигиены',
                'Молочные продукты', 'Мясо птица', 'Рыба и морепродукты', 'Детское питание', 'Техника', 'Ремонт',
                'Товары для дома', 'Авто', 'Канцтовары', 'Красота и здоровье', 'Досуг и хобби', 'Игрушки', 'Мебель',
                'Детская одежда и обувь', 'Хозтовары', 'Зоотовары', 'Детям и мамам', 'Книги', 'Дача и сад'
            ],
            other_category: '',
            price: '100.00',
            checkbox: false,
            loading: false,
        }
    },
    methods: {
        close_form(){
            this.$emit('closed');
            console.log("closed");
        },
        async add() {
            const { valid } = await this.$refs.form.validate()

            if(valid){
                if(this.edit_mode){
                    this.loading = true;
                    this.axios({
                        method: 'post',
                        url: `${fun.SERVER_URL}/change-transaction?id=${encodeURIComponent(this.Eid)}`,
                        data: {
                            name: this.name,
                            category: this.category_selected == this.categories[0] ? this.other_category : this.category_selected,
                            currency: "RUB",
                            amount: this.price
                        }
                    }).then((response) => {
                        this.loading = false;
                        if(response.status == 200) {
                            fun.show('Успешно изменено');
                            this.close_form();
                        }
                        else{
                            fun.show('Произошла ошибка, попробуйте позже');
                        }
                    }).catch((error) => {
                        this.loading = false;
                        fun.show('Произошла ошибка, попробуйте позже');
                    });
                }
                else{
                    this.loading = true;
                    this.axios({
                        method: 'post',
                        url: `${fun.SERVER_URL}/add-transaction`,
                        data: {
                            name: this.name,
                            category: this.category_selected == this.categories[0] ? this.other_category : this.category_selected,
                            currency: "RUB",
                            amount: this.price
                        }
                    }).then((response) => {
                        this.loading = false;
                        if(response.status == 200) {
                            fun.show('Успешно добавлено');
                            this.close_form();
                        }
                        else{
                            fun.show('Произошла ошибка, попробуйте позже');
                        }
                    }).catch((error) => {
                        this.loading = false;
                        fun.show('Произошла ошибка, попробуйте позже');
                    });
                }
            }
        }
    },
    mounted(){
        console.log('mounted');
        if(this.edit_mode){
            console.log('edit mode');
            console.log(this.Ecategory_selected);
            this.name = this.Ename;
            this.price = this.Eprice;
            console.log(this.categories.filter(c => c != this.Ecategory_selected).length)
            console.log(this.categories.length)
            if(this.categories.filter(c => c != this.Ecategory_selected).length >= this.categories.length){
                this.other_category = this.Ecategory_selected;
            }
            else{
                this.category_selected = this.Ecategory_selected;
            }
        }
    },
    setup() {
    }
}
</script>

<style scoped>
</style>