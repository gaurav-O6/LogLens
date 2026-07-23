import { useEffect, useState, useRef } from "react";

import {
    Database,
    CheckCircle,
    Clock3,
    RefreshCw,
    FileText,
} from "lucide-react";

import api from "../api/client";
import "./Page.css";


function History() {


    const [jobs, setJobs] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [refreshing, setRefreshing] = useState(false);


    const jobsRef = useRef([]);





    useEffect(() => {


        loadJobs();


        const interval = setInterval(() => {


            const activeJobs =
                jobsRef.current.some(
                    job =>
                        job.status === "queued" ||
                        job.status === "processing"
                );


            if(activeJobs){

                loadJobs(false);

            }


        },5000);



        return () => {

            clearInterval(interval);

        };


    }, []);







    async function loadJobs(showLoading=true){


        try {


            if(showLoading){

                setLoading(true);

            }
            else{

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


        catch(error){


            console.error(
                "HISTORY ERROR",
                error
            );


            setError(
                "Failed to load job history."
            );


        }


        finally{


            setLoading(false);

            setRefreshing(false);


        }


    }







    const formatDate = (date)=>{


        if(!date){

            return "-";

        }


        return new Date(date)
            .toLocaleString();


    };







    const statusClass=(status)=>{


        switch(status?.toLowerCase()){


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
            job =>
            job.status === "completed"
        ).length;



    const activeJobs =
        jobs.filter(
            job =>
            job.status === "queued" ||
            job.status === "processing"
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

                    <Database size={24}/>

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

                    <CheckCircle size={24}/>

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


                    <Clock3 size={24}/>


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
                                refreshing
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
                    loading ?


                    <div className="empty-state">

                        Loading history...

                    </div>



                    : error ?



                    <div className="empty-state">

                        {error}

                    </div>



                    : jobs.length===0 ?



                    <div className="empty-state">

                        No processing jobs found.

                    </div>



                    :



                    <div className="history-table-container">


                        <table className="history-table">


                            <thead>

                                <tr>

                                    <th>ID</th>

                                    <th>File</th>

                                    <th>Status</th>

                                    <th>Progress</th>

                                    <th>Created</th>

                                    <th>Started</th>

                                    <th>Completed</th>


                                </tr>


                            </thead>





                            <tbody>


                            {
                                jobs.map(job=>(


                                    <tr key={job.id}>


                                        <td>
                                            #{job.id}
                                        </td>



                                        <td>

                                            <FileText size={16}/>

                                            {job.filename}

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