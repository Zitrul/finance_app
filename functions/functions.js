const db = require("../models");
const sequelize = require("sequelize");

function periodToMiliseconds(period) {
    let miliseconds = 0; // how many miliseconds fit in this period
    if (period === "day") {
        miliseconds = 24 * 60 * 60 * 1000;
    } else if (period === "month") {
        miliseconds = 30 * 24 * 60 * 60 * 1000;
    } else if (period === "3 months") {
        miliseconds = 3 * 30 * 24 * 60 * 60 * 1000;
    } else if (period === "6 months") {
        miliseconds = 6 * 30 * 24 * 60 * 60 * 1000;
    } else if (period === "year") {
        miliseconds = 365 * 24 * 60 * 60 * 1000;
    } else if (period === "all") {
        miliseconds = new Date().getTime();
    }

    return miliseconds;
}

async function transactionsByPeriod(period) {
    let miliseconds = periodToMiliseconds(period); // how many miliseconds fit in this period

    const transactions = await db.Transaction.findAll({
        where: {
            created_at: {
                [sequelize.Op.lt]: new Date(),
                [sequelize.Op.gt]: new Date(new Date() - miliseconds),
            },
        },
    });

    return transactions.reverse();
}

function categoriesAmounts(transactions) {
    let result = {}; // how much money wasted on every category in exact period
    for (let i = 0; i < transactions.length; i++) {
        if (
            result[transactions[i].category] == null ||
            result[transactions[i].category] == undefined
        ) {
            result[transactions[i].category] = 0;
        }
        result[transactions[i].category] += transactions[i].amount;
    }

    return result;
}

function top6Categories(amounts) {
    const entries = Object.entries(amounts);
    entries.sort((a, b) => b[1] - a[1]);
    const sortedObject = Object.fromEntries(entries);
    const top6 = Object.keys(sortedObject)
        .slice(0, 6)
        .reduce((result, key) => {
            result[key] = sortedObject[key];

            return result;
        }, {});

    return top6;
}

module.exports = {
    transactionsByPeriod: transactionsByPeriod,
    categoriesAmounts: categoriesAmounts,
    top6Categories: top6Categories,
};
