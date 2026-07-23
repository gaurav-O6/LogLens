import axios from "axios";


const api = axios.create({

    baseURL: import.meta.env.VITE_API_URL,

    timeout: 60000,

});


api.interceptors.request.use((config) => {

    console.log(
        "REQUEST:",
        config.method?.toUpperCase(),
        config.baseURL + config.url
    );

    return config;

});


api.interceptors.response.use(

    (response) => {

        console.log(
            "RESPONSE:",
            response.status,
            response.config.url,
            response.data
        );

        return response;

    },


    (error) => {

        console.error("AXIOS ERROR");


        if (error.response) {

            console.error("Status:", error.response.status);

            console.error("Data:", error.response.data);

        } 
        
        else if (error.request) {

            console.error("No response received");

        } 
        
        else {

            console.error(error.message);

        }


        return Promise.reject(error);

    }

);


export default api;