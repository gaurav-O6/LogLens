import { useState } from "react";


function DetectionTable({ detections }) {

    const [selectedDetection, setSelectedDetection] = useState(null);


    return (

        <>

        <div className="table-container">

            <div className="table-header">

                <div className="table-title">

                    <h2>Threat Investigations</h2>

                    <p>
                        Search and investigate detected threats
                    </p>

                </div>


                <div className="detection-count">

                    <strong>{detections.length}</strong>

                    <span>Detections</span>

                </div>

            </div>



            <div className="table-wrapper">

                <table>

                    <thead>

                        <tr>

                            <th>Timestamp</th>
                            <th>Attack Type</th>
                            <th>Severity</th>
                            <th>Source IP</th>
                            <th>Location</th>
                            <th>Pattern</th>

                        </tr>

                    </thead>


                    <tbody>

                    {
                        detections.length === 0 ?

                        (
                            <tr>
                                <td
                                    colSpan="6"
                                    className="empty-table"
                                >
                                    No threats found
                                </td>
                            </tr>
                        )

                        :

                        detections.map((item) => (

                            <tr
                                key={item.id}
                                onClick={() =>
                                    setSelectedDetection(item)
                                }
                                className="clickable-row"
                            >

                                <td>
                                    {item.timestamp || "-"}
                                </td>


                                <td className="attack-name">
                                    {item.attack_type}
                                </td>


                                <td>

                                    <span
                                        className={`severity-badge ${item.severity?.toLowerCase()}`}
                                    >
                                        {item.severity}
                                    </span>

                                </td>


                                <td className="ip-address">
                                    {item.source_ip}
                                </td>


                                <td>

                                    {
                                        item.city && item.country ?

                                        `${item.city}, ${item.country}`

                                        :

                                        "-"
                                    }

                                </td>


                                <td className="pattern-cell">
                                    {item.matched_pattern || "-"}
                                </td>


                            </tr>

                        ))

                    }

                    </tbody>


                </table>


            </div>


        </div>



        {
            selectedDetection && (

                <div className="investigation-panel">

                    <div className="panel-header">

                        <h2>
                            Threat Details
                        </h2>


                        <button
                            onClick={() =>
                                setSelectedDetection(null)
                            }
                        >
                            ×
                        </button>

                    </div>


                    <div className="panel-content">


                        <p>
                            <strong>Attack:</strong>
                            {" "}
                            {selectedDetection.attack_type}
                        </p>


                        <p>
                            <strong>Severity:</strong>
                            {" "}
                            {selectedDetection.severity}
                        </p>


                        <p>
                            <strong>Source IP:</strong>
                            {" "}
                            {selectedDetection.source_ip}
                        </p>


                        <p>
                            <strong>Location:</strong>
                            {" "}
                            {
                                selectedDetection.city &&
                                selectedDetection.country
                                ?
                                `${selectedDetection.city}, ${selectedDetection.country}`
                                :
                                "Unknown"
                            }
                        </p>


                        <p>
                            <strong>Coordinates:</strong>
                            {" "}
                            {
                                selectedDetection.latitude &&
                                selectedDetection.longitude
                                ?
                                `${selectedDetection.latitude}, ${selectedDetection.longitude}`
                                :
                                "Unavailable"
                            }
                        </p>


                        <p>
                            <strong>Request:</strong>
                            {" "}
                            {selectedDetection.request_path || "-"}
                        </p>


                        <p>
                            <strong>Method:</strong>
                            {" "}
                            {selectedDetection.http_method || "-"}
                        </p>


                        <p>
                            <strong>Status:</strong>
                            {" "}
                            {selectedDetection.status_code || "-"}
                        </p>


                        <p>
                            <strong>Pattern:</strong>
                            {" "}
                            {selectedDetection.matched_pattern || "-"}
                        </p>


                        <p>
                            <strong>Raw Log:</strong>
                        </p>


                        <pre>
                            {selectedDetection.raw_log || "-"}
                        </pre>


                    </div>


                </div>

            )
        }


        </>

    );

}


export default DetectionTable;