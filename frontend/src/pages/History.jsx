
import {
    useEffect,
    useState,
    useRef
} from "react";

import {
    Database,
    CheckCircle,
    Clock3,
    RefreshCw,
    FileText,
    ExternalLink,
    Trash2,
    AlertTriangle,
} from "lucide-react";

import {
    useNavigate
} from "react-router-dom";

import api from "../api/client";

import "./Page.css";


function History() {


    const navigate = useNavigate();


    const [jobs, setJobs] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [refreshing, setRefreshing] = useState(false);

    const [clearingDatabase, setClearingDatabase] =
        useState(false);


    const jobsRef = useRef([]);


    /*
    ==========================================================
    LOAD JOBS + POLL ACTIVE JOBS
    ==========================================================
    */

    useEffect(() => {

        loadJobs();


        const interval = setInterval(() => {

            const activeJobs =
                jobsRef.current.some(
                    job =>
                        job.status === "queued" ||
                        job.status === "processing"
                );


            if (activeJobs) {

                loadJobs(false);

            }

        }, 5000);


        return () => {

            clearInterval(interval);

        };

    }, []);


    /*
    ==========================================================
    LOAD JOB HISTORY
    ==========================================================
    */

    async function loadJobs(showLoading = true) {

        try {

            if (showLoading) {

                setLoading(true);

            }

            else {

                setRefreshing(true);

            }


            setError("");


            const response =
                await api.get("/jobs");


            const data =
                Array.isArray(response.data)
                    ?
                    response.data
                    :
                    [];


            jobsRef.current = data;

            setJobs(data);

        }


        catch (error) {

            console.error(
                "HISTORY ERROR",
                error
            );


            setError(
                "Failed to load job history."
            );

        }


        finally {

            setLoading(false);

            setRefreshing(false);

        }

    }


    /*
    ==========================================================
    CLEAR DATABASE
    ==========================================================
    */

    async function clearDatabase() {

        if (clearingDatabase) {

            return;

        }


        const confirmed =
            window.confirm(
                "WARNING: This will permanently delete ALL log entries, detections, and job history.\n\nThis action cannot be undone.\n\nAre you sure you want to continue?"
            );


        if (!confirmed) {

            return;

        }


        const finalConfirmation =
            window.confirm(
                "Final confirmation:\n\nDelete the entire LogLens analysis database?"
            );


        if (!finalConfirmation) {

            return;

        }


        try {

            setClearingDatabase(true);

            setError("");


            await api.post(
                "/admin/reset-database"
            );


            jobsRef.current = [];

            setJobs([]);


            await loadJobs(false);

        }


        catch (error) {

            console.error(
                "DATABASE RESET ERROR",
                error
            );


            const message =
                error?.response?.data?.error ||
                error?.response?.data?.message ||
                "Failed to clear the database.";


            setError(message);

        }


        finally {

            setClearingDatabase(false);

        }

    }


    /*
    ==========================================================
    DATE FORMAT
    ==========================================================
    */

    const formatDate = (date) => {

        if (!date) {

            return "-";

        }


        return new Date(date)
            .toLocaleString();

    };


    /*
    ==========================================================
    STATUS CLASS
    ==========================================================
    */

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


    /*
    ==========================================================
    OPEN JOB ANALYSIS
    ==========================================================
    */

    const openAnalysis = (job) => {

        if (!job?.id) {

            return;

        }


        navigate(
            `/?job_id=${encodeURIComponent(job.id)}`
        );

    };


    /*
    ==========================================================
    SUMMARY COUNTS
    ==========================================================
    */

    const completedJobs =
        jobs.filter(
            job =>
                job.status === "completed"
        ).length;


    const activeJobs =
        jobs.filter(
            job =>
                job.status === "queued" ||
                job.status === "processing"
        ).length;


    /*
    ==========================================================
    PAGE
    ==========================================================
    */

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
                            {activeJobs}
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

                            onClick={() => loadJobs()}

                            disabled={
                                loading ||
                                refreshing ||
                                clearingDatabase
                            }

                        >

                            <RefreshCw

                                size={17}

                                className={
                                    refreshing
                                        ?
                                        "spin"
                                        :
                                        ""
                                }

                            />

                            Refresh

                        </button>


                    </div>


                </div>


                {
                    loading

                        ?

                        <div className="empty-state">

                            Loading history...

                        </div>


                        :

                        error

                            ?

                            <div className="empty-state">

                                {error}

                            </div>


                            :

                            jobs.length === 0

                                ?

                                <div className="empty-state">

                                    No processing jobs found.

                                </div>


                                :

                                <div className="history-table-container">


                                    <table className="history-table">


                                        <thead>

                                            <tr>

                                                <th>
                                                    ID
                                                </th>

                                                <th>
                                                    File
                                                </th>

                                                <th>
                                                    Status
                                                </th>

                                                <th>
                                                    Progress
                                                </th>

                                                <th>
                                                    Created
                                                </th>

                                                <th>
                                                    Started
                                                </th>

                                                <th>
                                                    Completed
                                                </th>

                                                <th>
                                                    Analysis
                                                </th>

                                            </tr>

                                        </thead>


                                        <tbody>


                                            {
                                                jobs.map(job => (


                                                    <tr key={job.id}>


                                                        <td>
                                                            #{job.id}
                                                        </td>


                                                        <td>

                                                            <div className="history-file-cell">

                                                                <FileText size={16} />

                                                                <span>
                                                                    {job.filename || "-"}
                                                                </span>

                                                            </div>

                                                        </td>


                                                        <td>

                                                            <span

                                                                className={
                                                                    `status-badge ${statusClass(job.status)}`
                                                                }

                                                            >

                                                                {job.status}

                                                            </span>

                                                        </td>


                                                        <td>

                                                            {job.progress ?? 0}%

                                                        </td>


                                                        <td>

                                                            {formatDate(
                                                                job.created_at
                                                            )}

                                                        </td>


                                                        <td>

                                                            {formatDate(
                                                                job.started_at
                                                            )}

                                                        </td>


                                                        <td>

                                                            {formatDate(
                                                                job.completed_at
                                                            )}

                                                        </td>


                                                        <td>


                                                            {
                                                                job.status === "completed"

                                                                    ?

                                                                    <button

                                                                        type="button"

                                                                        className="history-view-btn"

                                                                        onClick={() =>
                                                                            openAnalysis(job)
                                                                        }

                                                                    >

                                                                        <ExternalLink
                                                                            size={15}
                                                                        />

                                                                        View Analysis

                                                                    </button>


                                                                    :

                                                                    <span className="history-analysis-disabled">

                                                                        â€”

                                                                    </span>
                                                            }


                                                        </td>


                                                    </tr>


                                                ))
                                            }


                                        </tbody>


                                    </table>


                                </div>

                }


            </div>


            {/* =================================================
                DATABASE MANAGEMENT
            ================================================= */}

            <div className="history-danger-zone">


                <div className="history-danger-content">


                    <div className="history-danger-icon">

                        <AlertTriangle size={22} />

                    </div>


                    <div>

                        <h2>
                            Database Management
                        </h2>

                        <p>
                            Permanently remove all uploaded log
                            entries, detections, and analysis history.
                        </p>

                    </div>


                </div>


                <button

                    type="button"

                    className="history-clear-btn"

                    onClick={clearDatabase}

                    disabled={
                        clearingDatabase ||
                        activeJobs > 0
                    }

                >

                    <Trash2 size={17} />

                    {
                        clearingDatabase
                            ?
                            "Clearing..."
                            :
                            "Clear Database"
                    }

                </button>


            </div>


            {
                activeJobs > 0 && (

                    <p className="history-clear-warning">

                        <AlertTriangle size={15} />

                        Wait for active processing jobs to finish
                        before clearing the database.

                    </p>

                )
            }


        </div>

    );

}


export default History;
