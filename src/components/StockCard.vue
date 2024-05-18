<template>
    <v-card>
        <v-card-title>{{ stock.name }}</v-card-title>
        <v-card-text>
            <div>Цена: {{ stock.price }}</div>
            <div>Изменение: {{ stock.change }}</div>
            <v-sparkline :model-value="stock.history" height="100"></v-sparkline>
        </v-card-text>
    </v-card>
</template>

<script>
export default {
    props: {
        stock: Object // Ожидаем получить данные об акции
    }
}
</script>