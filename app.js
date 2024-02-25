require("dotenv").config();

const auth = require("./functions/auth.js");
const express = require("express");
const fs = require("fs");
const path = require("path");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const db = require("./models");
const bodyParser = require("body-parser");
const sequelize = require("sequelize");
// const adminAuthMiddleware = require("./middlewares/adminAuthMiddleware");
// const fun = require("./functions");

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "dist")));

// app.get("*", (req, res) => {
//   res.sendFile(path.join(__dirname, "dist", "index.html"));
// });

app.get("/", (req, res) => {
    res.send("123");
});

app.post("/register", async (req, res) => {
    try {
        const username = req.body.username;
        const email = req.body.email;
        const formPassword = req.body.password;
        await bcrypt.genSalt().then(async function (salt) {
            await bcrypt.hash(formPassword, salt).then(async function (hash) {
                const [user, created] = await db.User.findOrCreate({
                    where: {
                        [sequelize.Op.or]: [
                            { username: username },
                            { email_auth: email },
                            { telegram_bot_token: require('crypto').randomBytes(32).toString('hex') }
                        ],
                    },
                    defaults: {
                        username: username,
                        email_auth: email,
                        password: hash.toString(),
                        telegram_bot_token: require('crypto').randomBytes(32).toString('hex')
                    },
                });
                if (created) {
                    return res.status(200).json("success");
                }
                else {
                    return res.status(300).json("на чужое базаришься?");
                }
            });
        });
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});


app.post("/login", async (req, res) => {
    const username = req.body.username;
    const user = { username: username };

    const userFound = await db.User.findOne({
        where: sequelize.or({ username: username }, { email: username }),
    });

    if (
        userFound &&
        (await bcrypt.compare(req.body.password, userFound.password))
    ) {
        const accessToken = auth.generateAccessToken(user);
        const refreshToken = await auth.createRefreshToken(user, db);
        res.status(200).json({
            accessToken: accessToken,
            resfreshToken: refreshToken,
        });
    } else {
        res.status(403);
    }
});


app.post("/addTransaction", async (req, res) => {
    const description = req.body.description;
    const type = req.body.type;
    const amount = parseFloat(req.body.amount);
    const currency = req.body.currency;
    try {
        const transaction = await db.Transaction.findOrCreate({
            where: {
                [sequelize.Op.or]: [
                    { description: description },
                    { type: type },
                    { amount: amount },
                    { currency: currency }
                ],
            },
            defaults: {
                user_id: null,
                description: description,
                type: type,
                amount: amount,
                currency: currency
            },
        });
        res.json(transaction.rows[0]);
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

db.sequelize.sync().then((req) => {
    app.listen(port, () => {
        console.log(`Server listened on port http://localhost:${port}`);
    });
});
