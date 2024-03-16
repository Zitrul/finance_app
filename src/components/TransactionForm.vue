<template>
    <v-container class="d-flex flex-column align-center pa-10 bg-surface rounded-xl">
        <v-container class="d-flex flex-row align-center justify-space-between pa-0" fluid>
            <p class="text-h5">Занесение трат</p>
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
            Добавить
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
    data(){
        return {
            name: '',
            nameRules: [
                v => !!v || 'Заполните поле',
                v => (v && v.length <= 20) || 'Длина не должна превышать 20 символов',
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
        },
        async add() {
            const { valid } = await this.$refs.form.validate()

            if(valid){
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
                    console.log(response);
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
    },
    mounted(){
    },
    setup() {
    }
}
</script>

<style scoped>
</style>