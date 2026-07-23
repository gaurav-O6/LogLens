import axios from "axios";



const api = axios.create({

    baseURL: import.meta.env.VITE_API_URL,

    // Large log uploads need more time
    timeout: 300000,

});




api.interceptors.request.use(

    (config) => {


        console.log(

            "REQUEST:",

            config.method?.toUpperCase(),

            config.baseURL + config.url

        );


        if (config.data instanceof FormData) {


            console.log(
                "UPLOAD REQUEST DETECTED"
            );


        }



        return config;


    },



    (error) => {


        return Promise.reject(error);


    }

);






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


        console.error(
            "AXIOS ERROR"
        );



        if (error.response) {


            console.error(
                "STATUS:",
                error.response.status
            );


            console.error(
                "DATA:",
                error.response.data
            );


        }



        else if (error.request) {


            console.error(
                "NO RESPONSE RECEIVED"
            );


            console.error(
                "REQUEST:",
                error.request
            );


        }



        else {


            console.error(
                "MESSAGE:",
                error.message
            );


        }



        return Promise.reject(error);


    }


);



export default api;