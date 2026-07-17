import "./TopAttackers.css";


function TopAttackers({ sourceIps }) {


    const attackers = Object.entries(sourceIps || {})
        .sort((a,b)=>b[1]-a[1])
        .slice(0,10);



    const maxAttacks =
        attackers.length > 0
            ? attackers[0][1]
            : 1;



    return (

        <div className="top-attackers">


            <div className="top-attackers-header">

                <div>

                    <h2>
                        Top Attackers
                    </h2>

                    <p>
                        Most active malicious sources detected
                    </p>

                </div>

            </div>




            {
                attackers.length === 0 ?


                (

                    <div className="top-attackers-empty">

                        No attack data available.

                    </div>

                )


                :


                (

                <div className="attacker-list">


                {
                    attackers.map(
                        ([ip,count],index)=>(


                        <div
                            className={`attacker-row ${index===0 ? "top-threat":""}`}
                            key={ip}
                        >



                            <div className="attacker-rank">

                                {index+1}

                            </div>




                            <div className="attacker-info">


                                <span className="attacker-ip">

                                    {ip}

                                </span>



                                <div className="attack-bar">

                                    <div
                                        style={{
                                            width:`${(count/maxAttacks)*100}%`
                                        }}
                                    />

                                </div>


                            </div>




                            <div className="attack-count">

                                <strong>
                                    {count}
                                </strong>


                                <span>
                                    attacks
                                </span>

                            </div>



                        </div>


                        )

                    )
                }


                </div>

                )

            }


        </div>

    );

}


export default TopAttackers;