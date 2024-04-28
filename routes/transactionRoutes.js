const express = require("express");
const router = express.Router();

const db = require("../models");
const mid = require("../middlewares");
const charts = require("../functions/charts.js");
const axios = require("axios");

router.post("/add-transaction", mid.authenticate, async (req, res) => {
    try {
        const user_id = req.user["id"];
        const name = req.body.name;
        const amount = parseFloat(req.body.amount);
        const category = req.body.category;
        const currency = req.body.currency;
        if (amount >= 0.01) {
            await db.Transaction.create({
                user_id: user_id,
                name: name,
                amount: amount,
                category: category,
                currency: currency,
            });
            res.status(200).json("success");
        } else {
            res.status(400).json("Указана неверная сумма");
        }
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.put("/change-transaction", mid.authenticate, async (req, res) => {
    try {
        const id = req.query.id;

        const transaction = await db.Transaction.findOne({
            where: {
                id: id,
                user_id: req.user["id"],
            },
        });

        transaction.name = req.body.name;
        transaction.amount = req.body.amount;
        transaction.category = req.body.category;
        transaction.currency = req.body.currency;

        await transaction.save();

        res.status(200).json("success");
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.delete("/delete-transaction", mid.authenticate, async (req, res) => {
    try {
        const id = req.query.id;

        const transaction = await db.Transaction.findOne({
            where: {
                id: id,
                user_id: req.user["id"],
            },
        });

        transaction.destroy();
        res.status(200).json("success");
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

/* router.post("/scan-qr", mid.authenticate, async (req, res) => {
    try {
        const image = req.files.img;
        const buf = image.data;
        const base64Data = buf.toString("base64");
        const json = { data: base64Data };

        url = `http://${process.env.API_IP}:3214/check_bill`;

        const formData = new FormData();
        formData.append("base64_data", json.data);
        formData.append("user_id", req.user["id"].toString());
        formData.append("sort", "True");

        axios
            .post(url, formData, {
                headers: {
                    "Content-Type": `multipart/form-data`,
                },
            })
            .then((response) => {
                console.log("Данные:", response.data);
                res.send("Файл успешно загружен!");
            })
            .catch((error) => {
                console.error("Ошибка:", error);
                res.status(500).send("Ошибка загрузки файла! 2853");
            });
    } catch (err) {
        console.error(err);
    }
}); */

router.post("/scan-detected-qr", mid.authenticate, (req, res) => {
    axios
        .get(`http://${process.env.API_IP}:3214/get_qr_info`, {
            params: {
                user_id: req.user["id"],
                qr_data: req.body.data,
                auto_sort: true,
            },
        })
        .then((response) => {
            res.json(response.data);
        })
        .catch((error) => {
            console.error(error.response.data.detail);
            res.status(500).json("smth went wrong");
        });
});

router.post("/all-transactions", mid.authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await charts.transactionsByPeriod(period, user_id);

    res.json(transactions);
});

router.post("/categories-amounts", mid.authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await charts.transactionsByPeriod(period, user_id);

    let result = charts.categoriesAmounts(transactions);

    res.json(result);
});

router.post("/add-profit", mid.authenticate, async (req, res) => {
    try {
        const user_id = req.user["id"];
        const name = req.body.name;
        const amount = parseFloat(req.body.amount);
        const category = req.body.category;
        const currency = req.body.currency;
        if (amount >= 0.01) {
            await db.ProfitableTransaction.create({
                user_id: user_id,
                name: name,
                amount: amount,
                category: category,
                currency: currency,
            });
            res.status(200).json("success");
        } else {
            res.status(400).json("Указана неверная сумма");
        }
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.put("/change-profit", mid.authenticate, async (req, res) => {
    try {
        const id = req.query.id;

        const transaction = await db.ProfitableTransaction.findOne({
            where: {
                id: id,
                user_id: req.user["id"],
            },
        });

        transaction.name = req.body.name;
        transaction.amount = req.body.amount;
        transaction.category = req.body.category;
        transaction.currency = req.body.currency;

        await transaction.save();

        res.status(200).json("success");
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.delete("/delete-profit", mid.authenticate, async (req, res) => {
    try {
        const id = req.query.id;

        const transaction = await db.ProfitableTransaction.findOne({
            where: {
                id: id,
                user_id: req.user["id"],
            },
        });

        transaction.destroy();
        res.status(200).json("success");
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

module.exports = router;
