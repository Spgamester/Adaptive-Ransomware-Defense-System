import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip
} from "recharts";

const data = [
    { name: "Critical", value: 23 },
    { name: "High", value: 312 },
    { name: "Medium", value: 578 },
    { name: "Low", value: 216 }
];

const COLORS = [
    "#FF3B3B",
    "#FF9D00",
    "#FFD000",
    "#00E5FF"
];

function SeverityChart() {
    return (
        <div className="mini-panel">

            <h3>Detection Severity</h3>

            <ResponsiveContainer width="100%" height={280}>
                <PieChart>

                    <Pie
                        data={data}
                        dataKey="value"
                        innerRadius={70}
                        outerRadius={100}
                    >
                        {data.map((entry, index) => (
                            <Cell
                                key={index}
                                fill={COLORS[index]}
                            />
                        ))}
                    </Pie>

                    <Tooltip />

                </PieChart>
            </ResponsiveContainer>

        </div>
    );
}

export default SeverityChart;