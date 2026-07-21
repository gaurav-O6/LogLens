import { useState } from "react";
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

    const pollJobStatus = async (jobId) => {

        const interval = setInterval(async () => {

            try {

                const response = await api.get(`/jobs/${jobId}`);

                const job = response.data;

                setStatus(`Status: ${job.status}`);

                if (job.status === "completed") {

                    clearInterval(interval);

                    setResult({
                        filename: job.filename,
                        status: job.status,
                    });

                    setLoading(false);

                    if (onComplete) {
                        onComplete();
                    }
                }

                if (job.status === "failed") {

                    clearInterval(interval);

                    setLoading(false);

                    setError(job.error || "Processing failed.");
                }

            }
            catch (err) {

                console.error(err);

                clearInterval(interval);

                setLoading(false);

                setError("Failed checking job status.");
            }

        }, 2000);

    };

    const startProcessing = async (endpoint, options = {}) => {

        try {

            setLoading(true);
            setError("");
            setResult(null);
            setStatus("Uploading...");

            const response = await api.request({
                url: endpoint,
                method: options.method || "POST",
                data: options.data,
                headers: options.headers,
            });

            console.log("UPLOAD RESPONSE:", response.data);

            const jobId = response.data.job_id;

            setStatus("Job created. Processing...");

            pollJobStatus(jobId);

        }
        catch (err) {

            console.error("UPLOAD ERROR:", err);

            setLoading(false);

            if (err.response) {

                console.error(err.response.data);

                setError(JSON.stringify(err.response.data));

            }
            else {

                setError(err.message);

            }

        }

    };

    const handleUpload = () => {

        if (!file) {

            setError("Please select a .log file");
            return;

        }

        const formData = new FormData();

        formData.append("file", file);

        startProcessing("/logs/upload", {
            method: "POST",
            data: formData,
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });

    };

    const handleDemoLoad = () => {

        startProcessing("/logs/demo", {
            method: "GET",
        });

    };

    return (

        <div className="upload-box">

            <UploadCloud size={48} />

            <h2>Upload Security Logs</h2>

            <p>Supports Apache / Nginx .log files</p>

            <label className="file-drop">

                <input
                    type="file"
                    accept=".log"
                    onChange={(e) => setFile(e.target.files[0])}
                />

                <span>
                    {file ? file.name : "Choose log file"}
                </span>

            </label>

            <button
                onClick={handleUpload}
                disabled={loading}
            >
                {loading ? "Processing..." : "Upload & Analyze"}
            </button>

            <button
                onClick={handleDemoLoad}
                disabled={loading}
            >
                {loading ? "Processing..." : "Load Demo Log"}
            </button>

            {status && (
                <p>{status}</p>
            )}

            {result && (

                <div className="upload-result success">

                    <CheckCircle size={20} />

                    <div>

                        <strong>Analysis Complete</strong>

                        <p>
                            File: {result.filename}
                        </p>

                        <button onClick={onComplete}>
                            View Dashboard
                        </button>

                    </div>

                </div>

            )}

            {error && (

                <div className="upload-result error">

                    <AlertCircle size={20} />

                    <span>{error}</span>

                </div>

            )}

        </div>

    );

}

export default UploadBox;