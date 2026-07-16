import { useEffect, useState } from "react";
import apiClient from "../api/client";

import SummaryCards from "../components/SummaryCards";
import SeverityChart from "../components/SeverityChart";
import AttackChart from "../components/AttackChart";
import DetectionTable from "../components/DetectionTable";
import DetectionTimeline from "../components/DetectionTimeline";
import TopAttackers from "../components/TopAttackers";

import "./Dashboard.css";

function Dashboard() {

    const [summary, setSummary] = useState(null);
    const [detections, setDetections] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {

        try {

            const summaryResponse =
                await apiClient.get("/analysis/summary");

            const detectionResponse =
                await apiClient.get("/analysis/detections");

            setSummary(summaryResponse.data);
            setDetections(detectionResponse.data);

        }
        catch (error) {

            console.error(error);

        }
        finally {

            setLoading(false);

        }

    };


    const exportReport = (format) => {

        window.open(
            `http://localhost:5000/api/v1/analysis/export/${format}`,
            "_blank"
        );

    };


    if (loading) {

        return (

            <div className="dashboard-loading">

                Loading security analytics...

            </div>

        );

    }


    return (

        <div className="dashboard">

            <div className="dashboard-title">

                <div>

                    <h1>
                        SOC Dashboard
                    </h1>

                    <p>
                        Security event monitoring and threat intelligence
                    </p>

                </div>

                <div className="export-buttons">

                    <button
                        className="export-btn"
                        onClick={() => exportReport("csv")}
                    >
                        Export CSV
                    </button>

                    <button
                        className="export-btn"
                        onClick={() => exportReport("json")}
                    >
                        Export JSON
                    </button>

                </div>

            </div>


            {
                summary &&
                <SummaryCards summary={summary} />
            }


            <section>

                <div className="section-header">

                    <h2>
                        Threat Overview
                    </h2>

                    <p>
                        Attack severity and classification analysis
                    </p>

                </div>

                <div className="dashboard-grid">

                    <SeverityChart
                        severity={summary.severity}
                    />

                    <AttackChart
                        attacks={summary.attack_types}
                    />

                </div>

            </section>


            <section>

                <div className="section-header">

                    <h2>
                        Attack Activity
                    </h2>

                    <p>
                        Security events over time
                    </p>

                </div>

                <DetectionTimeline
                    detections={detections}
                />

            </section>


            {/* NEW Top Attackers Section */}

            <section>

                <TopAttackers
                    sourceIps={summary.source_ips}
                />

            </section>


            <section>

                <div className="section-header">

                    <h2>
                        Recent Threats
                    </h2>

                </div>

                <DetectionTable
                    detections={detections}
                />

            </section>

        </div>

    );

}

export default Dashboard;