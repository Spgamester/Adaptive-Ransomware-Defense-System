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
    "#FFD000",
    "#00E5FF"
];

function SeverityChart() {

    const [data, setData] = useState([]);
    const hasData = data.some(item => item.value > 0);

    useEffect(() => {

        const loadSeverity = () => {

            fetch(`${API}/api/dashboard`)
                .then((res) => res.json())
                .then((dashboard) => {

                    if (!dashboard) return;

                    const severity = dashboard?.severity || {

                        low:0,

                        medium:0,

                        high:0,

                        critical:0

                    };

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

        {!hasData ? (

            <div className="empty-chart">

                <h2>🛡️</h2>

                <p>No threats detected</p>

                <small>Run a scan to populate the chart</small>

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

        )}

    </div>
    );

}

export default SeverityChart;