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

    const mountedRef = useRef(true);


    const stopPolling = () => {

        if (intervalRef.current) {

            clearInterval(
                intervalRef.current
            );

            intervalRef.current = null;

        }

    };


    useEffect(() => {

        mountedRef.current = true;

        return () => {

            mountedRef.current = false;

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


            if (!mountedRef.current) {

                return true;

            }


            const progress =
                Number.isFinite(
                    Number(job.progress)
                )
                    ? Number(job.progress)
                    : 0;


            setStatus(
                `${String(job.status || "unknown").toUpperCase()} (${progress}%)`
            );


            if (job.status === "completed") {

                stopPolling();

                setResult({

                    filename:
                        job.filename,

                    status:
                        job.status,

                });

                setLoading(false);

                setStatus(
                    "Analysis complete."
                );

                return true;

            }


            if (job.status === "failed") {

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

        catch (error) {

            console.error(
                "JOB STATUS ERROR:",
                error
            );


            if (!mountedRef.current) {

                return true;

            }


            stopPolling();

            setLoading(false);

            setError(

                error.response?.data?.error ||

                "Unable to check job status."

            );

            return true;

        }

    };


    const pollJobStatus = async (jobId) => {

        stopPolling();


        const finished =
            await checkJobStatus(
                jobId
            );


        if (finished) {

            return;

        }


        intervalRef.current =
            setInterval(
                async () => {

                    const done =
                        await checkJobStatus(
                            jobId
                        );

                    if (done) {

                        stopPolling();

                    }

                },
                3000
            );

    };


    const startProcessing = async (
        endpoint,
        options = {}
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

                    url: endpoint,

                    method:
                        options.method ||
                        "POST",

                    data:
                        options.data,

                    headers:
                        options.headers,

                });


            console.log(
                "PROCESS RESPONSE:",
                response.data
            );


            const jobId =
                response.data.job_id;


            if (!jobId) {

                throw new Error(
                    "No job id returned from server."
                );

            }


            setStatus(
                "Job queued..."
            );


            await pollJobStatus(
                jobId
            );

        }

        catch (error) {

            console.error(
                "PROCESSING ERROR:",
                error
            );


            if (!mountedRef.current) {

                return;

            }


            stopPolling();

            setLoading(false);

            setError(

                error.response?.data?.error ||

                error.message ||

                "Processing failed."

            );

        }

    };


    const handleUpload = async () => {

        if (!file) {

            setError(
                "Please select a .log file."
            );

            return;

        }


        if (
            !file.name
                .toLowerCase()
                .endsWith(".log")
        ) {

            setError(
                "Please select a .log file."
            );

            return;

        }


        console.log(
            "FILE SELECTED:",
            file.name,
            file.size,
            "bytes"
        );


        try {

            setLoading(true);

            setError("");

            setResult(null);

            setStatus(
                "Preparing upload..."
            );


            /*
             * STEP 1
             *
             * Ask Flask for a temporary R2
             * presigned upload URL.
             *
             * Only small JSON metadata is sent
             * to the backend here.
             */

            const urlResponse =
                await api.post(
                    "/logs/upload-url",
                    {
                        filename:
                            file.name,

                        content_type:
                            file.type ||
                            "application/octet-stream",
                    }
                );


            const uploadUrl =
                urlResponse.data.upload_url;

            const objectName =
                urlResponse.data.object_name;


            if (
                !uploadUrl ||
                !objectName
            ) {

                throw new Error(
                    "Server did not return a valid upload URL."
                );

            }


            console.log(
                "R2 OBJECT:",
                objectName
            );


            /*
             * STEP 2
             *
             * Upload the actual log file directly
             * from the browser to Cloudflare R2.
             *
             * The log file does NOT pass through Flask.
             */

            setStatus(
                "Uploading log file..."
            );


            const uploadResponse =
                await fetch(
                    uploadUrl,
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                file.type ||
                                "application/octet-stream",
                        },

                        body: file,
                    }
                );


            if (!uploadResponse.ok) {

                let details = "";


                try {

                    details =
                        await uploadResponse.text();

                }

                catch {

                    // Ignore response parsing errors.

                }


                console.error(
                    "R2 UPLOAD FAILED:",
                    uploadResponse.status,
                    details
                );


                throw new Error(
                    `File upload failed (${uploadResponse.status}).`
                );

            }


            console.log(
                "R2 UPLOAD COMPLETE"
            );


            /*
             * STEP 3
             *
             * Tell Flask that the R2 object is ready
             * for processing.
             */

            setStatus(
                "Starting analysis..."
            );


            await startProcessing(
                "/logs/process",
                {
                    method: "POST",

                    data: {
                        object_name:
                            objectName,

                        filename:
                            file.name,
                    },
                }
            );

        }

        catch (error) {

            console.error(
                "UPLOAD ERROR:",
                error
            );


            if (!mountedRef.current) {

                return;

            }


            stopPolling();

            setLoading(false);

            setError(

                error.response?.data?.error ||

                error.message ||

                "Upload failed."

            );

        }

    };


    const handleDemoLoad = async () => {

        await startProcessing(

            "/logs/demo",

            {
                method: "GET",
            }

        );

    };


    const handleFileChange = (event) => {

        const selectedFile =
            event.target.files?.[0] || null;


        stopPolling();

        setFile(
            selectedFile
        );

        setError("");

        setResult(null);

        setStatus("");

    };


    const handleViewDashboard = () => {

        stopPolling();

        if (onComplete) {

            onComplete();

        }

    };


    return (

        <div className="upload-box">


            <UploadCloud size={48} />


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
                        handleFileChange
                    }

                    disabled={
                        loading
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

                onClick={
                    handleUpload
                }

                disabled={
                    loading ||
                    !file
                }

            >

                {
                    loading
                        ? "Processing..."
                        : "Upload & Analyze"
                }

            </button>


            <button

                onClick={
                    handleDemoLoad
                }

                disabled={
                    loading
                }

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

                    <CheckCircle size={20} />

                    <div>

                        <strong>
                            Analysis Complete
                        </strong>


                        <p>
                            File: {result.filename}
                        </p>


                        <button
                            onClick={
                                handleViewDashboard
                            }
                        >
                            View Dashboard
                        </button>

                    </div>

                </div>

            }


            {
                error &&

                <div className="upload-result error">

                    <AlertCircle size={20} />

                    <span>
                        {error}
                    </span>

                </div>

            }

        </div>

    );

}


export default UploadBox;