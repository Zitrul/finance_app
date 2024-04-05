const express = require('express');
const router = express.Router();


const db = require("../models");
const mid = require("../middlewares");
const charts = require("../functions/charts.js");

router.post("/bar-chart", mid.authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await charts.transactionsByPeriod(period, user_id);
    const amounts = charts.categoriesAmounts(transactions);

    let top6categories = charts.top6Categories(amounts);

    res.json(top6categories);
});

router.post("/pie-chart", mid.authenticate, async (req, res) => {
    //! same as /categories-amounts
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await charts.transactionsByPeriod(period, user_id);
    const amounts = charts.categoriesAmounts(transactions);

    res.json(amounts);
});

router.post("/line-chart", mid.authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await charts.spendingsByPeriod(period, user_id);

    res.json(transactions);
});

module.exports = router;