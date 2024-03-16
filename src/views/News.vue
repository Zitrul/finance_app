<template>
    <v-app>
        <UsualBar>Последние новости</UsualBar>

        <v-main>
            <v-container fluid :class="{'ml-16': lgAndUp, 'pl-8': lgAndUp, 'pl-6': lgAndDown, 'd-flex': true, 'justify-center': true}">
                <v-row>
                    <v-col cols="1" v-if="lgAndUp">
                    </v-col>

                    <v-col :cols="smAndDown ? 12 : 10">
                        <v-row>
                            <v-col cols="12">
                                <v-row>
                                    <p class="text-h4 text-text_title">Новости из мира финансов</p>
                                </v-row>
                                <v-row fluid>

                                </v-row>
                            </v-col>
                            <v-col v-if="!loading_content">
                                <v-list class="ml-0">
                                    <v-list-item
                                        v-for="val in current_news_list"
                                        :key="val.id"
                                        :subtitle="val.company_name"
                                        :href="val.link"
                                        target="_blank"
                                        class="pa-2"
                                    >
                                        <div class="d-flex flex-row justify-space-between">
                                            <p class="font-weight-medium link">{{ val.description.split(' - ').length == 2 ? val.description.split(' - ')[1] : val.description }}</p>
                                            <p>{{ fun.format_current_date(val.created_at) }}</p>
                                        </div>
                                    </v-list-item>
                                </v-list>
                                <div class="text-center">
                                    <v-pagination
                                    v-model="news_page"
                                    fluid
                                    :length="Math.floor(news.length / news_pro_page) + (news.length % news_pro_page == 0 ? 0 : 1)"
                                    :total-visible="7"
                                    ></v-pagination>
                                </div>
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
            </v-container>
        </v-main>
    </v-app>
</template>

<script setup>
import { useDisplay } from 'vuetify'

// Destructure only the keys you want to use
const { xs, sm, smAndDown, smAndUp, md, mdAndDown, mdAndUp, lg, lgAndDown, lgAndUp, xl, xlAndDown, xlAndUp, xxl } = useDisplay();
</script>

<script>
import UsualBar from '@/components/UsualBar.vue'
import * as fun from "@/functions.js";

export default {
  name: "News",
  components: {
    UsualBar,
  },
  data() {
    return {
        news: [],
        news_page: 1,
        news_pro_page: 10,
        loading_content: true,
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
  },
  computed: {
    current_news_list() {
        return this.news.slice(this.news_pro_page * (this.news_page - 1), this.news_pro_page * (this.news_page));
    }
  },
  mounted() {
    fun.check_auth(this).then(response => {
      if(response){
        this.fetch_news();
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