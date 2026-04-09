/**
 * ELITE LUXURY BOOKINGS - VALENS API BRIDGE
 * Connects the native search widget directly to the Valens Dashboard via API.
 */

const VALENS_CONFIG = {
    ENDPOINT: 'https://jetluxe.jetlink.app/api/affiliate/valens/v1/trip/new',
    TOKEN: '64|t997lbxqnHWlW15TpE5FCogSyTev2hKpOLRo2Hjj7cad47bc',
    AIRPORT_MAP: {
        'london': 'EGLL', 'lhr': 'EGLL', 'lgw': 'EGKK', 'fab': 'EGLF', 'nice': 'LFMN', 'nce': 'LFMN',
        'dubai': 'OMDB', 'dxb': 'OMDB', 'dwc': 'OMDW', 'paris': 'LFPG', 'cdg': 'LFPG', 'le bourgeois': 'LFPB',
        'miami': 'KMIA', 'mia': 'KMIA', 'opa locka': 'KOPF', 'new york': 'KJFK', 'jfk': 'KJFK', 'tebor': 'KTEB',
        'geneva': 'LSGG', 'gva': 'LSGG', 'aspen': 'KASE', 'ase': 'KASE', 'ibiza': 'LEIB', 'ibz': 'LEIB',
        'mykonos': 'LGMK', 'jmks': 'LGMK', 'moscow': 'UUEE', 'svo': 'UUEE', 'vnukovo': 'UUWW',
        'riyadh': 'OERK', 'ruh': 'OERK', 'doha': 'OTBD', 'dia': 'OTBD', 'hamad': 'OTHH'
    }
};

async function submitToValens(formData) {
    // 1. Generate Idempotency Key
    const idempotencyKey = crypto.randomUUID();

    // 2. Resolve ICAO Codes
    const departureICAO = resolveICAO(formData.departure);
    const arrivalICAO = resolveICAO(formData.arrival);

    // 3. Construct Payload
    const payload = {
        idempotency_key: idempotencyKey,
        legs: [{
            date: formData.travel_date,
            time: formData.travel_time || "12:00",
            passengers: parseInt(formData.passengers),
            departure_icao: departureICAO,
            arrival_icao: arrivalICAO
        }],
        customer: {
            full_name: formData.name,
            contact: formData.contact,
            email: formData.email || "client@eliteluxurybookings.com" // Fallback if email field is missing
        }
    };

    // 4. Submit to Valens API
    try {
        const response = await fetch(VALENS_CONFIG.ENDPOINT, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${VALENS_CONFIG.TOKEN}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        return { success: response.ok, data: result };
    } catch (error) {
        console.error("Valens API Error:", error);
        return { success: false, error: error.message };
    }
}

function resolveICAO(input) {
    const cleanInput = input.toLowerCase().trim();
    // Direct match in map
    for (const [key, icao] of Object.entries(VALENS_CONFIG.AIRPORT_MAP)) {
        if (cleanInput.includes(key)) return icao;
    }
    // Fallback/Generic (API requires 4 letters)
    return "EGLL"; // Defaulting to London if unknown for testing, or we should handle this better
}
