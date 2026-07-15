import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";


function AttackChart({ attacks }) {

    const data = Object.entries(attacks || {}).map(
        ([name, value]) => ({
            name,
            value,
        })
    );


    return (

        <div className="chart-container">

            <div className="chart-header">

                <h2>
                    Attack Types
                </h2>

            </div>



            <ResponsiveContainer width="100%" height={280}>

                <BarChart
                    data={data}
                    margin={{
                        top:20,
                        right:20,
                        left:0,
                        bottom:20
                    }}
                >

                    <XAxis
                        dataKey="name"
                        stroke="#8b949e"
                        tick={{
                            fill:"#8b949e",
                            fontSize:12
                        }}
                        axisLine={false}
                        tickLine={false}
                    />


                    <YAxis
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

                        dataKey="value"

                        fill="#10a37f"

                        radius={[6,6,0,0]}

                        activeBar={false}

                    />


                </BarChart>


            </ResponsiveContainer>


        </div>

    );

}


export default AttackChart;