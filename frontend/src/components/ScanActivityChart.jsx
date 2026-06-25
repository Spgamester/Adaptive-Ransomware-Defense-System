import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
} from "recharts";

const data = [
    { time: "09:00", scanned: 5000, detections: 2 },
    { time: "09:30", scanned: 12000, detections: 4 },
    { time: "10:00", scanned: 18000, detections: 7 },
    { time: "10:30", scanned: 26000, detections: 9 },
    { time: "11:00", scanned: 33000, detections: 14 },
    { time: "11:30", scanned: 41000, detections: 18 },
    { time: "12:00", scanned: 48000, detections: 23 }
];

function ScanActivityChart() {
    return (
        <div
            style={{
                width: "100%",
                height: "300px"
            }}
        >
            <ResponsiveContainer width="100%" height="100%">

                <LineChart data={data}>

                    <CartesianGrid
                        stroke="#13233E"
                        strokeDasharray="3 3"
                    />

                    <XAxis
                        dataKey="time"
                        stroke="#94A3B8"
                    />

                    <YAxis
                        yAxisId="left"
                        stroke="#FF3B3B"
                    />

                    <YAxis
                        yAxisId="right"
                        orientation="right"
                        stroke="#00E5FF"
                    />

                    <Tooltip
                        contentStyle={{
                            background: "#081224",
                            border: "1px solid #13233E",
                            borderRadius: "12px"
                        }}
                    />

                    <Legend />

                    <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="scanned"
                        stroke="#00E5FF"
                        strokeWidth={3}
                        dot={{ r: 4 }}
                    />

                    <Line
                        yAxisId="left"
                        type="monotone"
                        dataKey="detections"
                        stroke="#FF3B3B"
                        strokeWidth={3}
                        dot={{ r: 4 }}
                    />

                </LineChart>

            </ResponsiveContainer>
        </div>
    );
}

export default ScanActivityChart;