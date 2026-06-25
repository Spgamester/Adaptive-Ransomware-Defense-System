
function SecurityScore({ score }) {
    return (
        <div className="security-score-card">

            <div className="ring">
                <div className="inner-ring">
                    <h1>{score}</h1>
                    <span>/100</span>
                </div>
            </div>

            <h2>Security Score</h2>

            <p>System Secure</p>

        </div>
    );
}

export default SecurityScore;
