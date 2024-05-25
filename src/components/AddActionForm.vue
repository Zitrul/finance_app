<template>
    <v-container class="d-flex flex-column align-center pa-10 bg-surface rounded-xl" :style="`width: ${xs ? '90vw' : '500px'};`">
        <v-container class="d-flex flex-row align-center justify-space-between pa-0" fluid>
            <p class="text-h5 mr-5">Добавление акций</p>
            <font-awesome-icon :icon="['fas', 'xmark']" @click="close_form()" class="text-h4 cursor-pointer"/>
        </v-container>
        
        <v-form ref="form" class="mt-8" style="width: 100%;">
            <v-autocomplete
                ref="ticker"
                v-model="ticker"
                :items="tickers"
                :rules="[() => !!ticker || 'Заполните это поле']"
                label="Тикер"
                placeholder="Поиск..."
                required
            ></v-autocomplete>
                
            <v-text-field
                v-model="amount"
                :rules="amountRules"
                type="number"
                label="Количество"
                required
            ></v-text-field>

            <v-checkbox
            label="Я хочу получать уведомления о новостях эмитентов этой акции"
            color="primary"
            v-model="notifications"
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
    </v-container>
    
</template>


<script>
import * as fun from '@/functions.js'
import { useDisplay } from 'vuetify'

export default {
    name: 'AddActionForm',
    data(){
        return {
            ticker: "",
            amount: 1,
            notifications: false,
            loading: false,
            amountRules: [
                v => !!v || 'Заполните поле',
                v => (v && parseInt(v) >= 1) || 'Укажите коррекное число',
            ],
            tickers: ['ABIO', 'ABRD', 'AFKS', 'AGRO', 'AKGD', 'AKMB', 'AKME', 'AKMM', 'AKQU', 'AKRN', 'AKUP', 'ALRS', 'AMEZ', 'AMNR', 'AMRB', 'AMRE', 'AMRH', 'APTK', 'AQUA', 'ARSA', 'ASSB', 'ASTR', 'BANE', 'BANEP', 'BCSB', 'BELU', 'BISVP', 'BOND', 'BRZL', 'BSPB', 'BSPBP', 'CARM', 'CBOM', 'CHGZ', 'CHKZ', 'CHMF', 'CHMK', 'CIAN', 'CNTL', 'CNTLP', 'CNYM', 'DELI', 'DIAS', 'DIOD', 'DIVD', 'DSKY', 'DVEC', 'DZRD', 'DZRDP', 'EELT', 'ELFV', 'ELTZ', 'ENPG', 'EQMX', 'ESGE', 'ESGR', 'ETLN', 'EUTR', 'FEES', 'FESH', 'FIVE', 'FIXP', 'FLOT', 'GAZA', 'GAZAP', 'GAZC', 'GAZP', 'GAZS', 'GAZT', 'GCHE', 'GECO', 'GEMA', 'GEMC', 'GLTR', 'GMKN', 'GOLD', 'GPBM', 'GPBR', 'GPBS', 'GROD', 'GTRK', 'HHRU', 'HIMCP', 'HNFG', 'HYDR', 'IGST', 'IGSTP', 'INFL', 'INGO', 'INGR', 'IRAO', 'IRKT', 'JNOS', 'JNOSP', 'KAZT', 'KAZTP', 'KBSB', 'KCHE', 'KCHEP', 'KGKC', 'KGKCP', 'KLSB', 'KLVZ', 'KMAZ', 'KMEZ', 'KOGK', 'KRKN', 'KRKNP', 'KRKOP', 'KROT', 'KROTP', 'KRSB', 'KRSBP', 'KUBE', 'KUZB', 'LEAS', 'LENT', 'LIFE', 'LNZL', 'LNZLP', 'LPSB', 'LQDT', 'LSNG', 'LSNGP', 'LSRG', 'MAGE', 'MAGEP', 'MAGN', 'MDMG', 'MFGS', 'MFGSP', 'MGKL', 'MGNT', 'MGNZ', 'MGTS', 'MGTSP', 'MISB', 'MISBP', 'MKBD', 'MOEX', 'MRKC', 'MRKP', 'MRKS', 'MRKU', 'MRKV', 'MRKY', 'MRKZ', 'MRSB', 'MSNG', 'MSRS', 'MSTT', 'MTEK', 'MTLR', 'MTLRP', 'MVID', 'NFAZ', 'NKHP', 'NKNC', 'NKNCP', 'NKSH', 'NLMK', 'NMTP', 'NNSB', 'NNSBP', 'NSVZ', 'NVTK', 'OBLG', 'OGKB', 'OKEY', 'OMZZP', 'OPNB', 'OPNR', 'OZON', 'PAZA', 'PHOR', 'PIKK', 'PLZL', 'PMSB', 'PMSBP', 'POLY', 'POSI', 'PRFN', 'PRIE', 'PRMB', 'RASP', 'RBCM', 'RCGL', 'RCHY', 'RCMB', 'RCMX', 'RDRB', 'RENI', 'RGSS', 'RKKE', 'RNFT', 'ROLO', 'ROSB', 'ROSN', 'ROST', 'RSHU', 'RTGZ', 'RTKM', 'RTKMP', 'RTSB', 'RTSBP', 'RUAL', 'RUSI', 'RZSB', 'SARE', 'SAREP', 'SBBY', 'SBCB', 'SBCN', 'SBCS', 'SBDS', 'SBER', 'SBERP', 'SBFR', 'SBGB', 'SBGD', 'SBHI', 'SBLB', 'SBMM', 'SBMX', 'SBPS', 'SBRB', 'SBRI', 'SBRS', 'SBSC', 'SBWS', 'SCFT', 'SELG', 'SFIN', 'SGZH', 'SIBN', 'SLEN', 'SMLT', 'SNGS', 'SNGSP', 'SOFL', 'SPBE', 'STSB', 'STSBP', 'SUGB', 'SVAV', 'SVCB', 'SVET', 'TASB', 'TASBP', 'TBEU', 'TBIO', 'TBRU', 'TBUY', 'TCBR', 'TCSG', 'TDIV', 'TECH', 'TEMS', 'TEUR', 'TEUS', 'TFNX', 'TGKA', 'TGKB', 'TGKBP', 'TGLD', 'TGRN', 'TIPO', 'TLCB', 'TMON', 'TMOS', 'TNSE', 'TORS', 'TORSP', 'TPAS', 'TRAI', 'TRMK', 'TRNFP', 'TRUR', 'TSOX', 'TSPX', 'TSST', 'TTLK', 'TUSD', 'TUZA', 'UGLD', 'UKUZ', 'UNAC', 'UNKL', 'UPRO', 'URKZ', 'USBN', 'UTAR', 'UWGN', 'VGSB', 'VGSBP', 'VJGZ', 'VJGZP', 'VKCO', 'VRSB', 'VRSBP', 'VSMO', 'VSYD', 'VSYDP', 'VTBR', 'WTCM', 'WTCMP', 'WUSH', 'YAKG', 'YKEN', 'YKENP', 'YNDX', 'YRSB', 'YRSBP', 'YUAN', 'ZAYM', 'ZILL'],

        }
    },
    methods: {
        close_form(){
            this.$emit('closed');
        },
        add(){
            this.loading = true;
            this.axios({
                method: 'post',
                url: `${fun.SERVER_URL}/stocks/add-stocks`,
                data: {
                    stock_quote: this.ticker,
                    asset_amount: this.amount,
                    news_subscription: this.notifications,
                }
            }).then((response) => {
                this.loading = false;
                fun.show(this, "Акции успешно добавлены в портфель", true);
                this.close_form();
            }).catch((e) => {
                this.loading = false;
                fun.show(this, "Ошибка при добавлении акций", false);
                console.log(e);
            });
        },
    },
}
</script>

<style scoped>
</style>