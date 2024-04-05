const auth = require("../functions/auth.js");
const jwt = require("jsonwebtoken");
const db = require('../models');

function open(req, res, next) {
    const authHeader = req.headers["authorization"];
    const token = authHeader && authHeader.split(" ")[1];
    if (!token) {
        return res.sendStatus(401);
    }

    jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, async (err, user) => {
        if (err) {
            console.log("youuu");
            // Access token недействителен, проверяем наличие refresh token
            console.log(req.cookies)
            const refreshToken = req.cookies.refreshToken;
            if (!refreshToken) {
                return res.sendStatus(403); // Нет refresh token
            }

            // Проверяем действительность refresh token
            jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET, async (err, user) => {
                if (err || !(await auth.checkRefreshToken(user.username, refreshToken, db) ) ) {
                    return res.sendStatus(403); // Недействительный refresh token
                }
                // Генерируем новый access token и продолжаем выполнение запроса
                const newAccessToken = auth.generateAccessToken(user);
                req.user = await db.User.findOne({ where: { username: user.username } });
                res.cookie("accessToken", newAccessToken);
                next();
            });
        } else {
            // Access token действителен
            req.user = await db.User.findOne({ where: { username: user.username } });;
            next();
        }
    });
}

module.exports = {
    open: open,
};
