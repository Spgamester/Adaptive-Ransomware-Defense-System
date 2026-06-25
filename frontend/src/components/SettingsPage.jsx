
import { useEffect, useState } from "react";

function SettingsPage() {

    const [settings, setSettings] = useState({
        auto_scan: true,
        real_time: true,
        heuristic: true,
        entropy: true,
        auto_quarantine: true,
        threat_alerts: true,
        launch_startup: false
    });

    const [saved, setSaved] = useState(false);

    useEffect(() => {
        loadSettings();
    }, []);

    const loadSettings = async () => {

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/api/settings"
            );

            const data = await response.json();

            setSettings(data);

        } catch (error) {

            console.error(error);

        }

    };

    const saveSettings = async () => {

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/api/settings",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(settings)
                }
            );

            const result = await response.json();

            console.log(result);

            setSaved(true);

            setTimeout(() => {

                setSaved(false);

            }, 2500);

        } catch (error) {

            console.error(error);

        }

    };

    const handleToggle = (key) => {

        setSettings((prev) => ({
            ...prev,
            [key]: !prev[key]
        }));

    };

    return (

        <div>

            <h1 className="page-title">
                System Settings
            </h1>

            <p className="page-subtitle">
                Configure ARDS detection and protection preferences
            </p>

            <div className="system-status">

                <span className="status-dot"></span>

                <div>

                    <strong>
                        Protection Active
                    </strong>

                    <p>
                        All Security Modules Operational
                    </p>

                </div>

            </div>

            <div className="settings-grid">

                {/* ===========================
                    GENERAL SETTINGS
                =========================== */}

                <div className="settings-card">

                    <h3>
                        General Protection
                    </h3>

                    <div className="setting-row">

                        <span>
                            Automatic Startup Scan
                        </span>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={settings.auto_scan}
                                onChange={() =>
                                    handleToggle("auto_scan")
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>

                    <div className="setting-row">

                        <span>
                            Real-Time Protection
                        </span>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={settings.real_time}
                                onChange={() =>
                                    handleToggle("real_time")
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>

                    <div className="setting-row">

                        <span>
                            Auto Quarantine
                        </span>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={settings.auto_quarantine}
                                onChange={() =>
                                    handleToggle("auto_quarantine")
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>

                    <div className="setting-row">

                        <span>
                            Launch With Startup
                        </span>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={settings.launch_startup}
                                onChange={() =>
                                    handleToggle("launch_startup")
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>

                </div>

                {/* ===========================
                    DETECTION ENGINE
                =========================== */}

                <div className="settings-card">

                    <h3>
                        Detection Engine
                    </h3>

                    <div className="setting-row">

                        <span>
                            Machine Learning Detection
                        </span>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={settings.real_time}
                                onChange={() =>
                                    handleToggle("real_time")
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>

                    <div className="setting-row">

                        <span>
                            Heuristic Analysis
                        </span>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={settings.heuristic}
                                onChange={() =>
                                    handleToggle("heuristic")
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>

                    <div className="setting-row">

                        <span>
                            Entropy Detection
                        </span>

                        <label className="switch">

                            <input
                                type="checkbox"
                                checked={settings.entropy}
                                onChange={() =>
                                    handleToggle("entropy")
                                }
                            />

                            <span className="slider"></span>

                        </label>

                    </div>
<div className="setting-row">

<span>
    Behavior Monitoring
</span>

<label className="switch">

    <input
        type="checkbox"
        checked={settings.real_time}
        onChange={() =>
            handleToggle("real_time")
        }
    />

    <span className="slider"></span>

</label>

</div>

</div>

</div>

{/* ===========================
SECOND ROW
=========================== */}

<div className="settings-grid">

{/* ===========================
ALERT CONFIGURATION
=========================== */}

<div className="settings-card">

<h3>
Alert Configuration
</h3>

<div className="setting-row">

<span>
    Threat Alerts
</span>

<label className="switch">

    <input
        type="checkbox"
        checked={settings.threat_alerts}
        onChange={() =>
            handleToggle("threat_alerts")
        }
    />

    <span className="slider"></span>

</label>

</div>

<div className="setting-row">

<span>
    Email Alerts
</span>

<label className="switch">

    <input
        type="checkbox"
        checked
        readOnly
    />

    <span className="slider"></span>

</label>

</div>

<div className="setting-row">

<span>
    Desktop Notifications
</span>

<label className="switch">

    <input
        type="checkbox"
        checked
        readOnly
    />

    <span className="slider"></span>

</label>

</div>

<div className="setting-row">

<span>
    Quarantine Notifications
</span>

<label className="switch">

    <input
        type="checkbox"
        checked
        readOnly
    />

    <span className="slider"></span>

</label>

</div>

</div>

{/* ===========================
SYSTEM INFORMATION
=========================== */}

<div className="settings-card">

<h3>
System Information
</h3>

<div className="info-row">

<span>
    ARDS Version
</span>

<strong>
    v2.6.1
</strong>

</div>

<div className="info-row">

<span>
    ML Model
</span>

<strong>
    Random Forest
</strong>

</div>

<div className="info-row">

<span>
    Threat Database
</span>

<strong className="status-green">
    UPDATED
</strong>

</div>

<div className="info-row">

<span>
    Monitoring Engine
</span>

<strong className="status-green">
    ACTIVE
</strong>

</div>

<div className="info-row">

<span>
    Protection Status
</span>

<strong className="status-green">
    PROTECTED
</strong>

</div>

<div className="info-row">

<span>
    Auto Quarantine
</span>

<strong>

    {
        settings.auto_quarantine
            ? "Enabled"
            : "Disabled"
    }

</strong>

</div>

<div className="info-row">

<span>
    Threat Alerts
</span>

<strong>

    {
        settings.threat_alerts
            ? "Enabled"
            : "Disabled"
    }

</strong>

</div>

</div>

</div>
{/* ===========================
                SAVE SECTION
            =========================== */}

            <div className="save-settings-card">

                <div>

                    <h3>
                        Configuration
                    </h3>

                    <p className="save-text">
                        Changes are stored locally inside
                        <strong> settings.json </strong>
                        and will automatically load when
                        ARDS starts.
                    </p>

                    {
                        saved && (

                            <div className="save-success">

                                ✔ Configuration Saved Successfully

                            </div>

                        )
                    }

                </div>

                <button
                    className="save-btn"
                    onClick={saveSettings}
                >

                    💾 Save Configuration

                </button>

            </div>

        </div>

    );

}

export default SettingsPage;
