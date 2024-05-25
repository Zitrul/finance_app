<template>
    <ContentWrapper>
        <v-row cols="12">
            <v-col cols="1" v-if="lgAndUp">
            </v-col>

            <v-col :cols="mdAndDown ? 12 : 7">
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
                            
                            class="pa-2"
                        >
                            <div class="d-flex flex-row justify-space-between">
                                <p class="text-primary font-weight-medium">{{ val.amount }} ₽</p>
                                <p class="font-weight-medium">{{ val.name }}</p>
                                <p>{{ fun.format_current_date(val.created_at) }}</p>
                                <v-btn icon="mdi-pencil" density="comfortable" variant="text" @click="open_edit_form(val.id);"></v-btn>
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

        <v-row cols="12" class="mt-5">
            <v-col cols="1" v-if="lgAndUp">
            </v-col>

            <v-col :cols="mdAndDown ? 12 : 11">
                <v-row>
                    <v-col cols="12">
                        <v-row>
                            <p class="text-h4 text-text_title">Внести прибыль</p>
                        </v-row>
                        <v-row fluid>
                            <v-btn size="x-large" :class="{'ma-3' : smAndUp}" @click="income_transactin_form_opened = true">
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
                        <p class="text-h4 text-text_title">Ваши пополнения</p>
                    </v-row>
                    <v-row>
                        <v-col>
                            <div class="mt-3"></div>
                            <v-row>
                                <v-menu v-model="menu2Open">
                                    <template v-slot:activator="{ props }">
                                        <v-btn
                                        color="primary"
                                        v-bind="props"
                                        >
                                        {{ periods[period2_selected].title }} <font-awesome-icon :icon="['fas', menuOpen ? 'angle-up' : 'angle-down']" class="ml-2"/>
                                        </v-btn>
                                    </template>
                                    <v-list>
                                        <v-list-item
                                        v-for="(item, index) in periods"
                                        :key="index"
                                        :value="index"
                                        @click="this.period2_selected = index; fetch_transactions();"
                                        >
                                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                                        </v-list-item>
                                    </v-list>
                                </v-menu>
                            </v-row>
                            <v-row>
                                <div class="chart_container">
                                    <v-card>
                                        <v-list>
                                            <v-list-item
                                                v-for="val in current_profit_list"
                                                :key="val.id"
                                                :subtitle="val.category"
                                                
                                                class="pa-2"
                                            >
                                                <div class="d-flex flex-row justify-space-between">
                                                    <p class="text-primary font-weight-medium">{{ val.amount }} ₽</p>
                                                    <p class="font-weight-medium">{{ val.name }}</p>
                                                    <p>{{ fun.format_current_date(val.created_at) }}</p>

                                                    <v-btn icon="mdi-pencil" density="comfortable" variant="text"></v-btn>
                                                    <!-- @click="open_edit_form(val.id);" -->
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
                                </div>
                            </v-row>
                        </v-col>
                    </v-row>
                </div>
            </v-col>

            <!-- <v-col :cols="smAndDown ? 12 : (lgAndUp ? 3 : 5)">
                <v-card>
                    <p class="text-h4 text-text_title">Список получек</p>
                    <v-list>
                        <v-list-item
                            v-for="val in current_transactions_list"
                            :key="val.id"
                            :subtitle="val.category"
                            
                            class="pa-2"
                        >
                            <div class="d-flex flex-row justify-space-between">
                                <p class="text-primary font-weight-medium">{{ val.amount }} ₽</p>
                                <p class="font-weight-medium">{{ val.name }}</p>
                                <p>{{ fun.format_current_date(val.created_at) }}</p>
                                <v-btn icon="mdi-pencil" density="comfortable" variant="text" @click="open_edit_form(val.id);"></v-btn>
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
            </v-col> -->
        </v-row>

        <v-overlay v-model="scanner_opened" class="align-center justify-center">
            <QrScanner @closed="scanner_opened = false; change_period(period_selected);"></QrScanner>
        </v-overlay>

        <v-overlay v-model="transactin_form_opened" class="align-center justify-center">
            <TransactionForm @closed="transactin_form_opened = false; change_period(period_selected); fetch_transactions();"></TransactionForm>
        </v-overlay>
        <v-overlay v-model="edit_transaction_form_opened" class="align-center justify-center">
            <TransactionForm :edit_mode="true" :Ename="edit_form.name" :Eprice="edit_form.price" :Ecategory_selected="edit_form.category" :Eid="edit_form.id"
            @closed="edit_transaction_form_opened = false; change_period(period_selected); fetch_transactions();"></TransactionForm>
        </v-overlay>

        <v-overlay v-model="income_transactin_form_opened" class="align-center justify-center">
            <IncomeTransactionForm @closed="income_transactin_form_opened = false; change_period(period_selected);"></IncomeTransactionForm>
        </v-overlay>
        <v-overlay v-model="edit_income_transaction_form_opened" class="align-center justify-center">
            <IncomeTransactionForm :edit_mode="true" :Ename="income_edit_form.name" :Eprice="income_edit_form.price" :Ecategory_selected="income_edit_form.category" :Eid="income_edit_form.id"
            @closed="edit_income_transaction_form_opened = false; change_period(period_selected);"></IncomeTransactionForm>
        </v-overlay>
    </ContentWrapper>
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
import IncomeTransactionForm from '@/components/IncomeTransactionForm.vue'
import ContentWrapper from '@/components/ContentWrapper.vue'
import * as fun from "@/functions.js";

import Chart from 'chart.js/auto'

export default {
  name: "Wallet",
  components: {
    Sign,
    UsualBar,
    QrScanner,
    TransactionForm,
    IncomeTransactionForm,
    ContentWrapper
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
      period2_selected: 1,
      menuOpen: false,
      menu2Open: false,
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
      profits: [],
      profits_pro_page: 8,
      profits_page: 1,

      edit_form: {
        id: 0,
        name: '',
        price: '',
        category: '',
      },
      edit_transaction_form_opened: false,

      income_edit_form: {
        id: 0,
        name: '',
        price: '',
        category: '',
      },
      income_transactin_form_opened: false,
      edit_income_transaction_form_opened: false,
    };
  },
  methods: {
    open_edit_form(id){
        for(let i = 0; i < this.transactions.length; i++){
            if(this.transactions[i].id == id){
                this.edit_form.id = id;
                this.edit_form.name = this.transactions[i].name;
                this.edit_form.price = String(this.transactions[i].amount);
                this.edit_form.category = this.transactions[i].category;
            }
        }

        this.edit_transaction_form_opened = true;
    },
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
            url: `${fun.SERVER_URL}/transactions/all-transactions`,
            data: {
                period: this.periods[this.period_selected].code,
            }
        }).then(async (response) => {
            if(response.status == 200) {
                this.transactions = response.data;
            }
            else{
                fun.show(this, 'Произошла неизвестная ошибка');
            }
        }).catch((error) => {
            console.error(error);
            fun.show(this, 'Произошла неизвестная ошибка');
        });
        
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/transactions/all-profit`,
            data: {
                period: this.periods[this.period2_selected].code,
            }
        }).then(async (response) => {
            if(response.status == 200) {
                this.profits = response.data;
            }
            else{
                fun.show(this, 'Произошла неизвестная ошибка');
            }
        }).catch((error) => {
            console.error(error);
            fun.show(this, 'Произошла неизвестная ошибка');
        });
    },
    async bar_chart(){
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/charts/bar-chart`,
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
                fun.show(this, 'Произошла неизвестная ошибка');
            }
        }).catch((error) => {
            console.error(error);
            fun.show(this, 'Произошла неизвестная ошибка');
        });
    },
    async pie_chart(){
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/charts/pie-chart`,
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
                fun.show(this, 'Произошла неизвестная ошибка');
            }
        }).catch((error) => {
            console.error(error);
            fun.show(this, 'Произошла неизвестная ошибка');
        });
    },
    async line_chart(){
        this.axios({
            method: 'post',
            url: `${fun.SERVER_URL}/charts/line-chart`,
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
                                labels: Object.keys(data).reverse(),
                                datasets: [
                                    {
                                        // label: 'Денег потрачено',
                                        data: Object.values(data).reverse(),
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
                fun.show(this, 'Произошла неизвестная ошибка');
            }
        }).catch((error) => {
            console.error(error);
            fun.show(this, 'Произошла неизвестная ошибка');
        });
    },
  },
  computed: {
    current_transactions_list() {
        return this.transactions.slice(this.transactions_pro_page * (this.transaction_page - 1), this.transactions_pro_page * (this.transaction_page));
    },
    current_profit_list() {
        return this.profits.slice(this.transactions_pro_page * (this.profits_page - 1), this.profits_pro_page * (this.profits_page));
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