import { useEffect, useState } from "react";
import API from "../api/config";
import SecurityScore from "../components/dashboard/SecurityScore";
import StatCard from "../components/dashboard/StatCard";
import ThreatActivity from "../components/dashboard/ThreatActivity";
import ThreatMap from "../components/dashboard/ThreatMap";
import AttackVectorChart from "../components/dashboard/AttackVectorChart";
import SeverityChart from "../components/dashboard/SeverityChart";
import MitrePanel from "../components/dashboard/MitrePanel";
import IntelligencePanel from "../components/dashboard/IntelligencePanel";

import useIntelligence from "../hooks/useIntelligence";

function Dashboard() {

    const [stats, setStats] = useState({

        security_score: 100,

        detection_engines: 7,

        threats_blocked: 0,

        critical_threats: 0,

        files_scanned: 0,

        severity:{

            low:0,

            medium:0,

            high:0,

            critical:0

        }

    });


    const [alerts, setAlerts] = useState([]);
    const intelligence = useIntelligence();

    useEffect(() => {

        const loadDashboard = () => {

           

            fetch(`${API}/api/dashboard`)
                .then(res => res.json())
                .then(data => {

                    if (data && typeof data === "object") {
    
                        setStats(data);
    
                    }
    
                })
                .catch(err=>{
    
                    console.error(err);
    
                });

        };

        loadDashboard();

        const interval = setInterval(loadDashboard, 2000);

        return () => clearInterval(interval);

    }, []);
    useEffect(() => {

        const loadAlerts = () => {

            fetch(`${API}/api/alerts`)
                .then(res => res.json())
                .then(data => setAlerts(data));

        };

        loadAlerts();

        const interval = setInterval(loadAlerts, 2000);

        return () => clearInterval(interval);

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

                <SecurityScore score={stats?.security_score ?? 100}/>

                <StatCard
                    title="Detection Engines"
                    value={stats.detection_engines}
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
                value={stats.critical_threats}
                color="#FF9D00"
                data={criticalData}
            />

                <StatCard
                    title="Files Scanned"
                    value={(stats.files_scanned ?? 0).toLocaleString()}
                    color="#A855F7"
                    data={quarantineData}
                />

            </div>

            <IntelligencePanel intelligence={intelligence} />

            <div className="soc-panel">

                <ThreatActivity />

                <ThreatMap />

                <div className="bottom-grid">

                    <AttackVectorChart />

                    <SeverityChart />

                    <MitrePanel />

                </div>

                <h3>Recent Alerts</h3>

                <div className="recent-alert-scroll">

            

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

                    {
                    alerts.length > 0
                    ?

                    alerts.map((alert,index)=>(

                    <tr key={index}>

                    <td>{alert.time}</td>

                    <td>

                    <span
                    className={`severity-badge ${(alert.severity || "").toLowerCase()}`}
                    >

                    {alert.severity || "Unknown"}

                    </span>

                    </td>

                    <td>{alert.event}</td>

                    <td>

                    <span
                    className={`status-badge ${(alert.status || "").toLowerCase()}`}
                    >

                    {alert.status || "Unknown"}

                    </span>

                    </td>

                    </tr>

                    ))

                    :

                    <tr>

                    <td colSpan="4">

                    No recent alerts

                    </td>

                    </tr>

                    }

                    </tbody>
                    </table>
                </div>

            </div>
        </>
    );
}

export default Dashboard;

