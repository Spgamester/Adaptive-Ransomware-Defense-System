const API = "http://localhost:8000";

export async function getIntelligence() {

    const response = await fetch(`${API}/api/intelligence`);

    if (!response.ok) {
        throw new Error("Failed to fetch intelligence");
    }

    return await response.json();

}