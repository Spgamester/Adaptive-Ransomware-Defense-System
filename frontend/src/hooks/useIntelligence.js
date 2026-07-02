import { useEffect, useState } from "react";
import { getIntelligence } from "../api/intelligenceApi";

export default function useIntelligence() {

    const [intel, setIntel] = useState({

        behavior: "System Idle",

        confidence: 0,

        stage: "Monitoring",

        risk_score: 0,

        risk_level: "Safe",

        decision: "None",

        priority: 0,

        actions: [],

        status: "Ready"

    });

    useEffect(() => {

        async function load() {

            try {

                const data = await getIntelligence();

                setIntel(data);

            }

            catch (err) {

                console.error(err);

                setIntel({

                    behavior: "API Offline",

                    confidence: 0,

                    stage: "Disconnected",

                    risk_score: 0,

                    risk_level: "Unknown",

                    decision: "Retry",

                    priority: 0,

                    actions: [],

                    status: "Backend Offline"

                });

            }

        }

        load();

        const interval = setInterval(load, 2000);

        return () => clearInterval(interval);

    }, []);

    return intel;
}