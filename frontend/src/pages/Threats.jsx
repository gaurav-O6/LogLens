import { useEffect, useState } from "react";

import DetectionTable from "../components/DetectionTable";
import apiClient from "../api/client";

import "./Page.css";


function Threats(){

    const [detections, setDetections] = useState([]);

    const [search, setSearch] = useState("");

    const [severityFilter, setSeverityFilter] = useState("All");

    const [attackFilter, setAttackFilter] = useState("All");



    useEffect(()=>{

        loadThreats();

    },[]);



    const loadThreats = async()=>{

        try{

            const response =
                await apiClient.get("/analysis/detections");


            setDetections(response.data);


        }
        catch(error){

            console.error(error);

        }

    };



    const attackTypes = [
        "All",
        ...new Set(
            detections.map(
                item => item.attack_type
            )
        )
    ];



    const filteredDetections = detections.filter(
        (item)=>{


            const text =
                search.toLowerCase();


            const matchesSearch =
                item.source_ip
                    .toLowerCase()
                    .includes(text)

                ||

                item.attack_type
                    .toLowerCase()
                    .includes(text)

                ||

                (item.matched_pattern || "")
                    .toLowerCase()
                    .includes(text);



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

        }
    );



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



            <div className="threat-controls">


                <input

                    type="text"

                    placeholder="Search IP, attack type, pattern..."

                    value={search}

                    onChange={
                        (e)=>setSearch(e.target.value)
                    }

                />



                <select

                    value={severityFilter}

                    onChange={
                        (e)=>setSeverityFilter(e.target.value)
                    }

                >

                    <option>
                        All
                    </option>

                    <option>
                        High
                    </option>

                    <option>
                        Medium
                    </option>

                    <option>
                        Low
                    </option>


                </select>




                <select

                    value={attackFilter}

                    onChange={
                        (e)=>setAttackFilter(e.target.value)
                    }

                >

                    {
                        attackTypes.map(
                            (type)=>(
                                <option
                                    key={type}
                                >
                                    {type}
                                </option>
                            )
                        )
                    }

                </select>



            </div>




            <DetectionTable

                detections={filteredDetections}

            />



        </div>

    );

}


export default Threats;