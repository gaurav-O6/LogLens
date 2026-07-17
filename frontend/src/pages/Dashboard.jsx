import { useEffect, useState } from "react";
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

import "./Dashboard.css";


function Dashboard() {


    const [summary, setSummary] = useState(null);

    const [detections, setDetections] = useState([]);

    const [filteredDetections, setFilteredDetections] = useState([]);

    const [selectedDetection, setSelectedDetection] = useState(null);

    const [loading, setLoading] = useState(true);



    const [filters, setFilters] = useState({

        severity: "All",

        network: "All",

        attackType: "All",

        search: "",

    });





    useEffect(() => {

        fetchData();

    }, []);





    useEffect(() => {

        applyFilters();

    }, [filters, detections]);







    const fetchData = async () => {


        try {


            const summaryResponse =
                await apiClient.get("/analysis/summary");



            const detectionResponse =
                await apiClient.get("/analysis/detections");



            setSummary(summaryResponse.data);

            setDetections(detectionResponse.data);



        }

        catch(error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    };








    const applyFilters = () => {


        let result = [...detections];



        if(filters.severity !== "All") {


            result = result.filter(

                item =>
                    item.severity === filters.severity

            );

        }




        if(filters.network !== "All") {


            if(filters.network === "Internal") {


                result = result.filter(

                    item =>
                        item.is_private_ip === true

                );


            }


            else {


                result = result.filter(

                    item =>
                        item.is_private_ip === false

                );


            }

        }







        if(filters.attackType !== "All") {


            result = result.filter(

                item =>
                    item.attack_type === filters.attackType

            );


        }







        if(filters.search.trim() !== "") {


            const search =
                filters.search.toLowerCase();



            result = result.filter(

                item =>

                    item.source_ip
                    ?.toLowerCase()
                    .includes(search)

                    ||

                    item.request_path
                    ?.toLowerCase()
                    .includes(search)

            );


        }






        setFilteredDetections(result);


    };







    const createFilteredSummary = () => {


        const severity = {};

        const attacks = {};

        const ips = {};



        filteredDetections.forEach(item => {


            severity[item.severity] =
                (severity[item.severity] || 0) + 1;



            attacks[item.attack_type] =
                (attacks[item.attack_type] || 0) + 1;



            ips[item.source_ip] =
                (ips[item.source_ip] || 0) + 1;



        });




        return {


            ...summary,


            severity,


            attack_types: attacks,


            source_ips: ips,


            total_attacks:
                filteredDetections.length,

        };


    };






    const exportReport = (format) => {


        window.open(

            `http://localhost:5000/api/v1/analysis/export/${format}`,

            "_blank"

        );


    };







    if(loading) {


        return (

            <div className="dashboard-loading">

                Loading security analytics...

            </div>

        );


    }





    const attackTypes = [

        ...new Set(

            detections.map(
                item => item.attack_type
            )

        )

    ];





    const filteredSummary =
        createFilteredSummary();







    return (

        <div className="dashboard">





<div className="dashboard-title">


    <div className="dashboard-heading">


        <div className="title-row">


            <h1>
                SOC Dashboard
            </h1>


            <span className="status-badge">

                <span className="status-dot"></span>

                Monitoring Active

            </span>


        </div>



        <p>

            Security operations overview — monitor threats,
            analyze attack patterns, and investigate incidents

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







            <ThreatFilterBar

                filters={filters}

                setFilters={setFilters}

                attackTypes={attackTypes}

            />







            {
                summary &&

                <SummaryCards

                    summary={filteredSummary}

                />

            }







            {
                summary &&

                <ThreatIntelCards

                    summary={filteredSummary}

                />

            }








            <section>


                <AttackMap

                    detections={
                        filteredDetections
                    }

                />


            </section>








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

                        severity={
                            filteredSummary.severity
                        }

                    />



                    <AttackChart

                        attacks={
                            filteredSummary.attack_types
                        }

                    />


                </div>


            </section>








            <section>


            <DetectionTimeline
                timeline={
                    filteredSummary.timeline
                }
            />


            </section>








            <section>


                <TopAttackers

                    sourceIps={
                        filteredSummary.source_ips
                    }

                />


            </section>








            <section>


                <DetectionTable

                    detections={
                        filteredDetections
                    }

                    onSelect={
                        setSelectedDetection
                    }

                />


            </section>








            {
                selectedDetection &&

                <InvestigationPanel

                    detection={
                        selectedDetection
                    }

                    onClose={
                        () =>
                            setSelectedDetection(null)
                    }

                />

            }




        </div>

    );


}


export default Dashboard;