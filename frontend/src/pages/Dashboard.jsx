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

import "./dashboard.css";


function Dashboard(){


    const [summary,setSummary] = useState(null);

    const [detections,setDetections] = useState([]);

    const [selectedDetection,setSelectedDetection] = useState(null);


    const [loading,setLoading] = useState(true);


    const [page,setPage] = useState(1);

    const [pages,setPages] = useState(1);

    const [total,setTotal] = useState(0);



    const [filters,setFilters] = useState({

        severity:"All",

        network:"All",

        attackType:"All",

        search:"",

    });







    useEffect(()=>{

        fetchSummary();

    },[]);





    useEffect(()=>{

        fetchDetections();

    },[page]);







    const fetchSummary = async()=>{


        try{


            const response =
                await apiClient.get(
                    "/analysis/summary"
                );


            setSummary(
                response.data || {}
            );


        }


        catch(error){

            console.error(
                "Summary loading failed:",
                error
            );


            setSummary({});


        }


    };









    const fetchDetections = async()=>{


        try{


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
                "Detection loading failed:",
                error
            );


            setDetections([]);


        }


        finally{

            setLoading(false);

        }


    };











    const filteredDetections =

    detections.filter(item=>{


        if(!item){

            return false;

        }



        if(

            filters.severity !== "All"

            &&

            item.severity !== filters.severity

        ){

            return false;

        }





        if(

            filters.attackType !== "All"

            &&

            item.attack_type !== filters.attackType

        ){

            return false;

        }






        if(

            filters.network === "Internal"

            &&

            !item.is_private_ip

        ){

            return false;

        }





        if(

            filters.network === "External"

            &&

            item.is_private_ip

        ){

            return false;

        }





        if(filters.search.trim()){


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









    const attackTypes =

        Object.keys(
            summary?.attack_types || {}
        );









    if(loading){


        return (

            <div className="dashboard-loading">

                Loading security analytics...

            </div>

        );


    }









    return (


        <div className="dashboard">






            <div className="dashboard-title">


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


                    onClose={()=>{

                        setSelectedDetection(null);

                    }}

                />

            }






        </div>


    );


}


export default Dashboard;