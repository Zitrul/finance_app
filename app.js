require("dotenv").config();

const auth = require("./functions/auth.js");
const functions = require("./functions/functions.js");
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
const cors = require("cors");
const axios = require("axios");
const upload = require("express-fileupload");
const { periodToMiliseconds } = require("./functions/functions.js");
const yahooFinance = require("yahoo-finance2").default; // NOTE the .default

// const adminAuthMiddleware = require("./middlewares/adminAuthMiddleware");
// const fun = require("./functions");

const app = express();
const port = process.env.PORT || 3000;

// app.use(cors());
app.use(function (req, res, next) {
    // Enabling CORS
    res.header("Access-Control-Allow-Origin", "http://localhost:8080");
    res.header(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept, authorization, refreshToken"
    );
    res.header(
        "Access-Control-Allow-Methods",
        "GET, POST, PUT, DELETE, OPTIONS"
    );
    res.header("Access-Control-Allow-Credentials", true);
    next();
});

app.use(upload());
app.use(bodyParser.urlencoded({ extended: false }));
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
        await bcrypt.genSalt().then(async function (salt) {
            // hash password
            await bcrypt.hash(formPassword, salt).then(async function (hash) {
                const [user, created] = await db.User.findOrCreate({
                    where: {
                        [sequelize.Op.or]: [
                            { username: username }, // trying to find existing user
                            { email_auth: email },
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
        user: req.user,
    });
});

app.post("/add-transaction", authenticate, async (req, res) => {
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
            res.status(200).json("succeeded");
        } else {
            res.status(400).json("Указана неверная сумма");
        }
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
});

app.put("/change-transaction", async (req, res) => {
    try {
        const id = req.body.id;

        const transaction = await db.Transaction.findOne({
            where: { id: id },
        });

        transaction.name = req.body.name;
        transaction.amount = req.body.amount;
        transaction.category = req.body.category;
        transaction.currency = req.body.currency;

        transaction.save();

        res.status(200).json("success");
    } catch (err) {
        console.log(err);
        res.status(500).json("smth went wrong");
    }
    
});

app.post("/scan-qr", authenticate, async (req, res) => {
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
});

app.get("/check-api", (req, res) => {
    axios
        .get(`http://${process.env.API_IP}:3214/?name=a`)
        .then((response) => {
            res.json(response.data);
        })
        .catch((error) => {
            res.json("smth went wrong");
        });
});

app.post("/all-transactions", authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await functions.transactionsByPeriod(period, user_id);

    res.json(transactions);
});

app.post("/categories-amounts", authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await functions.transactionsByPeriod(period, user_id);

    let result = functions.categoriesAmounts(transactions);

    res.json(result);
});

app.post("/bar-chart", authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await functions.transactionsByPeriod(period, user_id);
    const amounts = functions.categoriesAmounts(transactions);

    let top6categories = functions.top6Categories(amounts);

    res.json(top6categories);
});

app.post("/pie-chart", authenticate, async (req, res) => {
    //! same as /categories-amounts
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await functions.transactionsByPeriod(period, user_id);
    const amounts = functions.categoriesAmounts(transactions);

    res.json(amounts);
});

app.post("/line-chart", authenticate, async (req, res) => {
    const period = req.body.period; // day | month | 3 months | 6 months | year | all
    const user_id = req.user["id"];
    const transactions = await functions.spendingsByPeriod(period, user_id);

    res.json(transactions);
});

app.post("/scan-detected-qr", authenticate, (req, res) => {
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

app.get("/all-news", authenticate, async (req, res) => {
    const user_id = req.user["id"];
    const news = await db.LatestNews.findAll();

    res.json(news);
});

app.post("/add-stocks", authenticate, async (req, res) => {
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
            stockFound.save();
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

app.get("/users-stocks", authenticate, async (req, res) => {
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

db.sequelize.sync().then((req) => {
    process.env.db = db;
    app.listen(port, () => {
        console.log(`Server listened on port http://localhost:${port}`);
    });
});
