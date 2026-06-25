function MitrePanel() {

    const tactics = [
        ["Execution", 352],
        ["Persistence", 214],
        ["Privilege Escalation", 187],
        ["Defense Evasion", 163],
        ["Lateral Movement", 142]
    ];

    return (
        <div className="mini-panel">

            <h3>MITRE ATT&CK</h3>

            {tactics.map((item) => (

                <div
                    className="mitre-row"
                    key={item[0]}
                >

                    <span>{item[0]}</span>

                    <div className="bar-bg">

                        <div
                            className="bar-fill"
                            style={{
                                width: `${item[1] / 4}px`
                            }}
                        />

                    </div>

                    <span>{item[1]}</span>

                </div>

            ))}

        </div>
    );
}

export default MitrePanel;