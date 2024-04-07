<template>
    <ContentWrapper>
        <v-row>
            <v-col cols="1" v-if="lgAndUp">
            </v-col>

            <v-col :cols="mdAndDown ? 12 : 10">
                <v-row fluid class="d-flex flex-row justify-center flex-wrap">
                    <v-col cols="12">
                        <v-row class="d-flex flex-row justify-space-between align-center">
                            <p :class="{'text-h4': smAndUp, 'text-h5': xs, 'text-text_title': true}">Ваш портфель</p>
                            <v-menu v-model="menuOpen">
                                <template v-slot:activator="{ props }">
                                    <v-btn
                                    color="primary"
                                    v-bind="props"
                                    >
                                    {{ periods[period_selected].title }} <font-awesome-icon :icon="['fas', menuOpen ? 'angle-up' : 'angle-down']" class="ml-2"/>
                                    </v-btn>
                                </template>
                                <v-list>
                                    <v-list-item
                                    v-for="(item, index) in periods"
                                    :key="index"
                                    :value="index"
                                    @click="change_period(index)"
                                    >
                                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                                    </v-list-item>
                                </v-list>
                            </v-menu>
                        </v-row>
                        <v-row fluid>

                        </v-row>
                    </v-col>
                    <v-col v-if="!loading_content">
                        <v-row fluid>
                            <v-col>
                                <div class="text-center">
                                    <v-btn prepend-icon="mdi-plus" rounded="xl" @click="add_action_form_opened = true;">
                                        Добавить акции в портфель
                                    </v-btn>
                                </div>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="4">
                                <v-list>
                                    <v-list-item
                                        v-for="(el, i) in user_stocks"
                                        :key="i"
                                        :value="i"
                                    >
                                        <div class="d-flex flex-row justify-space-between">
                                            <p>{{ el.ticker }}</p>
                                            <p :class="{'text-red': el.difference < 0, 'text-green': el.difference >= 0}">
                                                <b>{{ (el.difference >= 0 ? '+ ' : '- ') + Math.abs(Number(el.difference)) + '%' }}</b> {{ '(' + el.difference_money + ' ₽)' }}
                                                <font-awesome-icon :icon="['fas', 'up-long']" v-if="el.difference >= 0"/>
                                                <font-awesome-icon :icon="['fas', 'down-long']" v-else/>
                                            </p>
                                        </div>
                                    </v-list-item>
                                </v-list>
                            </v-col>
                            <v-col cols="8">
                                <!-- <TradingVue :data="chart_data"></TradingVue> -->
                                <v-row class="d-flex flex-row justify-space-between" fluid>
                                    <v-btn variant="text" prepend-icon="mdi-trash-can-outline" >Удалить</v-btn>
                                    <v-btn class="bg-sell" rounded="lg">Продать</v-btn>
                                </v-row>
                            </v-col>
                        </v-row>
                        
                    </v-col>
                    <v-col class="d-flex flex-row justify-center align-center mt-16" v-if="loading_content" fluid>
                        <p>Получаем данные</p>
                        <v-progress-circular
                        class="ml-5"
                        :size="50"
                        color="primary"
                        indeterminate
                        ></v-progress-circular>
                    </v-col>
                </v-row>
            </v-col>

            <v-col cols="1" v-if="lgAndUp">
            </v-col>
        </v-row>

        <v-overlay v-model="add_action_form_opened" class="align-center justify-center">
            <AddActionForm @closed="add_action_form_opened = false; change_period(period_selected);"></AddActionForm>
        </v-overlay>
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
import AddActionForm from '@/components/AddActionForm.vue'
import * as fun from "@/functions.js";

import TradingVue from 'trading-vue-js'

export default {
  name: "Investing",
  components: {
    UsualBar,
    ContentWrapper,
    AddActionForm,
    TradingVue
  },
  data() {
    return {
        add_action_form_opened: false,
        loading_content: false,
        user_stocks: [
            {
                ticker: "PORN",
                price: 100.89,
                difference: -0.24,
                difference_money: 120.56,
            },
            {
                ticker: "XXX",
                price: 50.89,
                difference: 25,
                difference_money: 120.56,
            },
            {
                ticker: "S911",
                price: 100.89,
                difference: 4.56,
                difference_money: 120.56,
            },
            {
                ticker: "AMST",
                price: 100.89,
                difference: -0.5,
                difference_money: 120.56,
            },
            {
                ticker: "PLKA",
                price: 100.89,
                difference: -8,
                difference_money: 120.56,
            },
            {
                ticker: "YNDX",
                price: 100.89,
                difference: 12,
                difference_money: 120.56,
            },
        ],
        periods: [
            {
                title: "День",
                code: "day",
            },
            {
                title: "Месяц",
                code: "month",
            },
            {
                title: "3 месяца",
                code: "3 months",
            },
            {
                title: "6 месяцев",
                code: "6 months",
            },
            {
                title: "Год",
                code: "year",
            },
            {
                title: "Все время",
                code: "all",
            },
        ],
        period_selected: 1,
        menuOpen: false,

        chart_data: {
            ohlcv: [
                [ 1551128400000, 33,  37.1, 14,  14,  196 ],
                [ 1551132000000, 13.7, 30, 6.6,  30,  206 ],
                [ 1551135600000, 29.9, 33, 21.3, 21.8, 74 ],
                [ 1551139200000, 21.7, 25.9, 18, 24,  140 ],
                [ 1551142800000, 24.1, 24.1, 24, 24.1, 29 ],
            ]
        },
    };
  },
  methods: {
    fetch_news(){
        this.axios({
            method: 'get',
            url: `${fun.SERVER_URL}/all-news`,
        }).then((response) => {
            if(response.status == 200) {
                this.news = response.data;
                this.loading_content = false;
            }
            else{
                fun.show('error');
            }
        }).catch((error) => {
            console.error(error);
            fun.show('error');
        });
    },
    change_period(ind){
        this.period_selected = ind;
    },
  },
  computed: {
    current_news_list() {
        return this.news.slice(this.news_pro_page * (this.news_page - 1), this.news_pro_page * (this.news_page));
    }
  },
  mounted() {
    fun.check_auth(this).then(response => {
      if(response){
        //this.fetch_news();
      }
    })
  },
};
</script>

<style scoped>
.link:hover{
    text-decoration: underline;
}
</style>