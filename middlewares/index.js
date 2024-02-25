const fs = require('fs');
const path = require('path');

const middlewares = {};

fs.readdirSync(__dirname)
    .filter(file => file !== 'index.js') // Исключаем сам index.js
    .forEach(file => {
        const middlewareName = file.replace('.js', ''); // Получаем имя middleware из имени файла
        const middlewareModule = require(path.join(__dirname, file));
        middlewares[middlewareName] = middlewareModule.open;
    });

module.exports = middlewares;
