require("dotenv").config();

const jwt = require("jsonwebtoken");

function generateAccessToken(user) {
    return jwt.sign({
        id: user.id,
        time: new Date().getTime(),
    }, process.env.ACCESS_TOKEN_SECRET, {
        expiresIn: "24h",
    });
}

async function createRefreshToken(user, db) {
    return (await db.RefreshToken.create({
        token: jwt.sign({id: user.id}, process.env.REFRESH_TOKEN_SECRET),
        user_id: user.id
    })).token;
}

async function checkRefreshToken(id, refreshToken, db) {
    await db.User.findOne({
        where: {
            id: id,
        },
    });

    const token = await db.RefreshToken.findOne({
        where: {
            user_id: id,
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
