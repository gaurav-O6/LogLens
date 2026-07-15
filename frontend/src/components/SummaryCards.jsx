import {
    ShieldAlert,
    AlertTriangle,
    Globe,
    FileText,
} from "lucide-react";

function SummaryCards({ summary }) {
    const cards = [
        {
            title: "Total Attacks",
            value: summary?.total_attacks || 0,
            icon: <ShieldAlert size={22} />,
        },
        {
            title: "High Severity",
            value: summary?.severity?.High || 0,
            icon: <AlertTriangle size={22} />,
        },
        {
            title: "Unique IPs",
            value: Object.keys(summary?.source_ips || {}).length,
            icon: <Globe size={22} />,
        },
        {
            title: "Attack Types",
            value: Object.keys(summary?.attack_types || {}).length,
            icon: <FileText size={22} />,
        },
    ];

    return (
        <div className="summary-grid">
            {cards.map((card) => (
                <div className="summary-card" key={card.title}>
                    <div className="summary-icon">
                        {card.icon}
                    </div>

                    <div>
                        <p>{card.title}</p>
                        <h2>{card.value}</h2>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default SummaryCards;