import { useEffect, useState } from "react";

import apiClient from "../api/client";

import SeverityChart from "../components/SeverityChart";
import AttackChart from "../components/AttackChart";
import AttackMap from "../components/AttackMap";
import DetectionTimeline from "../components/DetectionTimeline";
import TopAttackers from "../components/TopAttackers";

import "./Page.css";



function Analytics(){


    const [summary,setSummary] = useState({});

    const [detections,setDetections] = useState([]);

    const [loading,setLoading] = useState(true);

    const [error,setError] = useState(null);







    useEffect(()=>{


        loadAnalytics();


    },[]);









    const loadAnalytics = async()=>{


        try{


            setError(null);



            const summaryResponse =

                await apiClient.get(
                    "/analysis/summary"
                );





            const detectionResponse =

                await apiClient.get(
                    "/analysis/detections?limit=100"
                );






            setSummary(

                summaryResponse.data || {}

            );





            setDetections(

                detectionResponse.data?.items || []

            );





        }



        catch(error){


            console.error(

                "Analytics loading failed:",

                error

            );



            setError(

                "Failed to load analytics data"

            );



        }





        finally{


            setLoading(false);


        }



    };









    if(loading){


        return (

            <div className="dashboard-loading">

                Loading analytics...

            </div>

        );


    }









    if(error){


        return (

            <div className="dashboard-loading">

                {error}

            </div>

        );


    }









    return(


        <div className="page analytics-page">







            <div className="page-heading">



                <h1>

                    Security Analytics

                </h1>



                <p>

                    Identify attack trends,
                    patterns and threat behaviour

                </p>



            </div>









            <section>


                <AttackMap

                    detections={
                        detections
                    }

                />


            </section>









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









            <section>


                <DetectionTimeline


                    timeline={

                        summary?.timeline || {}

                    }


                />


            </section>









            <section>


                <TopAttackers


                    sourceIps={

                        summary?.source_ips || {}

                    }


                />


            </section>








        </div>


    );


}




export default Analytics;