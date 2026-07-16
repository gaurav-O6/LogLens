import { useEffect, useState } from "react";

import DetectionTable from "../components/DetectionTable";
import InvestigationPanel from "../components/InvestigationPanel";
import ThreatToolbar from "../components/ThreatToolbar";
import AttackStats from "../components/AttackStats";

import apiClient from "../api/client";

import "./Page.css";


function Threats() {

    const [detections, setDetections] = useState([]);

    const [selectedDetection, setSelectedDetection] = useState(null);

    const [search, setSearch] = useState("");

    const [severityFilter, setSeverityFilter] = useState("All");

    const [attackFilter, setAttackFilter] = useState("All");


    useEffect(() => {

        loadThreats();

    }, []);



    const loadThreats = async () => {

        try {

            const response =
                await apiClient.get("/analysis/detections");


            setDetections(response.data);


        } catch(error) {

            console.error(
                "Failed to load threats:",
                error
            );

        }

    };



    const attackOptions = [
        ...new Set(
            detections.map(
                item => item.attack_type
            )
        )
    ];



    const filteredDetections =
        detections.filter((item) => {


            const searchText =
                search.toLowerCase();



            const matchesSearch =

                item.source_ip
                    ?.toLowerCase()
                    .includes(searchText)

                ||

                item.attack_type
                    ?.toLowerCase()
                    .includes(searchText)

                ||

                item.matched_pattern
                    ?.toLowerCase()
                    .includes(searchText);



            const matchesSeverity =

                severityFilter === "All"

                ||

                item.severity === severityFilter;



            const matchesAttack =

                attackFilter === "All"

                ||

                item.attack_type === attackFilter;



            return (

                matchesSearch

                &&

                matchesSeverity

                &&

                matchesAttack

            );


        });



    const summary = {

        total_attacks:
            detections.length,


        severity: {

            High:
                detections.filter(
                    item =>
                    item.severity === "High"
                ).length,


            Medium:
                detections.filter(
                    item =>
                    item.severity === "Medium"
                ).length,


            Low:
                detections.filter(
                    item =>
                    item.severity === "Low"
                ).length

        },


        source_ips:
            detections.reduce(
                (acc,item)=>{

                    acc[item.source_ip] = true;

                    return acc;

                },
                {}
            )

    };



    return (

        <div className="page threat-page">


            <div className="page-heading">

                <h1>
                    Threat Center
                </h1>


                <p>
                    Investigate detected security incidents
                </p>

            </div>



            <AttackStats
                summary={summary}
            />



            <ThreatToolbar

                searchTerm={search}

                onSearchChange={
                    setSearch
                }


                severityFilter={
                    severityFilter
                }


                onSeverityChange={
                    setSeverityFilter
                }


                attackFilter={
                    attackFilter
                }


                attackOptions={
                    attackOptions
                }


                onAttackChange={
                    setAttackFilter
                }

            />



            <div className="threat-workspace">


    <DetectionTable

        detections={
            filteredDetections
        }


        onSelect={
            setSelectedDetection
        }


    />


</div>



{
    selectedDetection && (

        <InvestigationPanel

            detection={
                selectedDetection
            }


            onClose={
                ()=>setSelectedDetection(null)
            }

        />

    )
}

        </div>

    );

}


export default Threats;