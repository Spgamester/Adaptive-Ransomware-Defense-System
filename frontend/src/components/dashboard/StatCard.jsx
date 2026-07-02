import {
    ResponsiveContainer,
    AreaChart,
    Area
} from "recharts";


function StatCard({
    title,
    value,
    color,
    data
}) {
    return (
        <div className="stat-card">

            <div className="stat-top">

                <h4>{title}</h4>

                <span
                    style={{
                        color
                    }}
                >
                    ↗
                </span>

            </div>

            <h1
                style={{
                    color
                }}
            >
            {value ?? 0}
            </h1>

            <p className="trend">
            Live Endpoint Data
        </p>

            <div className="sparkline">

                <ResponsiveContainer
                    width="100%"
                    height={70}
                >

                    <AreaChart data={data}>

                        <Area
                            type="monotone"
                            dataKey="value"
                            stroke={color}
                            fill={color}
                            fillOpacity={0.25}
                        />

                    </AreaChart>

                </ResponsiveContainer>

            </div>

        </div>
    );
}

export default StatCard;