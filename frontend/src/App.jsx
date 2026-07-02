import { useState } from "react";

import {
    Shield,
    Search,
    Activity,
    Lock,
    Settings,
    Bell,
    CircleHelp,
    RefreshCw,
    ChevronDown,
    UserCircle
} from "lucide-react";

import Dashboard from "./pages/Dashboard";
import ScanPage from "./pages/ScanPage";
import MonitorPage from "./pages/MonitorPage";
import QuarantinePage from "./pages/QuarantinePage";
import SettingsPage from "./pages/SettingsPage";
import logo from "./assets/images/logo.png";

import SplashScreen from "./components/SplashScreen/SplashScreen";

import "./index.css";

function App() {

    const [loading, setLoading] = useState(true);

    const [activePage, setActivePage] = useState("dashboard");


    return (

        <div className="app">

            {/* ================= SIDEBAR ================= */}

            <aside className="sidebar">

                <div className="logo-area">

                    <img
                    src={logo}
                    alt="ARDS Logo"
                    className="sidebar-logo"
                />
                    

                    <div>

                        <h1>ARDS</h1>

                        <p>

                            Ransomware Detection System

                        </p>

                    </div>

                </div>

                <button

                    className={`nav ${activePage === "dashboard" ? "active" : ""}`}

                    onClick={() => setActivePage("dashboard")}

                >

                    <Shield size={18} />

                    Dashboard

                </button>

                <button

                    className={`nav ${activePage === "scan" ? "active" : ""}`}

                    onClick={() => setActivePage("scan")}

                >

                    <Search size={18} />

                    Scan Center

                </button>

                <button

                    className={`nav ${activePage === "monitor" ? "active" : ""}`}

                    onClick={() => setActivePage("monitor")}

                >

                    <Activity size={18} />

                    Monitor

                </button>

                <button

                    className={`nav ${activePage === "quarantine" ? "active" : ""}`}

                    onClick={() => setActivePage("quarantine")}

                >

                    <Lock size={18} />

                    Quarantine

                </button>

                <button

                    className={`nav ${activePage === "settings" ? "active" : ""}`}

                    onClick={() => setActivePage("settings")}

                >

                    <Settings size={18} />

                    Settings

                </button>

            </aside>

            {/* ================= MAIN ================= */}

            <main

                className="main-content"

            >

                {/* ================= HEADER ================= */}

                <div className="topbar">

                    <div>

                        <h2>

                            Security Operations Center

                        </h2>

                        <p className="subtitle">

                            AI Ransomware Defense System

                        </p>

                    </div>

                    <div className="header-actions">

                        <div className="notification-wrapper">

                            <Bell size={20} />

                            <span className="notification-badge">

                                3

                            </span>

                        </div>

                        <CircleHelp size={20} />

                        <div className="time-filter">

                            Last 24 Hours

                            <ChevronDown size={16} />

                        </div>

                        <div className="refresh-btn">

                            <RefreshCw size={18} />

                        </div>

                        <div className="user-profile">

                            <UserCircle size={28} />

                            <div>

                                <div className="user-name">

                                    SOC Analyst

                                </div>

                                <div className="user-role">

                                    Security Team

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

                {/* ================= PAGE ROUTER ================= */}

                <div className="page-container">

                    {activePage === "dashboard" && <Dashboard />}

                    {activePage === "scan" && <ScanPage />}

                    {activePage === "monitor" && <MonitorPage />}

                    {activePage === "quarantine" && <QuarantinePage />}

                    {activePage === "settings" && <SettingsPage />}

                </div>

            </main>

          {loading && (

            <SplashScreen

                onFinish={() => setLoading(false)}

            />

        )}

        </div>


    );

}

export default App;