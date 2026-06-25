import { useState, useEffect } from "react";
import ScanActivityChart from "./ScanActivityChart";

function ScanPage() {

    
const [scanPath, setScanPath] = useState(
    "C:/projects/Ransomwaredetectionproject/sample_data"
);

const [scanResult, setScanResult] = useState(null);

const [scanHistory, setScanHistory] = useState([]);

const [loading, setLoading] = useState(false);

const loadHistory = async () => {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/scan-history"
        );

        const data = await response.json();

        setScanHistory(data);

    } catch (error) {

        console.error(error);

    }

};

useEffect(() => {
    loadHistory();
}, []);

const runScan = async () => {

    setLoading(true);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/scan",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    path: scanPath
                })
            }
        );

        const data = await response.json();

        setScanResult(data);

        await loadHistory();

    } catch (error) {

        console.error(error);

    }

    setLoading(false);
};

return (

    <div className="scan-page">

        <h1 className="page-title">
            Scan Center
        </h1>

        <p className="page-subtitle">
            Intelligence-driven system scanning and detection
        </p>

        <div className="scan-search">

            <input
                type="text"
                value={scanPath}
                onChange={(e) =>
                    setScanPath(e.target.value)
                }
                placeholder="Enter folder path..."
                className="scan-input"
            />

            <button
                className="save-btn"
                onClick={runScan}
            >
                {loading ? "Scanning..." : "Start Scan"}
            </button>

        </div>

        <div className="scan-top-grid">

            <div className="scan-card">
                <h4>Scan Status</h4>

                <h2
                    className={
                        scanResult?.status ===
                        "RANSOMWARE DETECTED"
                            ? "status-red"
                            : "status-blue"
                    }
                >
                    {scanResult
                        ? scanResult.status
                        : "READY"}
                </h2>
            </div>

            <div className="scan-card">
                <h4>Scan Type</h4>
                <h2>ML + Entropy</h2>
            </div>

            <div className="scan-card">
                <h4>Objects Scanned</h4>

                <h2>
                    {scanResult
                        ? scanResult.files_scanned
                        : 0}
                </h2>
            </div>

            <div className="scan-card">
                <h4>Threats Found</h4>

                <h2 className="status-red">
                    {scanResult
                        ? scanResult.threat_count
                        : 0}
                </h2>
            </div>

            <div className="scan-card">
                <h4>Scan Duration</h4>

                <h2>
                    {scanResult
                        ? `${scanResult.scan_time}s`
                        : "0s"}
                </h2>
            </div>

        </div>

        <div className="scan-report-grid">

            <div className="scan-panel">

                <div className="scan-panel">

                    
                    <h3>Threat Analysis Report</h3>

                    {scanResult ? (

                        <div className="report-box">

                            <div className="report-item">
                                <span>Status</span>
                                <strong
                                    className={
                                        scanResult.status === "RANSOMWARE DETECTED"
                                            ? "danger-text"
                                            : "success-text"
                                    }
                                >
                                    <strong className="danger-text">
                                        {scanResult.status}
                                    </strong>
                                </strong>
                            </div>

                            <div className="report-item">
                                <span>Files Scanned</span>
                                <strong>{scanResult?.files_scanned?.toLocaleString()}</strong>
                            </div>

                            <div className="report-item">
                                <span>Threats Found</span>
                                <strong className="danger-text">
                                    {scanResult.threat_count}
                                </strong>
                            </div>

                            <div className="report-item">
                                <span>Scan Duration</span>
                                <strong>{scanResult.scan_time}s</strong>
                            </div>

                        </div>

                    ) : (

                        <div className="report-empty">
                            No scan executed yet.
                        </div>

                    )}
                    

                </div>

            </div>

            <div className="scan-panel">

                <h3>Recent Scans</h3>

                <table>

                    <thead>

                        <tr>
                            <th>Time</th>
                            <th>Status</th>
                            <th>Files</th>
                            <th>Threats</th>
                        </tr>

                    </thead>

                    <tbody>

                        <tbody>

                            
                            {scanHistory.length > 0 ? (

                                scanHistory.map((scan, index) => (

                                    <tr key={index}>

                                        <td>{scan.time}</td>

                                        <td
                                            className={
                                                scan.status === "RANSOMWARE DETECTED"
                                                    ? "danger-text"
                                                    : "success-text"
                                            }
                                        >
                                            {scan.status}
                                        </td>

                                        <td>{scan.files_scanned}</td>

                                        <td>{scan.threat_count}</td>

                                    </tr>

                                ))

                            ) : (

                                <tr>
                                    <td colSpan="4">
                                        No history available
                                    </td>
                                </tr>

                            )}
                            

                        </tbody>


                    </tbody>

                </table>

            </div>

        </div>

        <div className="scan-middle-grid">

            <div className="scan-panel">

                <h3>Scan Coverage</h3>

                <div className="coverage-ring">

                    <div className="coverage-inner">

                        <h2>4.7M</h2>

                        <span>Total Objects</span>

                    </div>

                </div>

            </div>

            <div className="scan-panel">

                <h3>Scan Activity</h3>

                <ScanActivityChart />

            </div>

        </div>

        <div className="engine-grid">

            <div className="scan-panel">

                <h3>Active Engines</h3>

                <div className="engine-card">
                    <h4>Behavior Engine</h4>
                    <p>Version 6.2.1</p>
                </div>

                <div className="engine-card">
                    <h4>Heuristic Engine</h4>
                    <p>Version 4.1.8</p>
                </div>

                <div className="engine-card">
                    <h4>ML Engine</h4>
                    <p>Random Forest</p>
                </div>

            </div>

            <div className="scan-panel">

                <div className="scan-panel">

                    
                    <h3>Detected Files</h3>

                    {scanResult?.details?.length ? (

                        <table>

                            <thead>
                                <tr>
                                    <th>File</th>
                                    <th>Detection Reason</th>
                                </tr>
                            </thead>

                            <tbody>

                                {scanResult.details.map((item, index) => (

                                    <tr key={index}>

                                        <td>
                                            {item.file.split("\\").pop()}
                                        </td>

                                        <td>{item.reason}</td>

                                    </tr>

                                ))}

                            </tbody>

                        </table>

                    ) : (

                        <div className="report-empty">
                            No threats detected.
                        </div>

                    )}
                    

                </div>


            </div>

        </div>

    </div>

);


}

export default ScanPage;
