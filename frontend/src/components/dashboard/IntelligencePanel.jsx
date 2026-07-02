function IntelligencePanel({ intelligence }) {

    return (

        <div className="intelligence-panel">

            <h2>Threat Intelligence</h2>

            <div className="intel-grid">

                <div className="intel-box">
                    <span>Behavior</span>
                    <h3>{intelligence.behavior}</h3>
                </div>

                <div className="intel-box">
                    <span>Confidence</span>
                    <h3>{intelligence.confidence}%</h3>
                </div>

                <div className="intel-box">
                    <span>Stage</span>
                    <h3>{intelligence.stage}</h3>
                </div>

                <div className="intel-box">
                    <span>Risk Level</span>
                    <h3>{intelligence.risk_level}</h3>
                </div>

                <div className="intel-box">
                    <span>Decision</span>
                    <h3>{intelligence.decision}</h3>
                </div>

                <div className="intel-box">
                    <span>Status</span>
                    <h3>{intelligence.status}</h3>
                </div>

            </div>

        </div>

    );

}

export default IntelligencePanel;