import { useEffect, useState } from "react";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid
} from "recharts";

function ThreatActivityChart() {

    const [data, setData] = useState([]);

    useEffect(() => {

        const loadTimeline = () => {

            fetch("http://127.0.0.1:8000/api/threat-timeline")
                .then(res => res.json())
                .then(events => {

                    const counts = {};

                    events.forEach(event => {

                        const t = event.time;

                        counts[t] = (counts[t] || 0) + 1;

                    });

                    const chartData = Object.keys(counts).map(time => ({

                        time,

                        threats: counts[time]

                    }));

                    setData(chartData);

                });

        };

        loadTimeline();

        const interval = setInterval(loadTimeline, 2000);

        return () => clearInterval(interval);

    }, []);

    return (

        <div className="chart-panel">

            <h3>Threat Activity</h3>

            <ResponsiveContainer
                width="100%"
                height={350}
            >

                <LineChart data={data}>

                    <CartesianGrid stroke="#13233E" />

                    <XAxis
                        dataKey="time"
                        stroke="#94A3B8"
                    />

                    <YAxis
                        stroke="#94A3B8"
                    />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="threats"
                        stroke="#FF3B3B"
                        strokeWidth={3}
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>

    );

}

export default ThreatActivityChart;