<template>
    <v-app>

        <v-main>
            <v-container fluid :class="{'ml-16': lgAndUp, 'pl-8': lgAndUp, 'pl-6': lgAndDown, 'd-flex': true, 'justify-center': true}">
                <v-row>
                    <v-col cols="1" v-if="lgAndUp">
                    </v-col>

                    <v-col :cols="smAndDown ? 12 : 7">
                        <v-row>
                            <v-col cols="12">
                                <v-row>
                                    <p class="text-h4 text-text_title">Внести расходы</p>
                                </v-row>
                                <v-row fluid>
                                    <v-btn size="x-large" class="ma-3 ml-0" @click="scanner_opened = true">
                                        <v-icon icon="mdi-qrcode-scan"></v-icon>
                                        <p class="ml-2">По фото чека</p>
                                    </v-btn>
                                    <v-btn size="x-large" :class="{'ma-3' : smAndUp}" @click="transactin_form_opened = true">
                                        <v-icon icon="mdi-file-edit-outline"></v-icon>
                                        <p class="ml-2">Внести вручную</p>
                                    </v-btn>
                                </v-row>
                            </v-col>
                            <v-col>
                                
                            </v-col>
                        </v-row>
                        <div class="mt-3">
                            <v-row>
                                <p class="text-h4 text-text_title">Ваши траты</p>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <div class="mt-3"></div>
                                    <v-row>
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
                                        
                                        <div class="d-flex flex-row ma-0 ml-5">
                                            <v-btn variant="plain" @click="change_chart('line')" title="Линейный график"><font-awesome-icon :icon="['fas', 'chart-line']"/></v-btn>
                                            <v-btn variant="plain" @click="change_chart('pie')" title="График-пирог"><font-awesome-icon :icon="['fas', 'chart-pie']" /></v-btn>
                                            <v-btn variant="plain" @click="change_chart('bar')" title="Столбцовый график"><font-awesome-icon :icon="['fas', 'chart-simple']" /></v-btn>
                                        </div>
                                    </v-row>
                                    <v-row>
                                        <div class="chart_container mt-7">
                                            <canvas id="chart"></canvas>
                                        </div>
                                    </v-row>
                                </v-col>
                            </v-row>
                        </div>
                    </v-col>

                    <v-col :cols="smAndDown ? 12 : (lgAndUp ? 3 : 5)">
                        <v-card>
                            <p class="text-h4 text-text_title">Список транзакций</p>
                            <v-list>
                                <v-list-item
                                    v-for="val in current_transactions_list"
                                    :key="val.id"
                                    :subtitle="val.category"
                                    href="#"
                                    class="pa-2"
                                >
                                    <div class="d-flex flex-row justify-space-between">
                                        <p class="text-primary font-weight-medium">{{ val.amount }} ₽</p>
                                        <p class="font-weight-medium">{{ val.name }}</p>
                                        <p>{{ fun.format_current_date(val.created_at) }}</p>
                                    </div>
                                </v-list-item>
                            </v-list>
                            <div class="text-center">
                                <v-pagination
                                v-model="transaction_page"
                                fluid
                                :length="Math.floor(transactions.length / transactions_pro_page) + (transactions.length % transactions_pro_page == 0 ? 0 : 1)"
                                ></v-pagination>
                            </div>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
        
        <v-overlay v-model="scanner_opened" class="align-center justify-center">
            <QrScanner @closed="scanner_opened = false; change_period(period_selected);"></QrScanner>
        </v-overlay>
        <v-overlay v-model="transactin_form_opened" class="align-center justify-center ">
            <TransactionForm @closed="transactin_form_opened = false; change_period(period_selected);"></TransactionForm>
        </v-overlay>
    </v-app>
</template>

<script setup>
import { useDisplay } from 'vuetify'

// Destructure only the keys you want to use
const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
</script>

<script>
import Sign from "@/components/Sign.vue";
import UsualBar from '@/components/UsualBar.vue'
import QrScanner from '@/components/QrScanner.vue'
import TransactionForm from '@/components/TransactionForm.vue'
import * as fun from "@/functions.js";

import Chart from 'chart.js/auto'

export default {
  name: "Wallet",
  components: {
    Sign,
    UsualBar,
    QrScanner,
    TransactionForm,
  },
  data() {
    return {
      sign_form_opened: false,
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
      current_chart_variable: null,
      chart_last_update: new Date().getTime(),
      current_chart_type: "line",
      chart_colors: [
        'rgba(238, 112, 84, 0.7)',
        'rgba(255, 137, 109, 0.7)',
        'rgba(255, 162, 134, 0.7)',
        'rgba(255, 187, 159, 0.7)',
        'rgba(255, 212, 184, 0.7)',
        'rgba(255, 237, 209, 0.7)',
        'rgba(255, 255, 234, 0.7)'
        // 'rgba(213, 87, 59, 0.7)'
      ],
      scanner_opened: false,
      transactin_form_opened: false,
      transactions: [],
      transactions_pro_page: 8,
      transaction_page: 1,
    };
  },
  methods: {
    checkNumber(num) {
        if (num >= 1) {
            return num;
        } else {
            return 1;
        }
    },
    change_period(ind){
        this.period_selected = ind;

        if(document.getElementById('chart')){
            setTimeout(() => {
                if(this.current_chart_type == "pie") this.pie_chart();
                else if(this.current_chart_type == "bar") this.bar_chart();
                else if(this.current_chart_type == "line") this.line_chart();
                this.fetch_transactions();
            },
            this.checkNumber( 1000 - ( (new Date().getTime() - this.chart_last_update)) ) );
        }
    },
    change_chart(type){
        this.current_chart_type = type;
        this.change_period(this.period_selected);
    },
    fetch_transactions(){
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/all-transactions`,
            data: {
                period: this.periods[this.period_selected].code,
            }
        }).then(async (response) => {
            if(response.status == 200) {
                this.transactions = response.data;
            }
            else{
                fun.show('error');
            }
        }).catch((error) => {
            console.error(error);
            fun.show('error');
        });
    },
    async bar_chart(){
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/bar-chart`,
            data: {
                period: this.periods[this.period_selected].code,
            }
        }).then(async (response) => {
            if(response.status == 200) {
                const data = response.data;
                if (this.current_chart_variable != null) await this.current_chart_variable.destroy();
                
                try{
                    let colors = (() => {
                        let arrachik = [];
                        for(let i = 0; i < Object.keys(data).length; i++){
                            arrachik.push(this.chart_colors[i % this.chart_colors.length]);
                        }
                        return arrachik;
                    })();

                    this.current_chart_variable = new Chart(
                        document.getElementById('chart'),
                        {
                            type: 'bar',
                            data: {
                                labels: Object.keys(data),
                                datasets: [
                                    {
                                        // label: 'Денег потрачено',
                                        data: Object.values(data),
                                        
                                        backgroundColor: colors,
                                    }
                                ]
                            },
                            options: {
                                maintainAspectRatio: false,
                                responsive: true,
                                aspectRatio: 1, // Задайте соотношение сторон графика
                                plugins: {
                                    legend: {
                                        display: false,
                                        position: 'top'
                                    }
                                },
                                scales: {
                                    x: {
                                        display: true,
                                        title: {
                                            display: true,
                                            text: 'Категория'
                                        }
                                    },
                                    y: {
                                        display: true,
                                        title: {
                                            display: true,
                                            text: 'Денег потрачено'
                                        }
                                    }
                                }
                            }
                        }
                    );

                    this.chart_last_update = new Date().getTime();
                }
                catch (e) {
                    console.log(e);
                }
            }
            else{
                fun.show('error');
            }
        }).catch((error) => {
            console.error(error);
            fun.show('error');
        });
    },
    async pie_chart(){
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/pie-chart`,
            data: {
                period: this.periods[this.period_selected].code,
            }
        }).then(async (response) => {
            if(response.status == 200) {
                const data = response.data;
                if (this.current_chart_variable != null) await this.current_chart_variable.destroy();
                
                try{
                    let colors = (() => {
                        let arrachik = [];
                        for(let i = 0; i < Object.keys(data).length; i++){
                            arrachik.push(this.chart_colors[i % this.chart_colors.length]);
                        }
                        return arrachik;
                    })();
                    
                    this.current_chart_variable = new Chart(
                        document.getElementById('chart'),
                        {
                            type: 'doughnut',
                            data: {
                                labels: Object.keys(data),
                                datasets: [
                                    {
                                        // label: 'Денег потрачено',
                                        data: Object.values(data),
                                        
                                        backgroundColor: colors,
                                        hoverOffset: 0
                                    }
                                ]
                            },
                            options: {
                                maintainAspectRatio: false,
                                responsive: true,
                                aspectRatio: 1, // Задайте соотношение сторон графика
                            }
                        }
                    );

                    this.chart_last_update = new Date().getTime();
                }
                catch (e) {
                    console.log(e);
                }
            }
            else{
                fun.show('error');
            }
        }).catch((error) => {
            console.error(error);
            fun.show('error');
        });
    },
    async line_chart(){
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/line-chart`,
            data: {
                period: this.periods[this.period_selected].code,
            }
        }).then(async (response) => {
            if(response.status == 200) {
                const data = response.data;
                if (this.current_chart_variable != null) await this.current_chart_variable.destroy();
                
                try{
                    this.current_chart_variable = new Chart(
                        document.getElementById('chart'),
                        {
                            type: 'line',
                            data: {
                                labels: Object.keys(data),
                                datasets: [
                                    {
                                        // label: 'Денег потрачено',
                                        data: Object.values(data),
                                        fill: true,
                                        borderColor: 'rgb(238, 112, 84)',
                                        tension: 0.1
                                    }
                                ]
                            },
                            options: {
                                maintainAspectRatio: false,
                                responsive: true,
                                aspectRatio: 1, // Задайте соотношение сторон графика
                                plugins: {
                                    legend: {
                                        display: false,
                                        position: 'top'
                                    }
                                },
                            }
                        }
                    );

                    this.chart_last_update = new Date().getTime();
                }
                catch (e) {
                    console.log(e);
                }
            }
            else{
                fun.show('error');
            }
        }).catch((error) => {
            console.error(error);
            fun.show('error');
        });
    },
  },
  computed: {
    current_transactions_list() {
        return this.transactions.slice(this.transactions_pro_page * (this.transaction_page - 1), this.transactions_pro_page * (this.transaction_page));
    }
  },
  mounted() {
    fun.check_auth(this).then(response => {
      if(response){
        this.chart_last_update = new Date().getTime();
        if(this.current_chart_type == "pie") this.pie_chart();
        else if(this.current_chart_type == "bar") this.bar_chart();
        else if(this.current_chart_type == "line") this.line_chart();
        this.fetch_transactions();
      }
    })
  },
};
</script>

<style scoped>
.chart_container{
    position: relative;
    height: 40vh;
    width: 50vw;
}
@media (min-width: 1024px) {
    .chart_container {
        width: 55vw;
    }
}
@media (max-width: 1023px) {
    .chart_container {
        width: 95vw;
    }
}

</style>