import { useEffect, useState } from "react";

import DetectionTable from "../components/DetectionTable";
import InvestigationPanel from "../components/InvestigationPanel";
import ThreatToolbar from "../components/ThreatToolbar";
import AttackStats from "../components/AttackStats";

import apiClient from "../api/client";

import "./Page.css";



function Threats(){


    const [detections,setDetections] = useState([]);

    const [selectedDetection,setSelectedDetection] = useState(null);


    const [search,setSearch] = useState("");

    const [severityFilter,setSeverityFilter] = useState("All");

    const [attackFilter,setAttackFilter] = useState("All");



    const [page,setPage] = useState(1);

    const [pages,setPages] = useState(1);

    const [total,setTotal] = useState(0);

    const [loading,setLoading] = useState(true);








    useEffect(()=>{


        loadThreats();


        setSelectedDetection(null);


    },[page]);









    const loadThreats = async()=>{


        try{


            setLoading(true);



            const response =

                await apiClient.get(

                    `/analysis/detections?page=${page}&limit=100`

                );




            setDetections(

                response.data?.items || []

            );



            setPages(

                response.data?.pages || 1

            );



            setTotal(

                response.data?.total || 0

            );


        }



        catch(error){


            console.error(

                "Failed to load threats:",

                error

            );


            setDetections([]);


        }



        finally{


            setLoading(false);


        }


    };









    const attackOptions = [


        ...new Set(


            detections

            .filter(Boolean)

            .map(

                item=>item.attack_type

            )


        )


    ];









    const filteredDetections =


    detections


    .filter(Boolean)


    .filter(item=>{





        const text =

            search.trim().toLowerCase();





        const matchesSearch =


            !text

            ||

            item.source_ip
            ?.toLowerCase()
            .includes(text)


            ||


            item.attack_type
            ?.toLowerCase()
            .includes(text)


            ||


            item.matched_pattern
            ?.toLowerCase()
            .includes(text);








        const matchesSeverity =


            severityFilter==="All"

            ||

            item.severity===severityFilter;








        const matchesAttack =


            attackFilter==="All"

            ||

            item.attack_type===attackFilter;






        return (

            matchesSearch

            &&

            matchesSeverity

            &&

            matchesAttack

        );



    })



    .sort((a,b)=>{


        const rank = {


            High:3,

            Medium:2,

            Low:1


        };



        return (

            (rank[b.severity] || 0)

            -

            (rank[a.severity] || 0)

        );


    });









    const sourceIps =


    detections.reduce(


        (acc,item)=>{


            if(!item?.source_ip){

                return acc;

            }



            acc[item.source_ip] =


                (acc[item.source_ip] || 0)

                +

                1;



            return acc;



        },


        {}

    );









    const summary = {


        total_attacks: total,



        severity:{


            High:

                detections.filter(

                    i=>i?.severity==="High"

                ).length,



            Medium:

                detections.filter(

                    i=>i?.severity==="Medium"

                ).length,



            Low:

                detections.filter(

                    i=>i?.severity==="Low"

                ).length,


        },



        source_ips:sourceIps,


    };









    if(loading){


        return (

            <div className="dashboard-loading">

                Loading threats...

            </div>

        );


    }









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


                onSearchChange={setSearch}



                severityFilter={severityFilter}


                onSeverityChange={setSeverityFilter}



                attackFilter={attackFilter}


                attackOptions={attackOptions}


                onAttackChange={setAttackFilter}


            />









            <div className="threat-workspace">






                <div className="threat-list">



                    <DetectionTable


                        detections={filteredDetections}


                        onSelect={setSelectedDetection}


                        selected={selectedDetection}


                    />



                </div>









                <div className="investigation-area">



                    {

                    selectedDetection


                    ?


                    <InvestigationPanel


                        detection={selectedDetection}


                        onClose={()=>{


                            setSelectedDetection(null);


                        }}


                    />



                    :


                    <div className="empty-investigation">


                        <h3>

                            Select a threat event

                        </h3>



                        <p>

                            Choose an incident from the table
                            to view investigation details

                        </p>


                    </div>


                    }



                </div>






            </div>









            {

                pages > 1 &&


                <div className="pagination">


                    <button


                        disabled={page===1}


                        onClick={()=>setPage(page-1)}


                    >

                        Previous

                    </button>







                    <span>

                        Page {page} / {pages}

                    </span>







                    <button


                        disabled={page===pages}


                        onClick={()=>setPage(page+1)}


                    >

                        Next

                    </button>




                </div>


            }





        </div>


    );


}


export default Threats;