import { useEffect, useState } from "react";

function MitrePanel() {

    const [mitre, setMitre] = useState({

        id: "-",

        technique: "Loading...",

        confidence: 0,

        reason: ""

    });

    useEffect(() => {

        const loadMitre = () => {

            fetch("http://127.0.0.1:8000/api/mitre")
                .then(res => res.json())
                .then(data => {

                    setMitre(data);

                })
                .catch(err => console.error(err));

        };

        loadMitre();

        const interval = setInterval(loadMitre, 2000);

        return () => clearInterval(interval);

    }, []);

    return (

        <div className="mini-panel">

            <h3>MITRE ATT&CK Mapping</h3>

            <div className="mitre-card">

                <div className="mitre-id">

                    {mitre.id}

                </div>

                <div className="mitre-technique">

                    {mitre.technique}

                </div>

                <div className="mitre-confidence">

                    Confidence

                    <strong>

                        {mitre.confidence}%

                    </strong>

                </div>

                <div className="mitre-reason">

                    {mitre.reason}

                </div>

            </div>

        </div>

    );

}

export default MitrePanel;