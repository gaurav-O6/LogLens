import DetectionTable from "../components/DetectionTable";
import { useEffect,useState } from "react";
import apiClient from "../api/client";

import "./Page.css";


function Threats(){


    const [detections,setDetections]=useState([]);



    useEffect(()=>{

        loadThreats();

    },[]);



    const loadThreats=async()=>{

        try{

            const response =
                await apiClient.get("/analysis/detections");


            setDetections(response.data);


        }
        catch(error){

            console.error(error);

        }

    };



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



            <DetectionTable
                detections={detections}
            />


        </div>

    );

}


export default Threats;