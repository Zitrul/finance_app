const express = require("express");
const fs = require("fs");
const path = require("path");
// const db = require("./models");
const bodyParser = require("body-parser");
// const adminAuthMiddleware = require("./middlewares/adminAuthMiddleware");
// const fun = require("./functions");

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "dist")));

// app.get("*", (req, res) => {
//   res.sendFile(path.join(__dirname, "dist", "index.html"));
// });

app.get("/", (req, res) => {
    res.send("123");
})

// db.sequelize.sync().then((req) => {
app.listen(port, () => {
console.log(`Server listened on port http://localhost:${port}`);
});
// });
