function DetectionTable({
    detections,
    onSelect
}) {


    return (

        <div className="table-container">


            <div className="table-header">


                <div className="table-title">

                    <h2>
                        Threat Events
                    </h2>


                    <p>
                        Security incidents detected from logs
                    </p>

                </div>



                <div className="detection-count">

                    <strong>
                        {detections.length}
                    </strong>


                    <span>
                        Events
                    </span>

                </div>


            </div>




            <div className="table-wrapper">


                <table>


                    <thead>

                        <tr>

                            <th>
                                Time
                            </th>


                            <th>
                                Attack
                            </th>


                            <th>
                                Severity
                            </th>


                            <th>
                                Source IP
                            </th>


                            <th>
                                Location
                            </th>


                            <th>
                                Pattern
                            </th>

                        </tr>

                    </thead>



                    <tbody>


                    {
                        detections.length === 0

                        ?

                        (

                            <tr>

                                <td
                                    colSpan="6"
                                    className="empty-table"
                                >

                                    No threats detected

                                </td>


                            </tr>

                        )


                        :


                        detections.map((item)=>(


                            <tr

                                key={item.id}

                                className="clickable-row"

                                onClick={() =>
                                    onSelect(item)
                                }

                            >


                                <td>

                                    {
                                        item.timestamp || "-"
                                    }

                                </td>



                                <td className="attack-name">

                                    {
                                        item.attack_type
                                    }

                                </td>



                                <td>


                                    <span

                                        className={
                                            `severity-badge ${
                                                item.severity?.toLowerCase()
                                            }`
                                        }

                                    >

                                        {
                                            item.severity
                                        }

                                    </span>


                                </td>



                                <td className="ip-address">

                                    {
                                        item.source_ip
                                    }

                                </td>




                                <td>


                                    {
                                        item.city &&
                                        item.country

                                        ?

                                        `${item.city}, ${item.country}`

                                        :

                                        "Unknown"

                                    }


                                </td>




                                <td className="pattern-cell">

                                    {
                                        item.matched_pattern || "-"
                                    }

                                </td>



                            </tr>


                        ))

                    }


                    </tbody>


                </table>


            </div>


        </div>

    );

}


export default DetectionTable;