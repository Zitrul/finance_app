const express = require('express');
const router = express.Router();


const db = require("../models");
const mid = require("../middlewares");
const axios = require("axios");
const yahooFinance = require("yahoo-finance2").default; // NOTE the .default

router.post("/add-stocks", mid.authenticate, async (req, res) => {
    try {
        const ticker = req.body.ticker;
        const amount = req.body.amount;
        const user_id = req.user["id"];
        const news_sub = req.body.news_sub;

        const stockFound = await db.UserAssets.findOne({
            where: sequelize.and({ user_id: user_id }, { stock_quote: ticker }),
        });

        if (stockFound) {
            stockFound.asset_amount += amount;
            await stockFound.save();
        } else {
            const stock_info = await yahooFinance.quote(ticker);
            const company_name = stock_info["shortName"];

            await db.UserAssets.create({
                user_id: user_id,
                company_name: company_name,
                asset_amount: amount,
                news_subscription: news_sub,
                stock_quote: ticker,
            });
        }

        res.status(200).json("succeeded");
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.get("/users-stocks", mid.authenticate, async (req, res) => {
    try {
        const user_id = req.user["id"];

        const stocks = await db.UserAssets.findAll({
            where: {
                user_id: user_id,
            },
        });

        res.status(200).json(stocks);
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.get("/stock-price", async (req, res) => {
    const ticker = req.body.ticker;

    axios
        .get(`http://${process.env.API_IP}:3214/get_current_price`, {
            params: {
                ticker: ticker,
            },
        })
        .then((response) => {
            res.status(200).json(response.data);
        })
        .catch((error) => {
            console.error(error.response.data.detail);
            res.status(500).json("smth went wrong");
        });
});

router.get("/stocks-shareholding", async (req, res) => {
    try {
        const shareholding = req.body.shareholding;
        let prices = {};

        for (stock in shareholding) {
            const ticker = stock;
            const amount = shareholding[stock];
            let price = 0;

            await axios
                .get(`http://${process.env.API_IP}:3214/get_current_price`, {
                    params: {
                        ticker: ticker,
                    },
                })
                .then((response) => {
                    price = response.data.price;
                })
                .catch((error) => {
                    console.error(error.response.data.detail);
                    res.status(500).json("smth went wrong");
                });

            prices[ticker] = amount * price;
        }

        res.status(200).json(prices);
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.get("/stock-chart", async (req, res) => {
    const ticker = req.body.ticker;
    const month_ago = charts.formatDate(new Date(new Date() - 30 * 24 * 60 * 60 * 1000));

    axios
        .get(`http://${process.env.API_IP}:3214/get_history`, {
            params: {
                ticker: ticker,
                date_from: month_ago
            },
        })
        .then((response) => {
            res.status(200).json(response.data);
        })
        .catch((error) => {
            console.error(error.response.data.detail);
            res.status(500).json("smth went wrong");
        });
});

module.exports = router;