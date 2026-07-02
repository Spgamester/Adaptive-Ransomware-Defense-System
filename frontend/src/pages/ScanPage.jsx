import { useState, useEffect } from "react";
import ScanActivityChart from "../components/dashboard/ScanActivityChart";
import API from "../api/config";
function ScanPage() {

    
    const [scanPath, setScanPath] = useState(

        localStorage.getItem("scanPath") ||
    
        "C:/projects/Ransomwaredetectionproject/sample_data"
    
    );

const [scanResult, setScanResult] = useState(null);

const [scanHistory, setScanHistory] = useState([]);

const [loading, setLoading] = useState(false);

const [progress, setProgress] = useState({

    running:false,

    files_scanned:0,

    total_files:0,

    current_file:"",

    elapsed:0

});

const loadHistory = async () => {

    try {

        const response = await fetch(`${API}/api/scan-history`);

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
            `${API}/api/scan`,
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

useEffect(()=>{

    const loadProgress = async()=>{

        const res = await fetch(
            `${API}/api/scan-progress`
        );

        const data = await res.json();

        setProgress(data);

    };

    const interval = setInterval(
        loadProgress,
        500
    );

    return ()=>clearInterval(interval);

},[]);

const percentage =
progress.total_files > 0
?
(progress.files_scanned /
progress.total_files) * 100
:
0;

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
                onChange={(e)=>{

                    setScanPath(e.target.value);

                    localStorage.setItem(

                        "scanPath",

                        e.target.value

                    );

                }}
                placeholder="Enter folder path..."
                className="scan-input"
            />

            <button
                className="save-btn"
                onClick={runScan}
            >
                {loading ? "Scanning..." : "Start Scan"}
            </button>

            {progress.running && (

                <div className="scan-progress-panel">
    
                <h4>Scanning...</h4>
    
                <div className="progress-bar">
    
                <div
                className="progress-fill"
                style={{
    
                width:`${percentage}%`
    
                }}
                ></div>
    
                </div>
    
                <p>
    
                {progress.files_scanned} /
                {progress.total_files}
    
                files
    
                </p>
    
                <p>
    
                Current:
    
                {progress.current_file}
    
                </p>
    
                <p>
    
                Elapsed:
    
                {progress.elapsed}s
    
                </p>
    
                </div>
    
                )}

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
                <h4>Detection Engines</h4>
                <h2>7 Engines</h2>
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

                <div className="scan-panel recent-scan-panel">
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


                </table>

            </div>

        </div>

        <div className="scan-middle-grid">

            <div className="scan-panel">

                <h3>Scan Coverage</h3>

                <div className="coverage-ring">

                    <div className="coverage-inner">

                        <h2>

                        {scanResult
                            ? scanResult.files_scanned.toLocaleString()
                            : 0}

                        </h2>

                        <span>Objects Scanned</span>

                    </div>

                </div>

            </div>

            <div className="scan-panel">

                <h3>Scan Activity</h3>

                <ScanActivityChart />

            </div>

        </div>

        <div className="engine-grid">

                <div className="scan-panel engine-panel">

                <h3>Active Engines</h3>

                <div className="engine-card">
                    <h4>Behavior Engine</h4>
                    <p>Version 6.2.1</p>
                </div>

                <div className="engine-card">
                    <h4>Risk Engine</h4>
                    <p>Version 4.1.8</p>
                </div>

                <div className="engine-card">
                    <h4>Decision Engine</h4>
                    <p>Version 3.2.5</p>

                </div>

                <div className="engine-card">
                    <h4>Entropy Detector</h4>
                    
                </div>

                <div className="engine-card">
                    <h4>ML Detector</h4>
                    <p></p>
                </div>

                <div className="engine-card">
                    <h4>Hash Detector</h4>
                    
                </div>

                <div className="engine-card">
                    <h4>Burst Detector</h4>
                    
                </div>

                <div className="engine-card">
                    <h4>Process Detector</h4>
                    
                </div>

            </div>

            

                    <div className="scan-panel detected-panel">

                    
                    <h3>Detected Files</h3>

                    {scanResult?.details?.length ? (

                        <table>

                            <thead>

                            <tr>

                            <th>File</th>

                            <th>Risk</th>

                            <th>Decision</th>

                            <th>Quarantine</th>

                            </tr>

                            </thead>

                            <tbody>

                            {scanResult.details.map((item,index)=>(

                            <tr key={index}>

                            <td>{item.file.split("\\").pop()}</td>

                            <td>{item.risk}</td>

                            <td>{item.decision}</td>

                            <td>{item.quarantine}</td>

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

);


}

export default ScanPage;
