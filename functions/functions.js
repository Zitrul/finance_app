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

module.exports = {
    periodToMiliseconds: periodToMiliseconds,
};