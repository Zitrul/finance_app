require("dotenv").config();

const auth = require("./functions/auth.js");
const mid = require("./middlewares");
const express = require("express");
const fs = require("fs");
const path = require("path");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const db = require("./models");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const sequelize = require("sequelize");
const cors = require('cors');
const axios = require('axios');
// const adminAuthMiddleware = require("./middlewares/adminAuthMiddleware");
// const fun = require("./functions");

const app = express();
const port = process.env.PORT || 3000;

app.use(cors())
app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "dist")));

// app.get("*", (req, res) => {
//   res.sendFile(path.join(__dirname, "dist", "index.html"));
// });
function authenticate(req, res, next) {
    return mid.authenticate(req, res, next, db);
}

app.get("/", (req, res) => {
    res.send("123");
});

app.post("/register", async (req, res) => {
    try {
        const username = req.body.username;
        const email = req.body.email;
        const formPassword = req.body.password;
        await bcrypt.genSalt().then(async function (salt) { // hash password
            await bcrypt.hash(formPassword, salt).then(async function (hash) {
                const [user, created] = await db.User.findOrCreate({
                    where: {
                        [sequelize.Op.or]: [
                            { username: username }, // trying to find existing user
                            { email_auth: email }
                        ],
                    },
                    defaults: {
                        username: username,
                        email_auth: email,
                        password: hash.toString(),
                        telegram_bot_token: require("crypto")
                            .randomBytes(32)
                            .toString("hex"),
                    },
                });
                if (created) {
                    return res.status(200).json("success");
                } else {
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
        where: sequelize.or({ username: username }, { email_auth: username }),
    });

    if (
        userFound &&
        (await bcrypt.compare(req.body.password, userFound.password)) // comparing hashes of passwords
    ) {
        const accessToken = auth.generateAccessToken(user);
        const refreshToken = await auth.createRefreshToken(user, db);
        res.cookie("accessToken", accessToken);
        res.cookie("refreshToken", refreshToken);
        res.status(200).json({
            accessToken: accessToken,
            refreshToken: refreshToken,
        });
    } else {
        res.sendStatus(403);
    }
});

app.get("/token-test", authenticate, (req, res) => {
    res.status(200).json({
        msg: "Authenticated!",
    });
});

app.post("/add-transaction", authenticate, async (req, res) => {
    try {
        const user_id = req.user["id"];
        const name = req.body.name;
        const amount = parseFloat(req.body.amount);
        const category = req.body.category;
        const currency = req.body.currency;
        const transaction = await db.Transaction.create({
            user_id: user_id,
            name: name,
            amount: amount,
            category: category,
            currency: currency,
        });
        res.status(200).json("succeeded");
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

db.sequelize.sync().then((req) => {
    process.env.db = db;
    app.listen(port, () => {
        console.log(`Server listened on port http://localhost:${port}`);
    });
});
