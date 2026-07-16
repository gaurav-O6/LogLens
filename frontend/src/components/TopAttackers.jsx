import "./TopAttackers.css";

function TopAttackers({ sourceIps }) {
    const attackers = Object.entries(sourceIps || {})
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);

    return (
        <div className="top-attackers">

            <div className="top-attackers-header">
                <h2>Top Attackers</h2>
                <p>Most active attacking IP addresses</p>
            </div>

            {
                attackers.length === 0 ? (
                    <div className="top-attackers-empty">
                        No attack data available.
                    </div>
                ) : (

                    <table className="top-attackers-table">

                        <thead>

                            <tr>
                                <th>Rank</th>
                                <th>IP Address</th>
                                <th>Attacks</th>
                            </tr>

                        </thead>

                        <tbody>

                            {
                                attackers.map(([ip, count], index) => (

                                    <tr key={ip}>

                                        <td>
                                            {index + 1}
                                        </td>

                                        <td className="attacker-ip">
                                            {ip}
                                        </td>

                                        <td>
                                            {count}
                                        </td>

                                    </tr>

                                ))
                            }

                        </tbody>

                    </table>

                )
            }

        </div>
    );
}

export default TopAttackers;