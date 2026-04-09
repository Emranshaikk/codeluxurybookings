/**
 * ELITE LUXURY BOOKINGS - VALENS API BRIDGE
 * Connects the native search widget directly to the Valens Dashboard via API.
 */

const VALENS_CONFIG = {
    ENDPOINT: 'https://jetluxe.jetlink.app/api/affiliate/valens/v1/trip/new',
    TOKEN: '77|CkX9R7zefI00A3vp3CPKqYH2P9NlHvCABNryulMba24b86ed',
    AIRPORTS: [
        { name: "London Heathrow", city: "London", icao: "EGLL" },
        { name: "London Gatwick", city: "London", icao: "EGKK" },
        { name: "London Farnborough", city: "London", icao: "EGLF" },
        { name: "London Biggin Hill", city: "London", icao: "EGKB" },
        { name: "Paris Charles de Gaulle", city: "Paris", icao: "LFPG" },
        { name: "Paris Le Bourget", city: "Paris", icao: "LFPB" },
        { name: "Nice Côte d'Azur", city: "Nice", icao: "LFMN" },
        { name: "Dubai International", city: "Dubai", icao: "OMDB" },
        { name: "Dubai Al Maktoum", city: "Dubai", icao: "OMDW" },
        { name: "New York JFK", city: "New York", icao: "KJFK" },
        { name: "Teterboro", city: "New York/NJ", icao: "KTEB" },
        { name: "Miami International", city: "Miami", icao: "KMIA" },
        { name: "Opa Locka", city: "Miami", icao: "KOPF" },
        { name: "Geneva Cointrin", city: "Geneva", icao: "LSGG" },
        { name: "Zurich Kloten", city: "Zurich", icao: "LSZH" },
        { name: "Ibiza Airport", city: "Ibiza", icao: "LEIB" },
        { name: "Mykonos", city: "Mykonos", icao: "LGMK" },
        { name: "Monaco Heliport", city: "Monaco", icao: "LNMC" },
        { name: "Cannes-Mandelieu", city: "Cannes", icao: "LFMD" },
        { name: "Aspen Pitkin County", city: "Aspen", icao: "KASE" },
        { name: "Riyadh King Khalid", city: "Riyadh", icao: "OERK" },
        { name: "Doha Hamad", city: "Doha", icao: "OTHH" }
    ]
};

async function submitToValens(data) {
    const payload = {
        idempotency_key: crypto.randomUUID(),
        legs: [{
            date: data.date,
            time: data.time || "12:00",
            passengers: parseInt(data.passengers),
            departure_icao: data.departure_icao,
            arrival_icao: data.arrival_icao
        }],
        customer: {
            full_name: data.full_name,
            contact: data.contact,
            email: data.email
        }
    };

    const url = `${VALENS_CONFIG.ENDPOINT}?api_token=${VALENS_CONFIG.TOKEN}`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (!response.ok) {
            const errorDetail = result.message || (result.errors ? JSON.stringify(result.errors) : JSON.stringify(result));
            return { success: false, error: errorDetail };
        }
        return { success: true, data: result };
    } catch (error) {
        console.error("Valens Redirect Error:", error);
        return { success: false, error: "Browser Security Block. Please refresh and try again or use WhatsApp." };
    }
}

// Search Logic
function searchAirports(query) {
    if (!query || query.length < 2) return [];
    const q = query.toLowerCase();
    return VALENS_CONFIG.AIRPORTS.filter(a => 
        a.name.toLowerCase().includes(q) || 
        a.city.toLowerCase().includes(q) || 
        a.icao.toLowerCase().includes(q)
    ).slice(0, 5);
}
