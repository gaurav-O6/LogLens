import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from "recharts";


const COLORS = [
    "#ef4444",
    "#f59e0b",
    "#22c55e",
];



function SeverityChart({ severity }) {


    const data = Object.entries(severity || {}).map(
        ([name,value]) => ({
            name,
            value,
        })
    );



    return (

        <div className="chart-container">


            <div className="chart-header">

                <h2>
                    Severity Distribution
                </h2>

            </div>



            <div className="chart-body">


                <ResponsiveContainer width="100%" height={300}>


                    <PieChart>


                        <Pie

                            data={data}

                            dataKey="value"

                            nameKey="name"

                            cx="50%"

                            cy="45%"

                            outerRadius={90}

                            label={({name,value}) =>
                                `${name}: ${value}`
                            }

                            labelLine={false}

                        >


                            {
                                data.map((_,index)=>(

                                    <Cell

                                        key={index}

                                        fill={
                                            COLORS[
                                                index %
                                                COLORS.length
                                            ]
                                        }

                                    />

                                ))
                            }


                        </Pie>



                        <Tooltip

                            contentStyle={{
                                background:"#161b22",
                                border:"1px solid #30363d",
                                borderRadius:"8px",
                                color:"#ffffff"
                            }}

                        />



                        <Legend

                            wrapperStyle={{
                                color:"#8b949e",
                                fontSize:"13px"
                            }}

                        />


                    </PieChart>


                </ResponsiveContainer>


            </div>


        </div>

    );

}


export default SeverityChart;