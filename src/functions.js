// import { useToast } from 'vue-toastification'
const { useToast } = require('vue-toastification');
const toast = useToast();

const SERVER_URL = "/api";

function get_cookie(obj, key){
    return obj.$cookies.get(key);
}

function show(obj, msg, status=false){
    if(status){
        toast.success(msg, {
            position: "top-right",
            timeout: 5000,
            closeOnClick: true,
            pauseOnFocusLoss: true,
            pauseOnHover: false,
            draggable: true,
            draggablePercent: 0.6,
            showCloseButtonOnHover: false,
            hideProgressBar: true,
            closeButton: "button",
            icon: true,
            rtl: false
        });
    }
    else{
        toast.error(msg, {
            position: "top-right",
            timeout: 5000,
            closeOnClick: true,
            pauseOnFocusLoss: true,
            pauseOnHover: false,
            draggable: true,
            draggablePercent: 0.6,
            showCloseButtonOnHover: false,
            hideProgressBar: true,
            closeButton: "button",
            icon: true,
            rtl: false
        });
    }
    // const message = document.createElement('div');
    // message.className = status ? 'message-success' : 'message-error';
    // message.textContent = msg;

    // document.body.appendChild(message);
    
    // setTimeout(() => {
    //     message.style.transform = 'translateX(-200px)';
    //     message.style.opacity = '1';
    // }, 20);
    
    // setTimeout(() => {
    //     message.style.opacity = '0';
    // }, 2000);
}

async function check_auth(obj){
    const axiosInstance = obj.axios;

    return axiosInstance({
        method: 'get',
        url: `${SERVER_URL}/token-test`,
    }).then((response) => {
        if(response.status === 200) {
            return true;
        } else {
            return false;
        }
    }).catch((error) => {
        return false;
    });
}

function format_current_date(dateString) {
    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear().toString().slice(-2);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');

    return `${day}.${month}.${year} ${hours}:${minutes}`;
}


module.exports = {
    SERVER_URL: SERVER_URL,
    get_cookie: get_cookie,
    show: show,
    check_auth: check_auth,
    format_current_date: format_current_date
}