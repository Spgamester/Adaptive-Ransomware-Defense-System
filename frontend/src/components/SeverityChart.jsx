import { useEffect, useState } from "react";

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
    "#FFD000",
    "#00E5FF"
];

function SeverityChart() {

    const [data, setData] = useState([]);

    useEffect(() => {

        const loadSeverity = () => {

            fetch("http://127.0.0.1:8000/api/dashboard")
                .then((res) => res.json())
                .then((dashboard) => {

                    const severity = dashboard.severity;

                    setData([

                        {
                            name: "Critical",
                            value: severity.critical
                        },

                        {
                            name: "High",
                            value: severity.high
                        },

                        {
                            name: "Medium",
                            value: severity.medium
                        },

                        {
                            name: "Low",
                            value: severity.low
                        }

                    ]);

                });

        };

        loadSeverity();

        const interval = setInterval(
            loadSeverity,
            2000
        );

        return () => clearInterval(interval);

    }, []);

    return (

        <div className="mini-panel">

            <h3>Detection Severity</h3>

            <ResponsiveContainer
                width="100%"
                height={280}
            >

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