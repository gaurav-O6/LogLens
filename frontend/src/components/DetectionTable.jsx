function DetectionTable({ detections }) {

    return (

        <div className="table-container">


            <div className="table-header">


                <div className="table-title">

                    <h2>
                        Recent Threats
                    </h2>

                    <p>
                        Latest detected security events
                    </p>

                </div>



                <div className="detection-count">

                    <strong>
                        {detections.length}
                    </strong>

                    <span>
                        Detections
                    </span>

                </div>


            </div>




            <div className="table-wrapper">


                <table>


                    <thead>

                        <tr>

                            <th>
                                Attack Type
                            </th>

                            <th>
                                Severity
                            </th>

                            <th>
                                Source IP
                            </th>

                            <th>
                                Pattern
                            </th>

                        </tr>

                    </thead>



                    <tbody>


                        {
                            detections.length === 0 ? (

                                <tr>

                                    <td
                                        colSpan="4"
                                        className="empty-table"
                                    >

                                        No threats detected

                                    </td>

                                </tr>


                            ) : (


                                detections.map((item, index) => (

                                    <tr key={index}>


                                        <td className="attack-name">

                                            {item.attack_type}

                                        </td>



                                        <td>

                                            <span
                                                className={`severity-badge ${item.severity.toLowerCase()}`}
                                            >

                                                {item.severity}

                                            </span>

                                        </td>



                                        <td className="ip-address">

                                            {item.source_ip}

                                        </td>



                                        <td className="pattern-cell">

                                            {item.matched_pattern || "-"}

                                        </td>


                                    </tr>

                                ))

                            )
                        }


                    </tbody>


                </table>


            </div>


        </div>

    );

}


export default DetectionTable;