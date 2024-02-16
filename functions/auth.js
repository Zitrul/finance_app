require("dotenv").config();

const jwt = require("jsonwebtoken");

function generateAccessToken(user) {
    return jwt.sign(user, process.env.ACCESS_TOKEN_SECRET, {
        expiresIn: "24h",
    });
}

async function createRefreshToken(user, db) {
    return await db.RefreshToken.create({
        token: jwt.sign(user, process.env.REFRESH_TOKEN_SECRET),
    });
}

module.exports = {
    generateAccessToken: generateAccessToken,
    createRefreshToken: createRefreshToken,
};
