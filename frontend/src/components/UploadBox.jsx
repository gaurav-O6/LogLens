import { useState, useRef, useEffect } from "react";

import {
    UploadCloud,
    CheckCircle,
    AlertCircle,
} from "lucide-react";

import api from "../api/client";


function UploadBox({ onComplete }) {


    const [file, setFile] = useState(null);

    const [loading, setLoading] = useState(false);

    const [result, setResult] = useState(null);

    const [error, setError] = useState("");

    const [status, setStatus] = useState("");


    const intervalRef = useRef(null);



    const stopPolling = () => {

        if (intervalRef.current) {

            clearInterval(intervalRef.current);

            intervalRef.current = null;

        }

    };



    useEffect(() => {

        return () => {

            stopPolling();

        };

    }, []);





    const checkJobStatus = async (jobId) => {


        try {


            const response =
                await api.get(
                    `/jobs/${jobId}`
                );


            const job =
                response.data;


            console.log(
                "JOB STATUS:",
                job
            );


            setStatus(
                `${job.status.toUpperCase()} (${job.progress || 0}%)`
            );



            if(job.status === "completed") {


                stopPolling();


                setResult({

                    filename:
                        job.filename,

                    status:
                        job.status,

                });


                setLoading(false);



                if(onComplete){

                    onComplete();

                }


                return true;

            }





            if(job.status === "failed") {


                stopPolling();


                setLoading(false);


                setError(
                    job.error ||
                    "Processing failed."
                );


                return true;

            }


            return false;


        }


        catch(error){


            console.error(
                "JOB STATUS ERROR:",
                error
            );


            stopPolling();


            setLoading(false);


            setError(
                "Unable to check job status."
            );


            return true;

        }

    };







    const pollJobStatus = async (jobId) => {


        stopPolling();


        // immediate check

        const finished =
            await checkJobStatus(jobId);



        if(finished){

            return;

        }




        intervalRef.current =
            setInterval(
                async () => {


                    const done =
                        await checkJobStatus(jobId);



                    if(done){

                        stopPolling();

                    }


                },
                3000
            );

    };








    const startProcessing = async (
        endpoint,
        options={}
    ) => {


        try {


            setLoading(true);

            setError("");

            setResult(null);

            setStatus(
                "Starting processing..."
            );



            const response =
                await api.request({

                    url:endpoint,

                    method:
                        options.method ||
                        "POST",

                    data:
                        options.data,

                    headers:
                        options.headers,

                });



            console.log(
                "UPLOAD RESPONSE:",
                response.data
            );



            const jobId =
                response.data.job_id;



            if(!jobId){

                throw new Error(
                    "No job id returned from server"
                );

            }



            setStatus(
                "Job queued..."
            );


            pollJobStatus(jobId);



        }


        catch(error){


            console.error(
                "UPLOAD ERROR:",
                error
            );


            setLoading(false);


            setError(
                error.response?.data?.error ||
                error.message
            );


        }


    };








    const handleUpload = () => {


        if(!file){

            setError(
                "Please select a .log file"
            );

            return;

        }



        const formData =
            new FormData();



        formData.append(
            "file",
            file
        );



        startProcessing(
            "/logs/upload",
            {

                method:"POST",

                data:formData,

                headers:{
                    "Content-Type":
                        "multipart/form-data",
                },

            }
        );

    };







    const handleDemoLoad = () => {


        startProcessing(
            "/logs/demo",
            {
                method:"GET",
            }
        );

    };







    return (

        <div className="upload-box">


            <UploadCloud size={48}/>


            <h2>
                Upload Security Logs
            </h2>


            <p>
                Supports Apache / Nginx .log files
            </p>



            <label className="file-drop">


                <input

                    type="file"

                    accept=".log"

                    onChange={
                        (e)=>
                            setFile(
                                e.target.files[0]
                            )
                    }

                />


                <span>

                    {
                        file
                        ? file.name
                        : "Choose log file"
                    }

                </span>


            </label>




            <button
                onClick={handleUpload}
                disabled={loading}
            >

                {
                    loading
                    ? "Processing..."
                    : "Upload & Analyze"
                }

            </button>





            <button
                onClick={handleDemoLoad}
                disabled={loading}
            >

                {
                    loading
                    ? "Processing..."
                    : "Load Demo Log"
                }

            </button>






            {
                status &&

                <p>
                    {status}
                </p>

            }






            {
                result &&

                <div className="upload-result success">

                    <CheckCircle size={20}/>


                    <div>

                        <strong>
                            Analysis Complete
                        </strong>


                        <p>
                            File: {result.filename}
                        </p>


                        <button
                            onClick={onComplete}
                        >
                            View Dashboard
                        </button>


                    </div>


                </div>

            }







            {
                error &&

                <div className="upload-result error">

                    <AlertCircle size={20}/>


                    <span>
                        {error}
                    </span>


                </div>

            }



        </div>

    );

}


export default UploadBox;