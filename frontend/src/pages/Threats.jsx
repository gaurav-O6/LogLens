import { useEffect, useMemo, useState } from "react";

import apiClient from "../api/client";

import DetectionTable from "../components/DetectionTable";
import ThreatToolbar from "../components/ThreatToolbar";

import "./Page.css";

function Threats() {

    const [detections, setDetections] = useState([]);

    const [searchTerm, setSearchTerm] = useState("");

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

        }

        catch (error) {

            console.error(error);

        }

    };

    const attackOptions = useMemo(() => {

        return [...new Set(
            detections.map(
                (item) => item.attack_type
            )
        )];

    }, [detections]);

    const filteredDetections = useMemo(() => {

        return detections.filter((item) => {

            const matchesSearch =

                item.attack_type
                    .toLowerCase()
                    .includes(searchTerm.toLowerCase())

                ||

                item.source_ip
                    .toLowerCase()
                    .includes(searchTerm.toLowerCase())

                ||

                (item.matched_pattern || "")
                    .toLowerCase()
                    .includes(searchTerm.toLowerCase());

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

    }, [

        detections,

        searchTerm,

        severityFilter,

        attackFilter

    ]);

    return (

        <div className="page">

            <div className="page-heading">

                <h1>
                    Threat Center
                </h1>

                <p>
                    Investigate detected security threats
                </p>

            </div>

            <ThreatToolbar

                searchTerm={searchTerm}
                onSearchChange={setSearchTerm}

                severityFilter={severityFilter}
                onSeverityChange={setSeverityFilter}

                attackFilter={attackFilter}
                attackOptions={attackOptions}
                onAttackChange={setAttackFilter}

            />

            <DetectionTable
                detections={filteredDetections}
            />

        </div>

    );

}

export default Threats;