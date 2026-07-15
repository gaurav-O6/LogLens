import {
    ShieldAlert,
    AlertTriangle,
    Globe
} from "lucide-react";


function AttackStats({ summary }) {


    return (

        <div className="stats-container">


            <div className="stat-card">

                <ShieldAlert size={35}/>

                <div>

                    <h3>
                        Total Attacks
                    </h3>

                    <p>
                        {summary.total_attacks}
                    </p>

                </div>

            </div>



            <div className="stat-card">

                <AlertTriangle size={35}/>

                <div>

                    <h3>
                        High Severity
                    </h3>

                    <p>
                        {summary.severity.High || 0}
                    </p>

                </div>

            </div>



            <div className="stat-card">

                <Globe size={35}/>

                <div>

                    <h3>
                        Attack Sources
                    </h3>

                    <p>
                        {
                        Object.keys(summary.source_ips).length
                        }
                    </p>

                </div>


            </div>


        </div>

    );

}


export default AttackStats;