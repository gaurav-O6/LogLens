import {
    Activity,
    Database,
    Server
} from "lucide-react";

import "./topbar.css";


function Topbar() {

    return (

        <header className="topbar">


            <div>

                <h1>
                    Security Overview
                </h1>


                <p>
                    Real-time log analysis and threat monitoring
                </p>


            </div>



            <div className="status-group">


                <div className="status-badge online">

                    <Activity size={15}/>

                    Monitoring

                </div>



                <div className="status-badge">

                    <Database size={15}/>

                    PostgreSQL

                </div>



                <div className="status-badge">

                    <Server size={15}/>

                    Backend

                </div>


            </div>


        </header>

    );

}


export default Topbar;