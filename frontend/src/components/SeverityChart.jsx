import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

const COLORS = [
    "#ef4444",
    "#f59e0b",
    "#22c55e",
];

function SeverityChart({ severity }) {
    const data = Object.entries(severity || {}).map(([name, value]) => ({
        name,
        value,
    }));

    return (
        <div className="chart-container">
            <div className="chart-header">
                <h2>Severity Distribution</h2>
            </div>

            <ResponsiveContainer width="100%" height={300}>
                <PieChart>

                    <Pie
                        data={data}
                        dataKey="value"
                        nameKey="name"
                        outerRadius={95}
                    >
                        {data.map((_, index) => (
                            <Cell
                                key={index}
                                fill={COLORS[index % COLORS.length]}
                            />
                        ))}
                    </Pie>

                    <Tooltip
                        contentStyle={{
                            background: "#262626",
                            border: "1px solid #404040",
                            borderRadius: "8px",
                            color: "#fff",
                        }}
                    />

                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}

export default SeverityChart;