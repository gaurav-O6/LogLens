import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
} from "recharts";

function AttackChart({ attacks }) {

    const data = Object.entries(attacks || {}).map(
        ([name, value]) => ({
            displayName: name.replace(" (XSS)", ""),
            originalName: name,
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

            <div className="chart-body">

                <ResponsiveContainer width="100%" height={340}>

                    <BarChart

                        data={data}

                        margin={{
                            top: 25,
                            right: 20,
                            left: 0,
                            bottom: 30,
                        }}

                    >

                        <CartesianGrid

                            strokeDasharray="3 3"

                            vertical={false}

                        />

                        <XAxis

                            dataKey="displayName"

                            interval={0}

                            tick={{
                                fill: "#8b949e",
                                fontSize: 11
                            }}

                            axisLine={false}

                            tickLine={false}

                        />

                        <YAxis

                            allowDecimals={false}

                            tick={{
                                fill: "#8b949e",
                                fontSize: 12
                            }}

                            axisLine={false}

                            tickLine={false}

                        />

                        <Tooltip

                            labelFormatter={(_, payload) =>
                                payload?.[0]?.payload?.originalName || ""
                            }

                            cursor={{
                                fill: "rgba(255,255,255,0.05)"
                            }}

                            contentStyle={{
                                background: "#161b22",
                                border: "1px solid #30363d",
                                borderRadius: "8px",
                                color: "#ffffff"
                            }}

                        />

                        <Bar

                            dataKey="value"

                            fill="#10a37f"

                            radius={[6, 6, 0, 0]}

                        />

                    </BarChart>

                </ResponsiveContainer>

            </div>

        </div>

    );

}

export default AttackChart;