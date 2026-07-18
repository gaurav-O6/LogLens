import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
    Area,
    AreaChart,
} from "recharts";



function DetectionTimeline({ timeline }) {


    const data = Object.entries(timeline || {})
        .map(([time, count]) => ({
            time,
            count
        }))
        .sort((a,b)=>
            a.time.localeCompare(b.time)
        );



    const totalEvents =
        data.reduce(
            (sum,item)=>sum+item.count,
            0
        );



    const peak =
        data.length
        ? Math.max(
            ...data.map(
                item=>item.count
            )
        )
        : 0;



    return (

        <div className="chart-container">


            <div className="chart-header">


                <div>

                    <h2>
                        Detection Timeline
                    </h2>


                    <p>
                        Attack activity trends over time
                    </p>

                </div>



                <div 
                    className="timeline-stats"
                    style={{
                        transform: "translateY(8px)"
                    }}
                >

                    <span>
                        Events: {totalEvents}
                    </span>


                    <span>
                        Peak: {peak}
                    </span>

                </div>


            </div>





            <ResponsiveContainer
                width="100%"
                height={320}
            >


                <AreaChart
                    data={data}
                >


                    <defs>

                        <linearGradient
                            id="attackGradient"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                        >

                            <stop
                                offset="0%"
                                stopColor="#ef4444"
                                stopOpacity={0.35}
                            />

                            <stop
                                offset="100%"
                                stopColor="#ef4444"
                                stopOpacity={0}
                            />

                        </linearGradient>


                    </defs>




                    <CartesianGrid
                        stroke="#30363d"
                        vertical={false}
                    />



                    <XAxis

                        dataKey="time"

                        stroke="#8b949e"

                        tick={{
                            fill:"#8b949e",
                            fontSize:12
                        }}

                        axisLine={false}

                        tickLine={false}

                    />




                    <YAxis

                        allowDecimals={false}

                        stroke="#8b949e"

                        tick={{
                            fill:"#8b949e",
                            fontSize:12
                        }}

                        axisLine={false}

                        tickLine={false}

                    />





                    <Tooltip

                        contentStyle={{

                            background:"#161b22",

                            border:"1px solid #30363d",

                            borderRadius:"10px",

                            color:"#ffffff"

                        }}

                    />





                    <Area

                        type="monotone"

                        dataKey="count"

                        stroke="#ef4444"

                        fill="url(#attackGradient)"

                        strokeWidth={3}

                    />



                    <Line

                        type="monotone"

                        dataKey="count"

                        stroke="#ef4444"

                        strokeWidth={2}

                        dot={{
                            r:4
                        }}

                    />



                </AreaChart>


            </ResponsiveContainer>


        </div>

    );

}


export default DetectionTimeline;