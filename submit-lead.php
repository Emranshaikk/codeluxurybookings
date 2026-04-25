<?php
/**
 * Elite Luxury Bookings - Lead Handler & Telegram Notifier
 * Version: 1.0.0
 */

// --- CONFIGURATION ---
$TELEGRAM_TOKEN = '8274022771:AAHDPmDq6vfAttktCf1iOeNAwqSAuUFgP2g';
$TELEGRAM_CHAT_ID = '5875175296'; // Emranshaikk ID
$BACKUP_EMAIL = 'info@eliteluxurybookings.com';

// --- SECURITY ---
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *'); // Allow from your domain

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

// --- DATA EXTRACTION ---
$data = $_POST;
$form_type = isset($data['form_type']) ? $data['form_type'] : 'General Lead';

// Format the message
$message = "🚀 *New Elite Lead Received!* \n\n";
$message .= "*Type:* " . ucfirst($form_type) . "\n";

if (isset($data['route'])) $message .= "*Route:* " . $data['route'] . "\n";
if (isset($data['date'])) $message .= "*Date:* " . $data['date'] . "\n";
if (isset($data['passengers'])) $message .= "*Passengers:* " . $data['passengers'] . "\n";
if (isset($data['budget'])) $message .= "*Budget:* " . $data['budget'] . "\n";
if (isset($data['name'])) $message .= "*Name:* " . $data['name'] . "\n";
if (isset($data['phone'])) $message .= "*Phone:* " . $data['phone'] . "\n";
if (isset($data['email'])) $message .= "*Email:* " . $data['email'] . "\n";
if (isset($data['whatsapp_pref'])) $message .= "*WhatsApp Pref:* " . $data['whatsapp_pref'] . "\n";

$message .= "\n📅 " . date('Y-m-d H:i:s') . " (UTC)";

// --- TELEGRAM NOTIFICATION ---
function sendTelegram($token, $chat_id, $text) {
    $url = "https://api.telegram.org/bot$token/sendMessage";
    $params = [
        'chat_id' => $chat_id,
        'text' => $text,
        'parse_mode' => 'Markdown'
    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

// Only send if Chat ID is configured
if ($TELEGRAM_CHAT_ID !== 'CHANGE_THIS_TO_YOUR_ID') {
    sendTelegram($TELEGRAM_TOKEN, $TELEGRAM_CHAT_ID, $message);
}

// --- BACKUP EMAIL (Optional) ---
$headers = "From: leads@eliteluxurybookings.com\r\n";
$headers .= "Reply-To: " . (isset($data['email']) ? $data['email'] : $BACKUP_EMAIL) . "\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

mail($BACKUP_EMAIL, "New Lead: " . (isset($data['name']) ? $data['name'] : 'Inquiry'), str_replace('*', '', $message), $headers);

// --- RESPONSE ---
echo json_encode(['status' => 'success', 'message' => 'Lead captured successfully']);
