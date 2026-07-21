import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:5000/api/v1",
    timeout: 60000,
});

api.interceptors.request.use((config) => {
    console.log("REQUEST");
    console.log(config.method?.toUpperCase(), config.baseURL + config.url);
    return config;
});

api.interceptors.response.use(
    (response) => {
        console.log("RESPONSE");
        console.log(response.status, response.config.url);
        console.log(response.data);
        return response;
    },
    (error) => {
        console.error("AXIOS ERROR");

        if (error.response) {
            console.error("Status:", error.response.status);
            console.error("Data:", error.response.data);
        } else if (error.request) {
            console.error("No response received");
            console.error(error.request);
        } else {
            console.error(error.message);
        }

        return Promise.reject(error);
    }
);

export default api;