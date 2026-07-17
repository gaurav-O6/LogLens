import {
    Globe,
    Radar,
    ShieldAlert,
    Target,
    Clock3,
    Activity,
} from "lucide-react";

import "./ThreatIntelCards.css";

function ThreatIntelCards({ summary }) {

    const cards = [

        {
            title: "Most Active IP",
            value: summary?.most_active_ip || "N/A",
            icon: <Radar size={22} />,
        },

        {
            title: "Top Country",
            value: summary?.most_active_country || "Unknown",
            icon: <Globe size={22} />,
        },

        {
            title: "Target Endpoint",
            value: summary?.top_endpoint || "N/A",
            icon: <Target size={22} />,
        },

        {
            title: "Highest Risk",
            value: summary?.highest_risk_attack || "N/A",
            icon: <ShieldAlert size={22} />,
        },

        {
            title: "Latest Attack",
            value: summary?.latest_attack
                ? new Date(summary.latest_attack).toLocaleString()
                : "N/A",
            icon: <Clock3 size={22} />,
        },

        {
            title: "Total Attacks",
            value: summary?.total_attacks || 0,
            icon: <Activity size={22} />,
        },

    ];


    return (

        <section className="intel-section">

            <div className="section-header">

                <h2>
                    Threat Intelligence
                </h2>

                <p>
                    Live intelligence generated from uploaded security logs
                </p>

            </div>


            <div className="intel-grid">

                {

                    cards.map((card) => (

                        <div
                            className="intel-card"
                            key={card.title}
                        >

                            <div className="intel-icon">

                                {card.icon}

                            </div>

                            <div>

                                <span>

                                    {card.title}

                                </span>

                                <h3>

                                    {card.value}

                                </h3>

                            </div>

                        </div>

                    ))

                }

            </div>

        </section>

    );

}

export default ThreatIntelCards;