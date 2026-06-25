import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip
} from "recharts";

const data = [
    { name: "Malicious Process", value: 42 },
    { name: "Encryption", value: 24 },
    { name: "API Abuse", value: 18 },
    { name: "Privilege Escalation", value: 10 },
    { name: "Other", value: 6 }
];

const COLORS = [
    "#FF3B3B",
    "#FF9D00",
    "#00E5FF",
    "#A855F7",
    "#94A3B8"
];

function AttackVectorChart() {
    return (
        <div className="mini-panel">

            <h3>Attack Vectors</h3>

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

export default AttackVectorChart;