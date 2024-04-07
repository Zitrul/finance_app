const express = require("express");
const router = express.Router();

const db = require("../models");
const mid = require("../middlewares");
const auth = require("../functions/auth.js");
const bcrypt = require("bcrypt");
const sequelize = require("sequelize");

router.post("/register", async (req, res) => {
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
                        telegram_bot_token:
                            require("crypto").randomBytes(16).toString("hex") +
                            encodeURIComponent(
                                bcrypt
                                    .hashSync(username, bcrypt.genSaltSync()) // 16 random hex symbols + 16 symbols of hashed username
                                    .toString()
                            ).substring(0, 16),
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

router.post("/login", async (req, res) => {
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

module.exports = router;
