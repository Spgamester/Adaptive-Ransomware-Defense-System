import { useEffect, useState } from "react";
import API from "../api/config";

function MonitorPage() {


const [monitorData, setMonitorData] = useState({
    files_monitored: 0,
    processes_watching: 0,
    suspicious_events: 0,
    active_threats: 0
});

const [events, setEvents] = useState([]);
const [timeline, setTimeline] = useState([]);
const [monitorRunning, setMonitorRunning] = useState(false);
const [monitorPath, setMonitorPath] = useState(

    localStorage.getItem("monitorPath") ||

    ""

);

const loadMonitorData = async () => {

    try {

        const monitorRes = await fetch(`${API}/api/monitor`)
        

        const monitorJson =
            await monitorRes.json();

        setMonitorData(monitorJson);

        const eventsRes = await fetch(`${API}/api/live-events`)
        

        const eventsJson =
            await eventsRes.json();

        setEvents(eventsJson);

        const timelineRes = await fetch(`${API}/api/threat-timeline`)

        const timelineJson =
            await timelineRes.json();

        setTimeline(timelineJson);

        const statusRes = await fetch(`${API}/api/monitor-status`)
        

        const statusJson =
            await statusRes.json();

        setMonitorRunning(
            statusJson.running
        );

    } catch (error) {

        console.error(
            "Monitor Load Error:",
            error
        );

    }

};

useEffect(() => {

    loadMonitorData();

    const interval = setInterval(
        loadMonitorData,
        3000
    );

    return () => clearInterval(interval);

}, []);




const startMonitoring = async () => {

    try {

        if (!monitorPath.trim()) {

            alert("Please enter a folder path to monitor.");

            return;

        }

        await fetch(
            `${API}/api/start-monitoring`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({

                    path: monitorPath

                })
            }
        );

        setMonitorRunning(true);

        loadMonitorData();

    } catch (error) {

        console.error(
            "Start Monitor Error:",
            error
        );

    }

};

const stopMonitoring = async () => {

    try {

        await fetch(
            `${API}/api/stop-monitoring`,
            {
                method: "POST"
            }
        );

        setMonitorRunning(false);

        loadMonitorData();

    } catch (error) {

        console.error(
            "Stop Monitor Error:",
            error
        );

    }

};

return (

    <div>

        <h1 className="page-title">
            Live Monitor
        </h1>

        


        <div className="monitor-status-live">

            <span className="live-dot"></span>

            {monitorRunning
                ? "LIVE MONITORING"
                : "MONITORING STOPPED"}

        </div>

        <p className="page-subtitle">
            Real-time ransomware monitoring and system surveillance
        </p>

        

    

        <div className="monitor-path-container">

        <label className="monitor-path-label">
            Monitoring Path
        </label>

        <input
            type="text"
            placeholder="Enter folder path to monitor..."
            value={monitorPath}
            onChange={(e)=>{

                setMonitorPath(e.target.value);

                localStorage.setItem(

                    "monitorPath",

                    e.target.value

                );

            }}
            className="monitor-path-input"
        />

    </div>
    

        <div className="monitor-grid">

            <div className="monitor-card">
                <h4>Files Monitored</h4>
                <h2>
                    {monitorData.files_monitored}
                </h2>
            </div>

            <div className="monitor-card">
                <h4>Processes Watching</h4>
                <h2>
                    {monitorData.processes_watching}
                </h2>
            </div>

            <div className="monitor-card">
                <h4>Suspicious Events</h4>
                <h2 className="warning-text">
                    {monitorData.suspicious_events}
                </h2>
            </div>

            <div className="monitor-card">
                <h4>Active Threats</h4>
                <h2 className="danger-text">
                    {monitorData.active_threats}
                </h2>
            </div>

            <div className="monitor-card system-monitor-card">

                <h4>System Monitoring</h4>

                
                <h2
                    className={
                        monitorRunning
                            ? "status-green"
                            : "status-red"
                    }
                >
                    {monitorRunning
                        ? "ON"
                        : "OFF"}
                </h2>

                <div className="monitor-actions">

                        <button
                        className="monitor-start-btn"
                        onClick={startMonitoring}
                        disabled={monitorRunning}
                    >
                    
                        Start
                    </button>

                        <button
                        className="monitor-stop-btn"
                        onClick={stopMonitoring}
                        disabled={!monitorRunning}
                    >
                        Stop
                    </button>

                </div>

            </div>

        </div>

        <div className="event-panel">

            <h2>Live Event Stream</h2>

            <table>

                <thead>

                    <tr>
                        <th>Time</th>
                        <th>Source</th>
                        <th>Event</th>
                        <th>Severity</th>
                    </tr>

                </thead>

                <tbody>

                    {events.length > 0 ? (

                        events.map(
                            (event, index) => (

                                <tr key={index}>

                                    <td>
                                        {event.time}
                                    </td>

                                    <td>
                                        {event.source}
                                    </td>

                                    <td>
                                        {event.event}
                                    </td>

                                    <td>

                                        <span
                                            className={
                                                event.severity === "Critical"
                                                    ? "critical-badge"
                                                    : event.severity === "High"
                                                    ? "high-badge"
                                                    : "medium-badge"
                                            }
                                        >
                                            {event.severity}
                                        </span>

                                    </td>

                                </tr>

                            )
                        )

                    ) : (

                        <tr>

                            <td colSpan="4">
                                No events detected
                            </td>

                        </tr>

                    )}

                </tbody>

            </table>

        </div>

        <div className="timeline-panel">

            <h2>Threat Timeline</h2>

            <div className="timeline">

                {timeline.map(
                    (item, index) => (

                        <div
                            key={index}
                            className="timeline-item"
                        >

                            <div
                                className={`timeline-dot ${item.level}`}
                            ></div>

                            <div className="timeline-content">

                                <h4>
                                    {item.title}
                                </h4>

                                <p>
                                    {item.time}
                                </p>

                            </div>

                        </div>

                    )
                )}

            </div>

        </div>

    </div>

);


}

export default MonitorPage;
