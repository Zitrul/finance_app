<template>
    <ContentWrapper>
        <v-row >
            <v-col cols="1" v-if="lgAndUp">
            </v-col>

            <v-col :cols="mdAndDown ? 12 : 10">
                <v-row fluid class="d-flex flex-row justify-center flex-wrap">
                    <v-col cols="12">
                        <v-row class="d-flex flex-row justify-space-between align-center">
                            <p :class="{'text-h4': smAndUp, 'text-h5': xs, 'text-text_title': true}">Новости из мира финансов</p>
                            <v-spacer></v-spacer>
                            <v-text-field label="Поиск по компаниям" variant="underlined" prepend-icon="mdi-magnify" class="mr-5" v-model="search_field" @change="find_news()"></v-text-field>
                            <v-btn variant="outlined" :class="{'mt-2': xs}" @click="loading_content = true; fetch_news();">
                                <font-awesome-icon :icon="['fas', 'rotate-right']" />
                                <p class="pl-2">Обновить</p>
                            </v-btn>
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
                                    <p>{{ /*fun.format_current_date(val.created_at)*/val.created_at }}</p>
                                </div>
                            </v-list-item>
                        </v-list>
                        <div class="text-center">
                            <v-pagination
                            v-model="news_page"
                            fluid
                            :length="Math.floor(news.length / news_pro_page) + (news.length % news_pro_page == 0 ? 0 : 1)"
                            :total-visible="4"
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
import * as fun from "@/functions.js";

export default {
  name: "News",
  components: {
    UsualBar,
    ContentWrapper,
  },
  data() {
    return {
        news: [],
        searched_news: [],
        news_page: 1,
        news_pro_page: 10,
        loading_content: true,
        search_field: "",
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
                this.searched_news = response.data;
                this.loading_content = false;
            }
            else{
                fun.show('Произошла неизвестная ошибка');
            }
        }).catch((error) => {
            console.error(error);
            fun.show('Произошла неизвестная ошибка');
        });
    },
    find_news(){
        this.searched_news = this.news.filter((val) => {
            return val.company_name.toLowerCase().includes(this.search_field.toLowerCase());
        });
    }
  },
  computed: {
    current_news_list() {
        return this.searched_news.slice(this.news_pro_page * (this.news_page - 1), this.news_pro_page * (this.news_page));
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