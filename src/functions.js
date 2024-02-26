SERVER_URL = "http://localhost:3000/";

function get_cookie(obj, key){
    return obj.$cookies.get(key);
}

module.exports = {
    SERVER_URL: SERVER_URL,
    get_cookie: get_cookie
}