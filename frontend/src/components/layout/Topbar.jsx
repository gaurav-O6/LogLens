import {
    Activity,
    Database,
    Server,
} from "lucide-react";

import { useLocation } from "react-router-dom";

import "./topbar.css";

const pageInfo = {
    "/": {
        title: "Security Overview",
        subtitle: "Real-time log analysis and threat monitoring",
    },

    "/upload": {
        title: "Upload Security Logs",
        subtitle: "Upload and analyze Apache / Nginx log files",
    },

    "/threats": {
        title: "Threat Center",
        subtitle: "Investigate detected attacks and security incidents",
    },

    "/analytics": {
        title: "Security Analytics",
        subtitle: "Visualize attack trends and threat intelligence",
    },

    "/history": {
        title: "Analysis History",
        subtitle: "Review previously processed log analyses",
    },
};

function Topbar() {

    const location = useLocation();

    const currentPage =
        pageInfo[location.pathname] || {
            title: "LogLens",
            subtitle: "Security Operations Dashboard",
        };

    return (

        <header className="topbar">

            <div>

                <h1>
                    {currentPage.title}
                </h1>

                <p>
                    {currentPage.subtitle}
                </p>

            </div>

            <div className="status-group">

                <div className="status-badge online">

                    <Activity size={15} />

                    Monitoring

                </div>

                <div className="status-badge">

                    <Database size={15} />

                    PostgreSQL

                </div>

                <div className="status-badge">

                    <Server size={15} />

                    Backend

                </div>

            </div>

        </header>

    );

}

export default Topbar;