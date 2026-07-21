import { useEffect, useState } from "react";
import {
    Database,
    CheckCircle,
    Clock3,
    RefreshCw,
} from "lucide-react";

import api from "../api/client";
import "./Page.css";


function History() {

    const [jobs, setJobs] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    useEffect(() => {

        loadJobs();

    }, []);


    async function loadJobs() {

        try {

            setLoading(true);

            setError("");

            const response = await api.get("/jobs");

            setJobs(response.data);

        }
        catch (error) {

            console.error(error);

            setError("Failed to load job history.");

        }
        finally {

            setLoading(false);

        }

    }


    const formatDate = (date) => {

        if (!date) {

            return "-";

        }

        return new Date(date).toLocaleString();

    };


    const statusClass = (status) => {

        switch (status?.toLowerCase()) {

            case "completed":
                return "status-completed";

            case "processing":
                return "status-processing";

            case "queued":
                return "status-queued";

            case "failed":
                return "status-failed";

            default:
                return "";

        }

    };


    const completedJobs =
        jobs.filter(
            job => job.status?.toLowerCase() === "completed"
        ).length;


    const queuedJobs =
        jobs.filter(
            job => job.status?.toLowerCase() === "queued"
        ).length;


    const processingJobs =
        jobs.filter(
            job => job.status?.toLowerCase() === "processing"
        ).length;



    return (

        <div className="page">


            <div className="page-heading">

                <h1>
                    Analysis History
                </h1>

                <p>
                    Previous log processing jobs
                </p>

            </div>



            <div className="history-summary">


                <div className="stat-card">

                    <Database size={24} />

                    <div>

                        <h3>
                            Total Jobs
                        </h3>

                        <p>
                            {jobs.length}
                        </p>

                    </div>

                </div>



                <div className="stat-card">

                    <CheckCircle size={24} />

                    <div>

                        <h3>
                            Completed
                        </h3>

                        <p>
                            {completedJobs}
                        </p>

                    </div>

                </div>



                <div className="stat-card">

                    <Clock3 size={24} />

                    <div>

                        <h3>
                            Active
                        </h3>

                        <p>
                            {processingJobs + queuedJobs}
                        </p>

                    </div>

                </div>


            </div>




            <div className="history-table-card">



                <div className="history-header">


                    <div className="history-header-top">


                        <div>

                            <h2>
                                Job History
                            </h2>


                            <p>
                                Uploaded log processing jobs
                            </p>

                        </div>



                        <button

                            className="history-refresh-btn"

                            onClick={loadJobs}

                            title="Refresh job history"

                            disabled={loading}

                        >

                            <RefreshCw
                                size={17}
                                className={loading ? "spin" : ""}
                            />

                            Refresh

                        </button>


                    </div>


                </div>





                {
                    loading ?


                        <div className="empty-state">

                            Loading history...

                        </div>


                    :


                    error ?


                        <div className="empty-state">

                            {error}

                        </div>


                    :


                    jobs.length === 0 ?


                        <div className="empty-state">

                            No processing jobs found.

                        </div>


                    :


                    <div className="history-table-container">


                        <table className="history-table">


                            <thead>

                                <tr>

                                    <th>ID</th>

                                    <th>Filename</th>

                                    <th>Status</th>

                                    <th>Progress</th>

                                    <th>Created</th>

                                    <th>Started</th>

                                    <th>Completed</th>

                                </tr>

                            </thead>



                            <tbody>


                                {
                                    jobs.map(job => (


                                        <tr key={job.id}>


                                            <td>
                                                {job.id}
                                            </td>


                                            <td>
                                                {job.filename}
                                            </td>


                                            <td>


                                                <span
                                                    className={`status-badge ${statusClass(job.status)}`}
                                                >

                                                    {job.status}

                                                </span>


                                            </td>


                                            <td>
                                                {job.progress ?? 0}%
                                            </td>


                                            <td>
                                                {formatDate(job.created_at)}
                                            </td>


                                            <td>
                                                {formatDate(job.started_at)}
                                            </td>


                                            <td>
                                                {formatDate(job.completed_at)}
                                            </td>


                                        </tr>


                                    ))
                                }


                            </tbody>


                        </table>


                    </div>

                }


            </div>


        </div>

    );

}


export default History;