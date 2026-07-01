<?php
// submit-lead.php - Secure Server-Side Telegram Lead Relay for Elite Luxury Bookings

// Set CORS and headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method Not Allowed"]);
    exit;
}

// Telegram Credentials (securely held on server side)
$telegram_bot_token = '8274022771:AAHDPmDq6vfAttktCf1iOeNAwqSAuUFgP2g';
$telegram_chat_id = '5875175296';

// Check if request is JSON
$contentType = isset($_SERVER["CONTENT_TYPE"]) ? trim($_SERVER["CONTENT_TYPE"]) : '';
$isJson = (stripos($contentType, 'application/json') !== false);

$name = '';
$email = '';
$phone = '';
$departure = '';
$destination = '';
$requirements = '';
$date = '';
$passengers = '';
$target = 'Elite Luxury Bookings Inquiry';
$rawText = '';

if ($isJson) {
    // Read raw body
    $content = trim(file_get_contents("php://input"));
    $decoded = json_decode($content, true);
    
    if (is_array($decoded)) {
        // Case 1: Client constructor constructed the message text itself
        if (isset($decoded['text'])) {
            $rawText = $decoded['text'];
        } else {
            // Case 2: Client sent structured JSON parameters
            $name = isset($decoded['name']) ? strip_tags(trim($decoded['name'])) : '';
            $email = isset($decoded['email']) ? filter_var(trim($decoded['email']), FILTER_VALIDATE_EMAIL) : '';
            $phone = isset($decoded['phone']) ? strip_tags(trim($decoded['phone'])) : '';
            $departure = isset($decoded['departure']) ? strip_tags(trim($decoded['departure'])) : '';
            $destination = isset($decoded['destination']) ? strip_tags(trim($decoded['destination'])) : '';
            $requirements = isset($decoded['requirements']) ? strip_tags(trim($decoded['requirements'])) : '';
            $date = isset($decoded['date']) ? strip_tags(trim($decoded['date'])) : '';
            $passengers = isset($decoded['passengers']) ? strip_tags(trim($decoded['passengers'])) : '';
            $target = isset($decoded['_target']) ? strip_tags(trim($decoded['_target'])) : 'Elite Luxury Bookings Inquiry';
        }
    }
} else {
    // Normal POST Form Parameter structure
    $name = isset($_POST['name']) ? strip_tags(trim($_POST['name'])) : '';
    $email = isset($_POST['email']) ? filter_var(trim($_POST['email']), FILTER_VALIDATE_EMAIL) : '';
    $phone = isset($_POST['phone']) ? strip_tags(trim($_POST['phone'])) : '';
    $departure = isset($_POST['departure']) ? strip_tags(trim($_POST['departure'])) : '';
    $destination = isset($_POST['destination']) ? strip_tags(trim($_POST['destination'])) : '';
    $requirements = isset($_POST['requirements']) ? strip_tags(trim($_POST['requirements'])) : '';
    $date = isset($_POST['date']) ? strip_tags(trim($_POST['date'])) : '';
    $passengers = isset($_POST['passengers']) ? strip_tags(trim($_POST['passengers'])) : '';
    $target = isset($_POST['_target']) ? strip_tags(trim($_POST['_target'])) : 'Elite Luxury Bookings Inquiry';
}

// Construct Telegram message if no raw text was passed
if (empty($rawText)) {
    $rawText = "🚀 NEW LEAD: " . $target . "\n\n";
    $rawText .= "👤 Name: " . ($name ? $name : "Not Provided") . "\n";
    $rawText .= "✉️ Email: " . ($email ? $email : "Not Provided") . "\n";
    $rawText .= "📞 Phone/WhatsApp: " . ($phone ? $phone : "Not Provided") . "\n";
    $rawText .= "🛫 Departure: " . ($departure ? $departure : "Not Provided") . "\n";
    $rawText .= "🛬 Destination: " . ($destination ? $destination : "Not Provided") . "\n";
    if (!empty($date)) {
        $rawText .= "📅 Date: " . $date . "\n";
    }
    if (!empty($passengers)) {
        $rawText .= "👥 Passengers: " . $passengers . "\n";
    }
    $rawText .= "📋 Requirements: " . (!empty($requirements) ? $requirements : "None") . "\n\n";
    $rawText .= "🌐 Source IP: " . $_SERVER['REMOTE_ADDR'] . "\n";
    $rawText .= "📅 Date/Time: " . date("Y-m-d H:i:s") . " UTC";
}

// Send to Telegram securely
$telegram_url = "https://api.telegram.org/bot" . $telegram_bot_token . "/sendMessage";
$data = [
    'chat_id' => $telegram_chat_id,
    'text' => $rawText
];

// If message looks like HTML format, specify parse_mode
if (stripos($rawText, '<b>') !== false || stripos($rawText, '<i>') !== false) {
    $data['parse_mode'] = 'HTML';
}

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $telegram_url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Send secure backup notification to FormSubmit if not raw text
if (empty($rawText) || !empty($email) || !empty($name)) {
    $email_backup_url = 'https://formsubmit.co/ajax/contactshaikk@gmail.com';
    $email_data = [
        'name' => $name ? $name : 'Inquiry Client',
        'email' => $email ? $email : 'no-email@eliteluxurybookings.com',
        'phone' => $phone,
        'departure' => $departure,
        'destination' => $destination,
        'date' => $date,
        'passengers' => $passengers,
        'requirements' => $requirements,
        '_subject' => "New Lead from {$target}"
    ];

    $ch_email = curl_init();
    curl_setopt($ch_email, CURLOPT_URL, $email_backup_url);
    curl_setopt($ch_email, CURLOPT_POST, true);
    curl_setopt($ch_email, CURLOPT_POSTFIELDS, json_encode($email_data));
    curl_setopt($ch_email, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch_email, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch_email, CURLOPT_SSL_VERIFYPEER, false);
    curl_exec($ch_email);
    curl_close($ch_email);
}

if ($http_code === 200) {
    http_response_code(200);
    echo json_encode(["status" => "success", "message" => "Lead securely dispatched."]);
} else {
    http_response_code(502);
    echo json_encode([
        "status" => "error", 
        "message" => "Telegram API error: HTTP " . $http_code,
        "details" => json_decode($response, true)
    ]);
}
?>
