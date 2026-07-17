import {
    X,
    MapPin,
    ShieldAlert,
    Globe,
    FileText,
    Home,
    Activity,
    Terminal,
    Server,
    Clock,
    Copy,
    CheckCircle
} from "lucide-react";

import { useState } from "react";


function InvestigationPanel({
    detection,
    onClose
}) {


    const [copied,setCopied] = useState(false);



    const getRiskLabel = (severity)=>{

        if(severity === "High")
            return "CRITICAL THREAT";


        if(severity === "Medium")
            return "SUSPICIOUS ACTIVITY";


        return "LOW RISK EVENT";

    };



    const formatTimestamp = (timestamp)=>{

        if(!timestamp)
            return "-";


        return timestamp.replace(
            /:(\d{2})\s/,
            " $1 "
        );

    };



    const copyIP = ()=>{

        navigator.clipboard.writeText(
            detection.source_ip
        );


        setCopied(true);


        setTimeout(()=>{
            setCopied(false);
        },1500);

    };



    const countryFlag = (country)=>{

        const flags={

            "United States":"🇺🇸",
            "India":"🇮🇳",
            "Germany":"🇩🇪",
            "United Kingdom":"🇬🇧"

        };


        return flags[country] || "🌐";

    };





    return (

        <aside className="investigation-panel">


            <div className="panel-header">


                <div>


                    <div className="incident-title">

                        <ShieldAlert size={22}/>

                        <h2>
                            Threat Investigation
                        </h2>

                    </div>


                    <p>
                        Detailed security event analysis
                    </p>


                </div>



                <button
                    onClick={onClose}
                >

                    <X size={18}/>

                </button>


            </div>





            <div className="investigation-body">





                {/* Threat Banner */}

                <div
                    className={
                        `threat-banner ${
                            detection.severity?.toLowerCase()
                        }`
                    }
                >

                    <ShieldAlert size={30}/>


                    <div>

                        <span>
                            {getRiskLabel(
                                detection.severity
                            )}
                        </span>


                        <strong>
                            {detection.severity}
                        </strong>

                    </div>


                </div>







                {/* Incident Details */}

                <section className="investigation-card">


                    <h3>

                        <Activity size={16}/>

                        Attack Details

                    </h3>




                    <div className="info-grid">


                        <div className="info-item">

                            <span>
                                Incident ID
                            </span>

                            <strong>
                                #{detection.id}
                            </strong>

                        </div>



                        <div className="info-item">

                            <span>
                                Attack Type
                            </span>

                            <strong>
                                {detection.attack_type}
                            </strong>

                        </div>



                        <div className="info-item">

                            <span>
                                Pattern
                            </span>

                            <strong>
                                {
                                    detection.matched_pattern || "-"
                                }
                            </strong>

                        </div>


                        <div className="info-item">

                            <span>
                                Status Code
                            </span>


                            <strong>
                                {detection.status_code || "-"}
                            </strong>

                        </div>


                    </div>


                </section>








                {/* Source Intelligence */}

                <section className="investigation-card">


                    <h3>

                        <Globe size={16}/>

                        Source Intelligence

                    </h3>




                    <div className="info-row">

                        <Server size={16}/>


                        <span>
                            {detection.source_ip}
                        </span>


                        <button
                            onClick={copyIP}
                            title="Copy IP"
                        >

                            {
                                copied
                                ?
                                <CheckCircle size={15}/>
                                :
                                <Copy size={15}/>
                            }

                        </button>


                    </div>





                    <div className="info-row">


                        {
                            detection.is_private_ip

                            ?

                            <Home size={16}/>

                            :

                            <Globe size={16}/>

                        }



                        <span>

                            {
                                detection.is_private_ip
                                ?
                                "Internal Network"
                                :
                                "External IP"
                            }

                        </span>


                    </div>






                    <div className="info-row">


                        <MapPin size={16}/>


                        <span>


                            {
                                countryFlag(
                                    detection.country
                                )
                            }


                            {" "}


                            {
                                detection.city &&
                                detection.country

                                ?

                                `${detection.city}, ${detection.country}`

                                :

                                "Unknown Location"

                            }


                        </span>


                    </div>





                    {
                        detection.latitude &&
                        detection.longitude &&

                        <div className="info-row">

                            <MapPin size={16}/>


                            <span>

                                Coordinates:

                                {" "}

                                {detection.latitude},

                                {" "}

                                {detection.longitude}

                            </span>


                        </div>

                    }



                </section>









                {/* HTTP Evidence */}

                <section className="investigation-card">


                    <h3>

                        <Terminal size={16}/>

                        HTTP Evidence

                    </h3>




                    <div className="info-grid">


                        <div className="info-item">

                            <span>
                                Method
                            </span>


                            <strong>
                                {
                                    detection.http_method || "-"
                                }
                            </strong>


                        </div>



                        <div className="info-item">

                            <span>
                                Status
                            </span>


                            <strong>

                                {
                                    detection.status_code || "-"
                                }

                            </strong>


                        </div>


                    </div>





                    <div className="endpoint">


                        Endpoint:


                        <strong>

                            {
                                detection.request_path || "-"
                            }

                        </strong>


                    </div>



                </section>









                {/* Time */}

                <section className="investigation-card">


                    <h3>

                        <Clock size={16}/>

                        Event Time

                    </h3>



                    <p>

                        {
                            formatTimestamp(
                                detection.timestamp
                            )
                        }

                    </p>


                </section>









                {/* Raw Event */}

                <section className="investigation-card">


                    <h3>

                        <FileText size={16}/>

                        Raw Event

                    </h3>



                    <pre>

                        {
                            detection.raw_log || "-"
                        }

                    </pre>


                </section>





            </div>


        </aside>

    );

}


export default InvestigationPanel;