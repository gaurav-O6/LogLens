function DetectionTable({
    detections = [],
    onSelect,
    selected
}) {


    const rows = Array.isArray(detections)
        ? detections
        : [];



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

                        {rows.length}

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


                    rows.length === 0 ?



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





                    rows.map((item)=>(



                        <tr



                            key={item.id}



                            className={

                                `clickable-row ${
                                    
                                    selected?.id === item.id

                                    ? "selected"

                                    : ""

                                }`

                            }



                            onClick={()=>


                                onSelect &&
                                onSelect(item)


                            }



                        >






                            <td>


                                {

                                    item.timestamp ||

                                    "-"

                                }


                            </td>









                            <td className="attack-name">


                                {

                                    item.attack_type ||

                                    "Unknown"

                                }


                            </td>









                            <td>



                                <span



                                    className={

                                        `severity-badge ${
                                            
                                            item.severity
                                            ?.toLowerCase()
                                            || ""

                                        }`

                                    }



                                >


                                    {

                                        item.severity ||

                                        "Unknown"

                                    }


                                </span>



                            </td>









                            <td className="ip-address">



                                <div>


                                    {

                                        item.source_ip ||

                                        "Unknown"


                                    }



                                </div>





                                {


                                    item.is_private_ip &&



                                    <small className="private-ip-badge">


                                        🏠 Internal IP


                                    </small>


                                }



                            </td>









                            <td>



                                {


                                item.city && item.country



                                ?



                                `${item.city}, ${item.country}`



                                :



                                "Unknown"



                                }



                            </td>









                            <td className="pattern-cell">


                                {


                                    item.matched_pattern ||

                                    "-"


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