import {
    Globe,
    Radar,
    ShieldAlert,
    Target,
    Clock3,
    Activity,
    Server,
    Zap,
} from "lucide-react";

import "./ThreatIntelCards.css";


function ThreatIntelCards({ summary }) {


    const totalAttacks =
        summary?.total_attacks || 0;


    const privateCount =
        summary?.network_type?.private || 0;


    const publicCount =
        summary?.network_type?.public || 0;


    const externalPercentage =
        totalAttacks > 0
            ? Math.round(
                (publicCount / totalAttacks) * 100
            )
            : 0;



    const cards = [

        {
            title: "Most Active IP",
            value:
                summary?.most_active_ip || "N/A",
            subtitle:
                "Primary attacker source",
            icon:
                <Radar size={24} />,
            color:
                "red",
        },


        {
            title: "Top Country",
            value:
                summary?.most_active_country || "Unknown",
            subtitle:
                "Highest attack origin",
            icon:
                <Globe size={24} />,
            color:
                "blue",
        },


        {
            title: "Target Endpoint",
            value:
                summary?.top_endpoint || "N/A",
            subtitle:
                "Most targeted resource",
            icon:
                <Target size={24} />,
            color:
                "purple",
        },


        {
            title: "Highest Risk",
            value:
                summary?.highest_risk_attack || "N/A",
            subtitle:
                "Detected attack pattern",
            icon:
                <ShieldAlert size={24} />,
            color:
                "orange",
        },


        {
            title: "Latest Attack",
            value:
                summary?.latest_attack
                    ? new Date(
                        summary.latest_attack
                    ).toLocaleString()
                    : "N/A",
            subtitle:
                "Most recent security event",
            icon:
                <Clock3 size={24} />,
            color:
                "yellow",
        },


        {
            title: "Network Activity",
            value:
                `${privateCount} Internal | ${publicCount} External`,
            subtitle:
                "Traffic classification",
            icon:
                <Server size={24} />,
            color:
                "green",
        },


        {
            title: "External Exposure",
            value:
                `${externalPercentage}%`,
            subtitle:
                "Public attack traffic",
            icon:
                <Zap size={24} />,
            color:
                "cyan",
        },

    ];



    return (

        <section className="intel-section">


            <div className="section-header">

                <h2>
                    Threat Intelligence
                </h2>

                <p>
                    Real-time intelligence extracted from security events
                </p>

            </div>



            <div className="intel-grid">


                {
                    cards.map((card)=>(

                        <div
                            key={card.title}
                            className={`intel-card ${card.color}`}
                        >


                            <div className="intel-icon">

                                {card.icon}

                            </div>



                            <div className="intel-content">


                                <span>
                                    {card.title}
                                </span>


                                <h3>
                                    {card.value}
                                </h3>


                                <p>
                                    {card.subtitle}
                                </p>


                            </div>


                        </div>

                    ))
                }


            </div>


        </section>

    );

}


export default ThreatIntelCards;