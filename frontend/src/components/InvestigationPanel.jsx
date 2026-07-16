import {
    X,
    MapPin,
    ShieldAlert,
    Globe,
    FileText
} from "lucide-react";


function InvestigationPanel({
    detection,
    onClose
}) {


    return (

        <aside className="investigation-panel">


            <div className="panel-header">


                <div>

                    <h2>
                        Threat Investigation
                    </h2>


                    <p>
                        Detailed security event analysis
                    </p>

                </div>



                <button
                    onClick={onClose}
                >

                    <X size={20}/>

                </button>


            </div>





            <div className="risk-banner">


                <ShieldAlert size={28}/>


                <div>

                    <span>
                        Severity
                    </span>


                    <strong>
                        {detection.severity}
                    </strong>

                </div>


            </div>





            <section className="investigation-section">


                <h3>
                    Attack Information
                </h3>


                <p>

                    <strong>
                        Type:
                    </strong>

                    {" "}

                    {detection.attack_type}

                </p>



                <p>

                    <strong>
                        Pattern:
                    </strong>

                    {" "}

                    {
                        detection.matched_pattern || "-"
                    }

                </p>


            </section>





            <section className="investigation-section">


                <h3>
                    Source Intelligence
                </h3>



                <p>

                    <strong>
                        IP:
                    </strong>

                    {" "}

                    {detection.source_ip}

                </p>




                <p className="location-line">


                    <MapPin size={16}/>


                    {

                        detection.city &&
                        detection.country

                        ?

                        `${detection.city}, ${detection.country}`

                        :

                        "Unknown Location"

                    }


                </p>





                <p>


                    <Globe size={16}/>


                    {

                        detection.latitude &&
                        detection.longitude

                        ?

                        `${detection.latitude}, ${detection.longitude}`

                        :

                        "Coordinates unavailable"

                    }


                </p>



            </section>







            <section className="investigation-section">


                <h3>
                    HTTP Evidence
                </h3>



                <p>

                    <strong>
                        Method:
                    </strong>

                    {" "}

                    {
                        detection.http_method || "-"
                    }

                </p>



                <p>

                    <strong>
                        Endpoint:
                    </strong>

                    {" "}

                    {
                        detection.request_path || "-"
                    }

                </p>



                <p>

                    <strong>
                        Status:
                    </strong>

                    {" "}

                    {
                        detection.status_code || "-"
                    }

                </p>



            </section>







            <section className="investigation-section">


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



        </aside>

    );

}


export default InvestigationPanel;