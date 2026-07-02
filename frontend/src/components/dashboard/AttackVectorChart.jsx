import { useEffect, useState } from "react";
import API from "../../api/config";
import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip
} from "recharts";

const COLORS = [
    "#FF3B3B",
    "#FF9D00",
    "#00E5FF",
    "#A855F7",
    "#94A3B8"
];

function AttackVectorChart() {

    const [data, setData] = useState([]);
    const hasData = data.length > 0;

    useEffect(() => {

        const loadAttackVectors = () => {

            fetch(`${API}/api/attack-vectors`)
                .then((res) => res.json())
                .then((vectors) => {

                    setData(vectors);

                })
                .catch((err) => {

                    console.error(err);

                });

        };

        loadAttackVectors();

        const interval = setInterval(
            loadAttackVectors,
            2000
        );

        return () => clearInterval(interval);

    }, []);

    return (

        <div className="mini-panel">

        <h3>Detection Techniques</h3>

        {!hasData ? (

            <div className="empty-chart">

                <h2>⚙️</h2>

                <p>No detections yet</p>

                <small>Detection engines are idle</small>

            </div>

        ) : (

            <ResponsiveContainer
                width="100%"
                height={280}
            >

                <PieChart>

                    <Pie
                        data={data}
                        dataKey="value"
                        nameKey="name"
                        innerRadius={70}
                        outerRadius={100}
                    >

                        {data.map((entry, index) => (

                            <Cell
                                key={index}
                                fill={COLORS[index % COLORS.length]}
                            />

                        ))}

                    </Pie>

                    <Tooltip />

                </PieChart>

            </ResponsiveContainer>

        )}

    </div>

    );

}

export default AttackVectorChart;