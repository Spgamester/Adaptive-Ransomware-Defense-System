import { useEffect, useRef, useState } from "react";
import "./SplashScreen.css";

import logo from "../../assets/images/logo.png";
import startupVideo from "../../assets/videos/startup.mp4";

function SplashScreen({ onFinish }) {

    const videoRef = useRef(null);

    const messages = [

        "Initializing Detection Engine...",

        "Loading Machine Learning Model...",

        "Loading Threat Intelligence...",

        "Loading Behavior Engine...",

        "Loading Risk Engine...",

        "Starting Real-Time Monitor...",

        "Launching Security Operations Center..."

    ];

    const [phase, setPhase] = useState("video");

    const [progress, setProgress] = useState(0);

    const [currentMessage, setCurrentMessage] = useState(-1);

    const [fadeOut, setFadeOut] = useState(false);
    useEffect(() => {

        if (phase !== "boot") return;
    
        let msg = -1;
    
        const msgInterval = setInterval(() => {
    
            msg++;
    
            setCurrentMessage(msg);
    
            if (msg >= messages.length - 1) {
    
                clearInterval(msgInterval);
    
            }
    
        }, 500);
    
        let p = 0;
    
        const progressInterval = setInterval(() => {
    
            p += 2;
    
            setProgress(p);
    
            if (p >= 100) {
    
                clearInterval(progressInterval);
    
                setTimeout(() => {
    
                    setFadeOut(true);
    
                }, 700);
    
                setTimeout(() => {
    
                    onFinish();
    
                }, 1800);
    
            }
    
        }, 70);
    
        return () => {
    
            clearInterval(msgInterval);
    
            clearInterval(progressInterval);
    
        };
    
    }, [phase, onFinish]);

    const handleVideoEnd = () => {

        setTimeout(() => {

            setPhase("boot");

        }, 500);

    };

    return (

        <div className={`splash-screen ${fadeOut ? "fade-out" : ""}`}>

            {

                phase === "video"

                ?

                (

                    <video

                        ref={videoRef}

                        className="startup-video"

                        autoPlay

                        muted

                        playsInline

                        onEnded={handleVideoEnd}

                    >

                        <source

                            src={startupVideo}

                            type="video/mp4"

                        />

                    </video>

                )

                :

                (

                    <div className="boot-screen">

                        <img

                            src={logo}

                            alt="ARDS"

                            className="boot-logo"

                        />

                        <h1>

                            Adaptive Ransomware Detection System

                        </h1>

                        <h3>

                            AI Powered Enterprise Ransomware Protection

                        </h3>

                        <div className="loading-box">

                            {

                                messages.map((msg,index)=>(

                                    <div

                                        key={index}

                                        className={

                                            index<=currentMessage

                                            ?

                                            "loaded"

                                            :

                                            "pending"

                                        }

                                    >

                                        {

                                            index<=currentMessage

                                            ?

                                            "✓"

                                            :

                                            "•"

                                        }

                                        {" "}

                                        {msg}

                                    </div>

                                ))

                            }

                        </div>

                        <div className="progress-container">

                            <div

                                className="progress-fill"

                                style={{

                                    width:`${progress}%`

                                }}

                            />

                        </div>

                        <div className="progress-text">

                            {progress}%

                        </div>

                    </div>

                )

            }

        </div>

    );

}

export default SplashScreen;