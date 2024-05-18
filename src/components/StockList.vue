<template>
    <v-data-table :headers="headers" :items="stocks">
        <template v-slot:item="{ item }">
            <StockCard :stock="item"></StockCard>
        </template>
    </v-data-table>
</template>
  
<script>
import StockCard from './StockCard'

export default {
    components: {
        StockCard // Подключаем наш компонент StockCard
    },
    data() {
        return {
            headers: [ // Заголовки таблицы
                { text: 'Название', value: 'name' },
                { text: 'Цена', value: 'price' },
                { text: 'Изменение', value: 'change' }
            ],
            stocks: [
                {
                    name: 'Apple',
                    price: 100,
                    change: 10,
                    history: [
                        1, 2, 3, 4, 100, 200
                    ],
                },
                {
                    name: 'Apple',
                    price: 100,
                    change: 10,
                    history: [
                        1, 2, 3, 4, 100, 200
                    ],
                },
                {
                    name: 'Apple',
                    price: 100,
                    change: 10,
                    history: [
                        1, 2, 3, 4, 100, 200
                    ],
                },
            ] //  данные о всех акциях
        }
    }
}
</script>