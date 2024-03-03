require("dotenv").config();

const jwt = require("jsonwebtoken");

function generateAccessToken(user) {
    return jwt.sign({
        username: user.username,
        time: new Date().getTime(),
    }, process.env.ACCESS_TOKEN_SECRET, {
        expiresIn: "30m",
    });
}

async function createRefreshToken(user, db) {
    return (await db.RefreshToken.create({
        token: jwt.sign(user, process.env.REFRESH_TOKEN_SECRET),
        username: user.username
    })).token;
}

async function checkRefreshToken(username, refreshToken, db) {
    await db.User.findOne({
        where: {
            username: username,
        },
    });

    const token = await db.RefreshToken.findOne({
        where: {
            username: username,
            token: refreshToken
        },
    });
    console.log(token);
    return (token != null);
}

module.exports = {
    generateAccessToken: generateAccessToken,
    createRefreshToken: createRefreshToken,
    checkRefreshToken: checkRefreshToken
};
