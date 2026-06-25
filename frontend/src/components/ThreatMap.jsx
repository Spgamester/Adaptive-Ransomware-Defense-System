function ThreatMap() {

    const regions = [
        { name: "North America", count: 532 },
        { name: "Europe", count: 412 },
        { name: "Asia Pacific", count: 198 },
        { name: "South America", count: 61 },
        { name: "Africa", count: 45 }
    ];

    return (

        <div className="threat-map-panel">

            <h3>Global Threat Map</h3>

            <div className="threat-map-layout">

                <div className="map-area">

                    <img
                        src="https://upload.wikimedia.org/wikipedia/commons/8/80/World_map_-_low_resolution.svg"
                        alt="World Map"
                        className="world-map"
                    />

                    <div className="attack-dot dot1"></div>
                    <div className="attack-dot dot2"></div>
                    <div className="attack-dot dot3"></div>
                    <div className="attack-dot dot4"></div>
                    <div className="attack-dot dot5"></div>

                </div>
                <div>

                    <h4>Top Regions</h4>

                    {regions.map((region) => (

                        <div
                            key={region.name}
                            className="region-row"
                        >

                            <div
                                style={{
                                    display: "flex",
                                    justifyContent: "space-between"
                                }}
                            >

                                <span>{region.name}</span>

                                <span>{region.count}</span>

                            </div>

                            <div className="region-bar">

                                <div
                                    className="region-fill"
                                    style={{
                                        width: `${region.count / 6}%`
                                    }}
                                />

                            </div>

                        </div>

                    ))}

                </div>

            </div>

        </div>

    );
}

export default ThreatMap;