import axios from 'axios';

if (process.env.NODE_ENV == 'development') {
    axios.defaults.baseURL = 'http://127.0.0.1:8000';
} else if (process.env.NODE_ENV == 'production') {
    axios.defaults.baseURL = 'https://nanshan520.com/';
}

export default axios;