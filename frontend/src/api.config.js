import axios from "axios";

export const instance = axios.create({
    withCredentials: true,
    baseURL: "http://127.0.0.1:8000",
});


// создаем перехватчик запросов
instance.interceptors.request.use(
    (config) => {
        config.headers.Authorization = `Bearer ${localStorage.getItem("token")}`
        return config
    }
)


// создаем перехватчик ответов
instance.interceptors.response.use(
    // в случае валидного accessToken ничего не делаем:
    (config) => {
        return config;
    },
    // в случае просроченного accessToken пытаемся его обновить:
    async (error) => {
        const originalRequest = {...error.config};
        originalRequest._isRetry = true;
        throw error;
    }
);