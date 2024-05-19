const express = require("express");
const router = express.Router();

const db = require("../models");
const mid = require("../middlewares");
const bcrypt = require("bcrypt");

router.get("/account-info", mid.authenticate, async (req, res) => {
    try {
        const user = await db.User.findOne({
            where: {
                id: req.user["id"],
            },
        });

        let telegram_auth = user.telegram_bot_token;

        if (user.telegram_bot_token === "0") {
            // if "0" it means user is authenticated in tg
            telegram_auth = true;
        }

        let info = {
            username: user.username,
            first_name: user.first_name,
            last_name: user.last_name,
            telegram_auth: telegram_auth,
            email: user.email_auth,
        };

        res.status(200).json(info);
    } catch (err) {
        res.status(500).json("smth went wrong");
    }
});

router.put("/change-account-info", mid.authenticate, async (req, res) => {
    try {
        const user = await db.User.findOne({
            where: {
                id: req.user["id"],
            },
        });

        if (
            (await db.User.findOne({
                where: { username: req.body.username },
            })) &&
            user.username != req.body.username
        ) {
            res.status(400).json("username already taken");
        } else {
            user.username = req.body.username;
            user.first_name = req.body.first_name;
            user.last_name = req.body.last_name;
            user.email_auth = req.body.email;

            await user.save();

            res.status(200).json("success");
        }
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

router.post("/reset-telegram", mid.authenticate, async (req, res) => {
    try {
        const user = await db.User.findOne({
            where: {
                id: req.user["id"],
            },
        });

        if (user.telegram_bot_token != "0") {
            res.status(400).json("you are not authenticated");
        } else {
            user.telegram_bot_token =
                require("crypto").randomBytes(32).toString("hex")

            await user.save();

            res.status(200).json("success");
        }
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

module.exports = router;
