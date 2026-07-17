import { Link } from "react-router-dom";
import {
    ShieldAlert,
    MapPin,
    Clock3,
    ArrowRight,
} from "lucide-react";

import "./RecentThreatFeed.css";

function RecentThreatFeed({ detections = [] }) {

    const recentThreats = [...detections]
        .slice(0, 10);

    return (

        <div className="recent-feed">

            <div className="recent-feed-header">

                <div>

                    <h2>
                        Recent Threat Feed
                    </h2>

                    <p>
                        Latest detected security events
                    </p>

                </div>

                <Link
                    to="/threats"
                    className="view-all-link"
                >
                    View All

                    <ArrowRight size={16}/>
                </Link>

            </div>


            {
                recentThreats.length === 0 ?

                (

                    <div className="feed-empty">

                        No threats detected.

                    </div>

                )

                :

                (

                    <div className="feed-list">

                        {
                            recentThreats.map((item) => (

                                <div
                                    key={item.id}
                                    className="feed-card"
                                >

                                    <div className="feed-icon">

                                        <ShieldAlert size={20}/>

                                    </div>


                                    <div className="feed-content">

                                        <div className="feed-top">

                                            <h3>

                                                {
                                                    item.attack_type
                                                }

                                            </h3>

                                            <span
                                                className={`severity-badge ${item.severity?.toLowerCase()}`}
                                            >
                                                {
                                                    item.severity
                                                }
                                            </span>

                                        </div>


                                        <p className="feed-ip">

                                            {
                                                item.source_ip
                                            }

                                        </p>


                                        <div className="feed-meta">

                                            <span>

                                                <MapPin size={14}/>

                                                {

                                                    item.city && item.country

                                                    ?

                                                    `${item.city}, ${item.country}`

                                                    :

                                                    "Unknown Location"

                                                }

                                            </span>


                                            <span>

                                                <Clock3 size={14}/>

                                                {

                                                    item.timestamp || "-"

                                                }

                                            </span>

                                        </div>

                                    </div>

                                </div>

                            ))
                        }

                    </div>

                )

            }

        </div>

    );

}

export default RecentThreatFeed;