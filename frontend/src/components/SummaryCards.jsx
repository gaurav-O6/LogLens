import {
    ShieldAlert,
    AlertTriangle,
    Globe,
    Radar,
    TrendingUp,
} from "lucide-react";

function SummaryCards({ summary }) {

    const cards = [

        {
            title: "Detected Threats",
            value: summary?.total_attacks || 0,
            subtitle: "Security events identified",
            icon: <ShieldAlert size={24} />,
            color: "red",
        },

        {
            title: "Critical Threats",
            value: summary?.severity?.High || 0,
            subtitle: "High severity incidents",
            icon: <AlertTriangle size={24} />,
            color: "orange",
        },

        {
            title: "Attack Sources",
            value: Object.keys(summary?.source_ips || {}).length,
            subtitle: "Unique attacker IPs",
            icon: <Globe size={24} />,
            color: "blue",
        },

        {
            title: "Threat Signatures",
            value: Object.keys(summary?.attack_types || {}).length,
            subtitle: "Attack categories detected",
            icon: <Radar size={24} />,
            color: "green",
        },

    ];


    return (

        <div className="summary-grid">

            {

                cards.map((card)=>(

                    <div
                        key={card.title}
                        className={`summary-card ${card.color}`}
                    >

                        <div className="summary-icon">

                            {card.icon}

                        </div>


                        <div className="summary-content">

                            <div className="summary-top">

                                <p>

                                    {card.title}

                                </p>

                                <TrendingUp
                                    size={16}
                                    className="summary-trend"
                                />

                            </div>


                            <h2>

                                {card.value.toLocaleString()}

                            </h2>


                            <span>

                                {card.subtitle}

                            </span>

                        </div>

                    </div>

                ))

            }

        </div>

    );

}

export default SummaryCards;