import { useEffect, useState } from "react";

function QuarantinePage() {

    const [quarantineData, setQuarantineData] = useState({
        threats_isolated: 0,
        files_quarantined: 0,
        risk_score: 0,
        storage_used: "0 GB"
    });

    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    useEffect(() => {

        loadQuarantineData();

    }, []);

    const loadQuarantineData = async () => {

        try {

            const statsResponse = await fetch(
                "http://127.0.0.1:8000/api/quarantine"
            );

            const statsData = await statsResponse.json();

            setQuarantineData(statsData);

            const filesResponse = await fetch(
                "http://127.0.0.1:8000/api/quarantine-files"
            );

            const filesData = await filesResponse.json();

            setFiles(filesData);

        } catch (error) {

            console.error(
                "Quarantine Load Error:",
                error
            );

        }

    };

    const restoreFile = async (id) => {

        try {

            await fetch(
                `http://127.0.0.1:8000/api/restore/${id}`,
                {
                    method: "POST"
                }
            );

            setFiles((prev) =>
                prev.filter(
                    (file) => file.id !== id
                )
            );

            if (selectedFile?.id === id) {
                setSelectedFile(null);
            }

        } catch (error) {

            console.error(
                "Restore Error:",
                error
            );

        }

    };

    const deleteFile = async (id) => {

        try {

            await fetch(
                `http://127.0.0.1:8000/api/delete/${id}`,
                {
                    method: "DELETE"
                }
            );

            setFiles((prev) =>
                prev.filter(
                    (file) => file.id !== id
                )
            );

            if (selectedFile?.id === id) {
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

            <div className="quarantine-table-panel">

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

                            <div className="detail-card">

                            <h4>File Size</h4>

                            <p>
                                {selectedFile.size}
                            </p>

                        </div>
                            <p className="danger-text">
                                ACTIVE
                            </p>
                        </div>

                    </div>

                ) : (

                    <div
                        style={{
                            padding: "30px",
                            textAlign: "center"
                        }}
                    >
                        Select a quarantined threat
                        to view intelligence details.
                    </div>

                )}

            </div>

        </div>

    );

}

export default QuarantinePage;