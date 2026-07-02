import { useEffect, useState } from "react";
import API from "../api/config";
function QuarantinePage() {

    const [quarantineData, setQuarantineData] = useState({
        threats_isolated: 0,
        files_quarantined: 0,
        risk_score: 0,
        storage_used: "0 GB"
    });

    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    useEffect(()=>{

        loadQuarantineData();

        const interval = setInterval(

            loadQuarantineData,

            2000

        );

        return ()=>clearInterval(interval);

    },[]);

    const loadQuarantineData = async () => {

        try {

            const statsResponse = awaitfetch(`${API}/api/qurantine`)

            const statsData = await statsResponse.json();

            setQuarantineData(statsData);

            const filesResponse = await fetch(
                `${API}/api/quarantine-files`
            );

            const filesData = await filesResponse.json();

            console.log(filesData);

            setFiles(filesData);

            setFiles(filesData);

        } catch (error) {

            console.error(
                "Quarantine Load Error:",
                error
            );

        }

    };

        const restoreFile = async (filename) => {

        try {

            await fetch(
                `${API}/api/restore/${filename}`,
                {
                    method: "POST"
                }
            );

            setFiles((prev) =>
                prev.filter(
                    (file) => file.file !== filename
                )
                
            );
            await loadQuarantineData();

            if (selectedFile?.file === filename) {
            }

        } catch (error) {

            console.error(
                "Restore Error:",
                error
            );

        }

    };

        const deleteFile = async (filename) => {

        try {

            await fetch(
                `${API}/api/delete/${filename}`,
                {
                    method: "DELETE"
                }
            );

            setFiles((prev) =>
                prev.filter(
                    (file) => file.file !== filename
                )
            );

            await loadQuarantineData();

            if (selectedFile?.file === filename) {
                setSelectedFile(null);
            }

        } catch (error) {

            console.error(
                "Delete Error:",
                error
            );

        }

    };

    return (

        <div>

            <h1 className="page-title">
                Quarantine Vault
            </h1>

            <p className="page-subtitle">
                Secure isolation of detected threats
            </p>

            <div className="vault-status">
                <span className="vault-dot"></span>
                Isolation Active
            </div>

            {/* KPI CARDS */}

            <div className="quarantine-stats">

                <div className="quarantine-card">
                    <h4>Threats Isolated</h4>
                    <h2>
                        {quarantineData.threats_isolated}
                    </h2>
                </div>

                <div className="quarantine-card">
                    <h4>Files Quarantined</h4>
                    <h2>
                        {quarantineData.files_quarantined}
                    </h2>
                </div>

                <div className="quarantine-card">
                    <h4>Risk Score</h4>
                    <h2 className="danger-text">
                        {quarantineData.risk_score}
                    </h2>
                </div>

                <div className="quarantine-card">
                    <h4>Storage Used</h4>
                    <h2>
                        {quarantineData.storage_used}
                    </h2>
                </div>

            </div>

            {/* THREATS TABLE */}

                <div className="quarantine-table-panel quarantine-scroll">

                <h2>Quarantined Threats</h2>

                <table>

                    <thead>

                        <tr>
                            <th>Threat</th>
                            <th>Family</th>
                            <th>Risk</th>
                            <th>Actions</th>
                        </tr>

                    </thead>

                    <tbody>

                        {files.length > 0 ? (

                            files.map((item) => (

                                <tr
                                    key={item.id}
                                    onClick={() =>
                                        setSelectedFile(item)
                                    }
                                    style={{
                                        cursor: "pointer"
                                    }}
                                >

                                    <td>{item.file}</td>

                                    <td>{item.family}</td>

                                    <td>

                                        <span
                                            className={
                                                item.risk === "Critical"
                                                    ? "critical-badge"
                                                    : item.risk === "High"
                                                    ? "high-badge"
                                                    : "medium-badge"
                                            }
                                        >
                                            {item.risk}
                                        </span>

                                    </td>

                                    <td>

                                        <button
                                            className="restore-btn"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                restoreFile(item.file);
                                            }}
                                        >
                                            Restore
                                        </button>

                                        <button
                                            className="delete-btn"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                deleteFile(item.file);
                                            }}
                                        >
                                            Delete
                                        </button>

                                    </td>

                                </tr>

                            ))

                        ) : (

                            <tr>

                                <td colSpan="4">
                                    No quarantined threats found
                                </td>

                            </tr>

                        )}

                    </tbody>

                </table>

            </div>

            {/* THREAT DETAILS */}

            <div className="threat-details-panel">

                <h2>Threat Intelligence</h2>

                {selectedFile ? (

                    <div className="details-grid">

                        <div className="detail-card">
                            <h4>Threat File</h4>
                            <p>{selectedFile.file}</p>
                        </div>

                        <div className="detail-card">
                            <h4>Malware Family</h4>
                            <p>{selectedFile.family}</p>
                        </div>

                        <div className="detail-card">
                            <h4>Risk Level</h4>
                            <p>{selectedFile.risk}</p>
                        </div>

                        <div className="detail-card">
                            <h4>Status</h4>
                            <p>{selectedFile.status}</p>
                        </div>

                        <div className="detail-card">
                            <h4>Threat ID</h4>
                            <p>{selectedFile.id}</p>
                        </div>

                        <div className="detail-card">
                            <h4>Isolation State</h4>
                            <p className="danger-text">ACTIVE</p>
                        </div>

                        <div className="detail-card">
                            <h4>File Size</h4>
                            <p>{selectedFile.size}</p>
                        </div>

                    </div>

                ) : (

                    <div
                        style={{
                            padding: "30px",
                            textAlign: "center"
                        }}
                    >
                        <div className="report-empty">

                            <h3>No Threat Selected</h3>

                            <p>

                                Select a quarantined file from the table to view:

                            </p>

                            <ul>

                                <li>Threat Intelligence</li>

                                <li>Risk Level</li>

                                <li>Isolation Status</li>

                                <li>File Metadata</li>

                            </ul>

                        </div>
                    </div>

                )}

            </div>

        </div>

    );

}

export default QuarantinePage;