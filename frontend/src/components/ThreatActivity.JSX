import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid
} from "recharts";

const data = [
    { time: "00:00", malware: 120, encryption: 80, suspicious: 40 },
    { time: "03:00", malware: 180, encryption: 120, suspicious: 90 },
    { time: "06:00", malware: 240, encryption: 180, suspicious: 120 },
    { time: "09:00", malware: 320, encryption: 250, suspicious: 170 },
    { time: "12:00", malware: 410, encryption: 320, suspicious: 220 },
    { time: "15:00", malware: 500, encryption: 390, suspicious: 270 },
    { time: "18:00", malware: 620, encryption: 470, suspicious: 340 },
    { time: "21:00", malware: 760, encryption: 540, suspicious: 410 }
];

function ThreatActivityChart() {
    return (
        <div className="chart-panel">

            <h3>Threat Activity Over Time</h3>

            <ResponsiveContainer width="100%" height={350}>
                <LineChart data={data}>

                    <CartesianGrid stroke="#13233E" />

                    <XAxis
                        dataKey="time"
                        stroke="#94A3B8"
                    />

                    <YAxis stroke="#94A3B8" />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="malware"
                        stroke="#FF3B3B"
                        strokeWidth={3}
                    />

                    <Line
                        type="monotone"
                        dataKey="encryption"
                        stroke="#FF9D00"
                        strokeWidth={3}
                    />

                    <Line
                        type="monotone"
                        dataKey="suspicious"
                        stroke="#00E5FF"
                        strokeWidth={3}
                    />

                </LineChart>
            </ResponsiveContainer>

        </div>
    );
}

export default ThreatActivityChart;