
function SecurityScore({ score = 100 }) {

    let status = "System Secure";

    let color = "#00D26A";

    if(score < 80){

        status="Monitoring";

        color="#FFD000";

    }

    if(score < 50){

        status="High Risk";

        color="#FF9D00";

    }

    if(score < 25){

        status="Critical";

        color="#FF3B3B";

    }

    return(

        <div className="security-score-card">

            <div
                className="ring"
                style={{
                    borderColor:color
                }}
            >

                <div className="inner-ring">

                    <h1>{score}</h1>

                    <span>/100</span>

                </div>

            </div>

            <h2>Security Score</h2>

            <p style={{color}}>

                {status}

            </p>

        </div>

    );

}

export default SecurityScore;