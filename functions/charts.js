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

async function transactionsByPeriod(period, user_id) {
    let miliseconds = periodToMiliseconds(period); // how many miliseconds fit in this period

    const transactions = await db.Transaction.findAll({
        where: {
            created_at: {
                [sequelize.Op.lt]: new Date(),
                [sequelize.Op.gt]: new Date(new Date() - miliseconds),
            },
            user_id: user_id,
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

function rearrangeObject(obj) {
    const keys = Object.keys(obj);
    let mid = Math.floor(keys.length / 2);
    if (keys.length % 2 == 0) mid += 1;

    let newObj = {};

    // console.log(obj);
    for (let i = 0; i < mid - 1; i++) {
        if (i % 2 == 0) newObj[keys[mid + i - 1]] = obj[keys[mid + i - 1]];
        else newObj[keys[i]] = obj[keys[i]];
        // console.log(`first ${i}`);
    }
    // console.log(newObj);
    for (let i = mid - 1; i < keys.length; i++) {
        if (i % 2 == 1) newObj[keys[i - mid + 1]] = obj[keys[i - mid + 1]];
        else newObj[keys[i]] = obj[keys[i]];
        // console.log(`second ${i}; ${keys[i - mid + 1]}`);
    }
    // console.log(newObj);

    return newObj;
}

function top6Categories(amounts) {
    const entries = Object.entries(amounts);
    entries.sort((a, b) => b[1] - a[1]);
    const sortedObject = Object.fromEntries(entries);
    let top6 = Object.keys(sortedObject)
        .slice(0, 6)
        .reduce((result, key) => {
            result[key] = sortedObject[key];

            return result;
        }, {});

    // return rearrangeObject(top6);
    return top6;
}

async function spendingsByPeriod(period, user_id) {
    let spendings = {};
    if (period === "day") {
        for (let i = 2; i < 25; i += 2) {
            let name = defineName("hour", i);

            spendings[name] = await spendingsBy2Hours(i, user_id);
        }
    } else if (period === "month") {
        for (let i = 2; i < 31; i += 2) {
            let name = defineName("day", i);

            spendings[name] = await spendingsBy2Days(i, user_id);
        }
    } else if (period === "3 months") {
        for (let i = 1; i < 13; i++) {
            let name = defineName("week", i);

            spendings[name] = await spendingsByWeek(i, user_id);
        }
    } else if (period === "6 months") {
        for (let i = 2; i < 25; i += 2) {
            let name = defineName("2 weeks", i);

            spendings[name] = await spendingsBy2Weeks(i, user_id);
        }
    } else if (period === "year") {
        for (let i = 1; i < 13; i++) {
            let name = defineName("month", i);

            spendings[name] = await spendingsByMonth(i, user_id);
        }
    }

    return spendings;
}

function defineName(period, i) {
    let name = "";
    if (period === "hour") {
        if (i === 2) {
            name = "последниe 2 часа";
        } else if (i === 4 || i === 22 || i === 24) {
            name = `${i} часа назад`;
        } else if (i === 21) {
            name = `${i} час назад`;
        } else {
            name = `${i} часов назад`;
        }
    } else if (period === "day") {
        if (i === 2) {
            name = "последние 2 дня";
        } else if ((i >= 2 && i <= 4) || i === 22 || i === 24) {
            name = `${i} дня назад`;
        } else {
            name = `${i} дней назад`;
        }
    } else if (period === "week") {
        if (i === 1) {
            name = "последняя неделя";
        } else if (i >= 2 && i <= 4) {
            name = `${i} недели назад`;
        } else {
            name = `${i} недель назад`;
        }
    } else if (period === "2 weeks") {
        if (i === 2) {
            name = "последние 2 недели";
        } else if (i === 4 || i === 22 || i === 24) {
            name = `${i} недели назад`;
        } else {
            name = `${i} недель назад`;
        }
    } else if (period === "month") {
        if (i === 1) {
            name = "последний месяц";
        } else if (i >= 2 && i <= 4) {
            name = `${i} месяца назад`;
        } else {
            name = `${i} месяцев назад`;
        }
    }

    return name;
}

async function spendingsBy2Hours(hours_ago, user_id) {
    const hour = 60 * 60 * 1000;
    const miliseconds = hour * hours_ago; // how many miliseconds fit in this period

    const transactions = await db.Transaction.findAll({
        where: {
            created_at: {
                [sequelize.Op.lt]: new Date(
                    new Date() - miliseconds + 2 * hour
                ),
                [sequelize.Op.gt]: new Date(new Date() - miliseconds),
            },
            user_id: user_id,
        },
    });

    let spendings = 0;
    for (let i = 0; i < transactions.length; i++) {
        spendings += transactions[i]["amount"];
    }

    return spendings;
}

async function spendingsBy2Days(days_ago, user_id) {
    const day_in_ms = 24 * 60 * 60 * 1000;
    const miliseconds = day_in_ms * days_ago; // how many miliseconds fit in this period

    const transactions = await db.Transaction.findAll({
        where: {
            created_at: {
                [sequelize.Op.lt]: new Date(new Date() - miliseconds + 2 * day_in_ms),
                [sequelize.Op.gt]: new Date(new Date() - miliseconds),
            },
            user_id: user_id,
        },
    });

    let spendings = 0;
    for (let i = 0; i < transactions.length; i++) {
        console.log(transactions[i]["amount"])
        spendings += transactions[i]["amount"];
    }

    return spendings;
}

async function spendingsByWeek(weeks_ago, user_id) {
    const week_in_ms = 7 * 24 * 60 * 60 * 1000;
    const miliseconds = week_in_ms * weeks_ago; // how many miliseconds fit in this period

    const transactions = await db.Transaction.findAll({
        where: {
            created_at: {
                [sequelize.Op.lt]: new Date(new Date() - miliseconds + week_in_ms),
                [sequelize.Op.gt]: new Date(new Date() - miliseconds),
            },
            user_id: user_id,
        },
    });

    let spendings = 0;
    for (let i = 0; i < transactions.length; i++) {
        spendings += transactions[i]["amount"];
    }

    return spendings;
}

async function spendingsBy2Weeks(weeks_ago, user_id) {
    const week_in_ms = 7 * 24 * 60 * 60 * 1000;
    const miliseconds = week_in_ms * weeks_ago; // how many miliseconds fit in this period

    const transactions = await db.Transaction.findAll({
        where: {
            created_at: {
                [sequelize.Op.lt]: new Date(
                    new Date() - miliseconds + 2 * week_in_ms
                ),
                [sequelize.Op.gt]: new Date(new Date() - miliseconds),
            },
            user_id: user_id,
        },
    });

    let spendings = 0;
    for (let i = 0; i < transactions.length; i++) {
        spendings += transactions[i]["amount"];
    }

    return spendings;
}

async function spendingsByMonth(months_ago, user_id) {
    const month_in_ms = 30 * 24 * 60 * 60 * 1000;
    const miliseconds = month_in_ms * months_ago; // how many miliseconds fit in this period

    const transactions = await db.Transaction.findAll({
        where: {
            created_at: {
                [sequelize.Op.lt]: new Date(
                    new Date() - miliseconds + month_in_ms
                ),
                [sequelize.Op.gt]: new Date(new Date() - miliseconds),
            },
            user_id: user_id,
        },
    });

    let spendings = 0;
    for (let i = 0; i < transactions.length; i++) {
        spendings += transactions[i]["amount"];
    }

    return spendings;
}

module.exports = {
    transactionsByPeriod: transactionsByPeriod,
    categoriesAmounts: categoriesAmounts,
    top6Categories: top6Categories,
    spendingsByPeriod: spendingsByPeriod,
};
