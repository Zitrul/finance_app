const express = require("express");
const router = express.Router();

const db = require("../models");
const mid = require("../middlewares");
const axios = require("axios");

router.post("/add-stocks", mid.authenticate, async (req, res) => {
    const user_id = req.user["id"];
    const asset_amount = req.body.amount;
    const stock_quote = req.body.ticker;
    const news_subscription = req.body.news_sub || false;

    await axios
        .post(`http://${process.env.API_IP}:3214/add_user_assets`, null, {
            params: {
                user_id: user_id,
                asset_amount: asset_amount,
                stock_quote: stock_quote,
                news_subscription: news_subscription,
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

router.get("/stock-trend", async (req, res) => {
    const ticker = req.body.ticker;

    axios
        .get(`http://${process.env.API_IP}:3214/get_current_price_trend`, {
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

router.get("/users-stocks", mid.authenticate, async (req, res) => {
    try {
        const user_id = req.user["id"];

        const stocks = await db.UserAssets.findAll({
            where: {
                user_id: user_id,
            },
        });

        result = {};

        for (let i = 0; i < stocks.length; i++) {
            const ticker = stocks[i].stock_quote;

            await axios
                .get(
                    `http://${process.env.API_IP}:3214/get_current_price_trend`,
                    {
                        params: {
                            ticker: ticker,
                        },
                    }
                )
                .then((response) => {
                    result[ticker] = { trend: response.data.trend , trend_percent: 0, price: 0};
                })
                .catch((error) => {
                    console.error(error.response.data.detail);
                    res.status(500).json("smth went wrong");
                });

            await axios
                .get(`http://${process.env.API_IP}:3214/get_current_price`, {
                    params: {
                        ticker: ticker,
                    },
                })
                .then((response) => {
                    result[ticker].trend_percent = (result[ticker].trend / response.data.price * 100).toFixed(2);

                    result[ticker].price = response.data.price;
                })
                .catch((error) => {
                    console.error(error.response.data.detail);
                    res.status(500).json("smth went wrong");
                });
        }

        res.status(200).json(result);
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
    const month_ago = charts.formatDate(
        new Date(new Date() - 30 * 24 * 60 * 60 * 1000)
    );

    axios
        .get(`http://${process.env.API_IP}:3214/get_history`, {
            params: {
                ticker: ticker,
                date_from: month_ago,
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
