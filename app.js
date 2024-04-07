require("dotenv").config();

const mid = require("./middlewares");
const express = require("express");
const fs = require("fs");
const path = require("path");
const db = require("./models");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const sequelize = require("sequelize");
const axios = require("axios");
const upload = require("express-fileupload");

const authenticationRoutes = require('./routes/authenticationRoutes.js');
const transactionRoutes = require('./routes/transactionRoutes.js');
const chartRoutes = require('./routes/chartRoutes.js');
const stocksRoutes = require('./routes/stocksRoutes.js');
const accountRoutes = require('./routes/accountRoutes.js');

const app = express();
const port = Number(process.env.PORT) || 3000;


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

// -------------------------------------------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------------------------------------------

// authentication routes
app.use('/api/authentication', authenticationRoutes);

// transaction routes
app.use('/api/transactions', transactionRoutes);

// chart routes
app.use('/api/charts', chartRoutes);

// stocks routes
app.use('/api/stocks', stocksRoutes);

// account routes
app.use('/api/account', accountRoutes);

app.get("/api/all-news", mid.authenticate, async (req, res) => {
    const user_id = req.user["id"];
    const news = await db.LatestNews.findAll();

    res.json(news);
});

app.get("/api/check-api", (req, res) => {
    axios
        .get(`http://${process.env.API_IP}:3214/?name=a`)
        .then((response) => {
            res.json(response.data);
        })
        .catch((error) => {
            res.json("smth went wrong");
        });
});

app.get("/api/token-test", mid.authenticate, (req, res) => {
    res.status(200).json({
        msg: "Authenticated!",
        user: req.user,
    });
});

// app.get("*", (req, res) => {
//   res.sendFile(path.join(__dirname, "dist", "index.html"));
// });

// -------------------------------------------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------------------------------------------


db.sequelize.sync().then((req) => {
    app.listen(port, () => {
        console.log(`Server listened on port http://localhost:${port}`);
    });
});
