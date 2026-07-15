import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
} from "recharts";


function DetectionTimeline({ detections }) {


    const timeline = {};



    detections.forEach((item)=>{


        if(!item.timestamp)
            return;


        const time = new Date(item.timestamp)
            .toLocaleTimeString([], {
                hour:"2-digit",
                minute:"2-digit"
            });


        timeline[time] =
            (timeline[time] || 0) + 1;


    });



    const data = Object.entries(timeline)
        .map(([time,count])=>({

            time,
            count

        }));



    return (

        <div className="chart-container">


            <div className="chart-header">

                <h2>
                    Detection Timeline
                </h2>

            </div>



            <ResponsiveContainer
                width="100%"
                height={300}
            >


                <LineChart
                    data={data}
                    margin={{
                        top:20,
                        right:20,
                        left:0,
                        bottom:20
                    }}
                >


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

                        cursor={false}

                        contentStyle={{

                            background:"#161b22",

                            border:"1px solid #30363d",

                            borderRadius:"8px",

                            color:"#ffffff"

                        }}

                    />



                    <Line

                        type="monotone"

                        dataKey="count"

                        stroke="#10a37f"

                        strokeWidth={3}

                        dot={{
                            r:5
                        }}

                        activeDot={false}

                    />


                </LineChart>


            </ResponsiveContainer>


        </div>

    );

}


export default DetectionTimeline;