import { useEffect, useState } from "react";
import SecurityScore from "./SecurityScore";
import StatCard from "./statcard";
import ThreatActivity from "./ThreatActivity";
import ThreatMap from "./ThreatMap";
import AttackVectorChart from "./AttackVectorChart";
import SeverityChart from "./SeverityChart";
import MitrePanel from "./MitrePanel";

function Dashboard() {

    const [stats, setStats] = useState({
        security_score: 0,
        threats_blocked: 0,
        files_scanned: 0,
        active_monitors: 0
    });


    const [alerts, setAlerts] = useState([]);

    useEffect(() => {

        fetch("http://127.0.0.1:8000/api/dashboard")
            .then((res) => res.json())
            .then((data) => {
                setStats(data);
            });

        fetch("http://127.0.0.1:8000/api/alerts")
            .then((res) => res.json())
            .then((data) => {
                setAlerts(data);
            });

    }, []);

    const threatData = [
        { value: 20 },
        { value: 40 },
        { value: 35 },
        { value: 70 },
        { value: 55 },
        { value: 90 },
        { value: 80 }
    ];

    const blockedData = [
        { value: 10 },
        { value: 20 },
        { value: 35 },
        { value: 25 },
        { value: 55 },
        { value: 75 },
        { value: 95 }
    ];

    const criticalData = [
        { value: 5 },
        { value: 8 },
        { value: 6 },
        { value: 12 },
        { value: 10 },
        { value: 18 },
        { value: 15 }
    ];

    const quarantineData = [
        { value: 1 },
        { value: 2 },
        { value: 3 },
        { value: 2 },
        { value: 4 },
        { value: 3 },
        { value: 5 }
    ];

    return (
        <>
            <div className="dashboard-grid">

                <SecurityScore score={stats.security_score} />

                <StatCard
                    title="Active Monitors"
                    value={stats.active_monitors}
                    color="#FF3B3B"
                    data={threatData}
                />

                <StatCard
                    title="Threats Blocked"
                    value={stats.threats_blocked}
                    color="#00D26A"
                    data={blockedData}
                />

                <StatCard
                    title="Critical Threats"
                    value="2"
                    color="#FF9D00"
                    data={criticalData}
                />

                <StatCard
                    title="Files Scanned"
                    value={stats.files_scanned.toLocaleString()}
                    color="#A855F7"
                    data={quarantineData}
                />

            </div>

            <div className="soc-panel">

                <ThreatActivity />

                <ThreatMap />

                <div className="bottom-grid">

                    <AttackVectorChart />

                    <SeverityChart />

                    <MitrePanel />

                </div>

                <h3>Recent Alerts</h3>

                <table>

                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Severity</th>
                            <th>Alert</th>
                            <th>Status</th>
                        </tr>
                    </thead>

                    <tbody>

                        {alerts.map((alert, index) => (

                            <tr key={index}>

                                <td>{alert.time}</td>

                                <td>
                                    <span className="critical-badge">
                                        {alert.severity}
                                    </span>
                                </td>

                                <td>{alert.alert}</td>

                                <td>
                                    <span className="blocked-badge">
                                        {alert.status}
                                    </span>
                                </td>

                            </tr>

                        ))}

                    </tbody>
                </table>

            </div>
        </>
    );
}

export default Dashboard;

