import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import apiClient from "../api/client";

import SummaryCards from "../components/SummaryCards";
import ThreatIntelCards from "../components/ThreatIntelCards";
import SeverityChart from "../components/SeverityChart";
import AttackChart from "../components/AttackChart";
import AttackMap from "../components/AttackMap";
import DetectionTable from "../components/DetectionTable";
import DetectionTimeline from "../components/DetectionTimeline";
import TopAttackers from "../components/TopAttackers";
import InvestigationPanel from "../components/InvestigationPanel";
import ThreatFilterBar from "../components/ThreatFilterBar";

import "./dashboard.css";


function Dashboard() {

    const [searchParams] = useSearchParams();

    const jobId = searchParams.get("job_id");


    const [summary, setSummary] = useState(null);

    const [detections, setDetections] = useState([]);

    const [selectedDetection, setSelectedDetection] = useState(null);


    const [loading, setLoading] = useState(true);

    const [summaryLoading, setSummaryLoading] = useState(true);


    const [page, setPage] = useState(1);

    const [pages, setPages] = useState(1);

    const [total, setTotal] = useState(0);


    const [filters, setFilters] = useState({

        severity: "All",

        network: "All",

        attackType: "All",

        search: "",

    });


    /*
    ==========================================================
    RESET DASHBOARD WHEN JOB CHANGES
    ==========================================================
    */

    useEffect(() => {

        setPage(1);

        setSelectedDetection(null);

        /*
         * Clear old dashboard data immediately.
         *
         * This is important when switching from:
         *
         *   /?job_id=27
         *
         * back to:
         *
         *   /
         *
         * or from one job to another.
         *
         * Without clearing this, React can temporarily display
         * the previous job's statistics while the new request
         * is still loading.
         */

        setSummary(null);

        setDetections([]);

        setPages(1);

        setTotal(0);

    }, [jobId]);


    /*
    ==========================================================
    LOAD SUMMARY
    ==========================================================
    */

    useEffect(() => {

        let cancelled = false;


        const fetchSummary = async () => {

            try {

                setSummaryLoading(true);


                /*
                 * Use Axios params instead of manually constructing
                 * the query string.
                 */

                const response =
                    await apiClient.get(
                        "/analysis/summary",
                        {
                            params: jobId
                                ? { job_id: jobId }
                                : {},
                        }
                    );


                if (cancelled) {

                    return;

                }


                const data =
                    response.data || {};


                /*
                 * Safety check:
                 *
                 * If we asked for Job #27, the backend must return
                 * job_id 27.
                 *
                 * This prevents an accidental global summary from
                 * being displayed inside a job-specific dashboard.
                 */

                if (jobId) {

                    const returnedJobId =
                        data.job_id !== null &&
                        data.job_id !== undefined
                            ? String(data.job_id)
                            : null;


                    if (returnedJobId !== String(jobId)) {

                        console.error(
                            "JOB SUMMARY MISMATCH:",
                            {
                                requestedJobId: String(jobId),
                                returnedJobId,
                                response: data,
                            }
                        );


                        setSummary({});

                        return;

                    }

                }


                console.log(
                    "DASHBOARD SUMMARY:",
                    {
                        requestedJobId: jobId || "ALL",
                        returnedJobId:
                            data.job_id ?? null,
                        totalAttacks:
                            data.total_attacks ?? 0,
                    }
                );


                setSummary(data);

            }

            catch (error) {

                if (cancelled) {

                    return;

                }


                console.error(
                    "Summary loading failed:",
                    error
                );


                setSummary({});

            }

            finally {

                if (!cancelled) {

                    setSummaryLoading(false);

                }

            }

        };


        fetchSummary();


        return () => {

            cancelled = true;

        };

    }, [jobId]);


    /*
    ==========================================================
    LOAD DETECTIONS
    ==========================================================
    */

    useEffect(() => {

        let cancelled = false;


        const fetchDetections = async () => {

            try {

                setLoading(true);


                const params = {

                    page,

                    limit: 100,

                    ...(jobId
                        ? { job_id: jobId }
                        : {}),

                };


                const response =
                    await apiClient.get(
                        "/analysis/detections",
                        {
                            params,
                        }
                    );


                if (cancelled) {

                    return;

                }


                const data =
                    response.data || {};


                /*
                 * Safety check for job-specific requests.
                 */

                if (jobId) {

                    const returnedJobId =
                        data.job_id !== null &&
                        data.job_id !== undefined
                            ? String(data.job_id)
                            : null;


                    if (returnedJobId !== String(jobId)) {

                        console.error(
                            "JOB DETECTIONS MISMATCH:",
                            {
                                requestedJobId: String(jobId),
                                returnedJobId,
                                response: data,
                            }
                        );


                        setDetections([]);

                        setPages(1);

                        setTotal(0);

                        return;

                    }

                }


                console.log(
                    "DASHBOARD DETECTIONS:",
                    {
                        requestedJobId: jobId || "ALL",
                        returnedJobId:
                            data.job_id ?? null,
                        items:
                            data.items?.length ?? 0,
                        total:
                            data.total ?? 0,
                    }
                );


                setDetections(
                    Array.isArray(data.items)
                        ? data.items
                        : []
                );


                setPages(
                    data.pages || 1
                );


                setTotal(
                    data.total || 0
                );

            }

            catch (error) {

                if (cancelled) {

                    return;

                }


                console.error(
                    "Detection loading failed:",
                    error
                );


                setDetections([]);

                setPages(1);

                setTotal(0);

            }

            finally {

                if (!cancelled) {

                    setLoading(false);

                }

            }

        };


        fetchDetections();


        return () => {

            cancelled = true;

        };

    }, [page, jobId]);


    /*
    ==========================================================
    FILTER DETECTIONS
    ==========================================================
    */

    const filteredDetections =
        detections.filter(item => {

            if (!item) {

                return false;

            }


            if (
                filters.severity !== "All"
                &&
                item.severity !== filters.severity
            ) {

                return false;

            }


            if (
                filters.attackType !== "All"
                &&
                item.attack_type !== filters.attackType
            ) {

                return false;

            }


            if (
                filters.network === "Internal"
                &&
                !item.is_private_ip
            ) {

                return false;

            }


            if (
                filters.network === "External"
                &&
                item.is_private_ip
            ) {

                return false;

            }


            if (filters.search.trim()) {

                const search =
                    filters.search.toLowerCase();


                return (

                    item.source_ip
                        ?.toLowerCase()
                        .includes(search)

                    ||

                    item.request_path
                        ?.toLowerCase()
                        .includes(search)

                    ||

                    item.attack_type
                        ?.toLowerCase()
                        .includes(search)

                );

            }


            return true;

        });


    /*
    ==========================================================
    ATTACK TYPES
    ==========================================================
    */

    const attackTypes =

        Object.keys(
            summary?.attack_types || {}
        );


    /*
    ==========================================================
    INITIAL LOADING
    ==========================================================
    */

    if (
        summaryLoading ||
        loading
    ) {

        return (

            <div className="dashboard-loading">

                Loading security analytics...

            </div>

        );

    }


    /*
    ==========================================================
    PAGE
    ==========================================================
    */

    return (

        <div className="dashboard">


            <div className="dashboard-title">

                <div>

                    <h1>

                        SOC Dashboard

                    </h1>


                    <p>

                        Security operations overview —
                        monitor threats,
                        analyze attack patterns,
                        and investigate incidents

                    </p>

                </div>


                {
                    jobId &&

                    <div className="dashboard-job-context">

                        <span>
                            Viewing Analysis
                        </span>

                        <strong>
                            Job #{jobId}
                        </strong>

                    </div>
                }

            </div>


            <ThreatFilterBar

                filters={filters}

                setFilters={setFilters}

                attackTypes={attackTypes}

            />


            {
                summary &&

                <SummaryCards

                    summary={summary}

                />

            }


            {
                summary &&

                <ThreatIntelCards

                    summary={summary}

                />

            }


            <AttackMap

                detections={
                    filteredDetections
                }

            />


            <section>

                <div className="dashboard-grid">


                    <SeverityChart

                        severity={
                            summary?.severity || {}
                        }

                    />


                    <AttackChart

                        attacks={
                            summary?.attack_types || {}
                        }

                    />

                </div>

            </section>


            <DetectionTimeline

                timeline={
                    summary?.timeline || {}
                }

            />


            <TopAttackers

                sourceIps={
                    summary?.source_ips || {}
                }

            />


            <DetectionTable

                detections={
                    filteredDetections
                }

                onSelect={
                    setSelectedDetection
                }

                selected={
                    selectedDetection
                }

            />


            {
                selectedDetection &&

                <InvestigationPanel

                    detection={
                        selectedDetection
                    }

                    onClose={() => {

                        setSelectedDetection(null);

                    }}

                />

            }


            {
                pages > 1 &&

                <div className="dashboard-pagination">


                    <button

                        type="button"

                        onClick={() =>
                            setPage(
                                current =>
                                    Math.max(
                                        current - 1,
                                        1
                                    )
                            )
                        }

                        disabled={page <= 1}

                    >

                        Previous

                    </button>


                    <span>

                        Page {page} / {pages}

                    </span>


                    <button

                        type="button"

                        onClick={() =>
                            setPage(
                                current =>
                                    Math.min(
                                        current + 1,
                                        pages
                                    )
                            )
                        }

                        disabled={page >= pages}

                    >

                        Next

                    </button>


                </div>

            }


        </div>

    );

}


export default Dashboard;