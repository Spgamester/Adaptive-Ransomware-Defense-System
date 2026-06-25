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

import Dashboard from "./components/Dashboard";
import ScanPage from "./components/ScanPage";
import MonitorPage from "./components/MonitorPage";
import QuarantinePage from "./components/QuarantinePage";
import SettingsPage from "./components/SettingsPage";

import "./index.css";

function App() {

  const [activePage, setActivePage] = useState("dashboard");

  return (

    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="logo-area">

          <Shield
            size={34}
            color="#00E5FF"
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

      {/* MAIN */}

      <main className="main-content">

        {/* HEADER */}

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

        {/* PAGE ROUTER */}

        {activePage === "dashboard" && <Dashboard />}

        {activePage === "scan" && <ScanPage />}

        {activePage === "monitor" && <MonitorPage />}

        {activePage === "quarantine" && <QuarantinePage />}

        {activePage === "settings" && <SettingsPage />}

      </main>

    </div>

  );
}

export default App;