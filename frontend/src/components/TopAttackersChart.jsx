import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
} from "recharts";


function TopAttackersChart({ sourceIps }) {

    const data = Object.entries(sourceIps || {})
        .map(([ip, count]) => ({
            ip,
            count,
        }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);



    return (

        <div className="chart-container">

            <div className="chart-header">

                <h2>
                    Top Attacking IPs
                </h2>

            </div>


            <ResponsiveContainer width="100%" height={300}>

                <BarChart
                    data={data}
                    layout="vertical"
                    margin={{
                        top: 20,
                        right: 30,
                        left: 30,
                        bottom: 20,
                    }}
                >

                    <CartesianGrid
                        stroke="#30363d"
                        horizontal={false}
                    />


                    <XAxis
                        type="number"
                        stroke="#8b949e"
                        tick={{
                            fill:"#8b949e",
                            fontSize:12
                        }}
                        axisLine={false}
                        tickLine={false}
                    />


                    <YAxis
                        type="category"
                        dataKey="ip"
                        width={100}
                        stroke="#8b949e"
                        tick={{
                            fill:"#8b949e",
                            fontSize:12
                        }}
                        axisLine={false}
                        tickLine={false}
                    />


                    <Tooltip

                        cursor={false}

                        contentStyle={{
                            background:"#161b22",
                            border:"1px solid #30363d",
                            borderRadius:"8px",
                            color:"#ffffff"
                        }}

                    />


                    <Bar

                        dataKey="count"

                        fill="#6366f1"

                        radius={[0,6,6,0]}

                        barSize={18}

                        activeBar={false}

                    />


                </BarChart>

            </ResponsiveContainer>


        </div>

    );

}


export default TopAttackersChart;