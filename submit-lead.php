<?php
/**
 * Elite Luxury Bookings - Lead Handler & Telegram Notifier
 * Version: 1.1.0
 */

// --- CONFIGURATION ---
$TELEGRAM_TOKEN = '8274022771:AAHDPmDq6vfAttktCf1iOeNAwqSAuUFgP2g';
$TELEGRAM_CHAT_ID = '5875175296'; 
$BACKUP_EMAIL = 'info@eliteluxurybookings.com';
$LOG_FILE = 'lead_handler_errors.log';

// --- SECURITY ---
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *'); 

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

// --- DATA EXTRACTION ---
$data = $_POST;
$form_type = isset($data['form_type']) ? $data['form_type'] : 'General Lead';

// --- HTML FORMATTING FOR TELEGRAM ---
$message = "🚀 <b>New Elite Lead Received!</b>\n\n";
$message .= "<b>Type:</b> " . htmlspecialchars(ucfirst($form_type)) . "\n";

$fields = [
    'route' => '📍 Route',
    'date' => '📅 Date',
    'passengers' => '👥 Passengers',
    'budget' => '💰 Budget',
    'name' => '👤 Name',
    'phone' => '📞 Phone',
    'email' => '✉️ Email',
    'whatsapp_pref' => '💬 WhatsApp Pref'
];

foreach ($fields as $key => $label) {
    if (isset($data[$key]) && !empty($data[$key])) {
        $message .= "<b>$label:</b> " . htmlspecialchars($data[$key]) . "\n";
    }
}

$message .= "\n⏰ " . date('Y-m-d H:i:s') . " UTC";

// --- TELEGRAM NOTIFICATION ---
function sendTelegram($token, $chat_id, $text, $log_file) {
    $url = "https://api.telegram.org/bot$token/sendMessage";
    $params = [
        'chat_id' => $chat_id,
        'text' => $text,
        'parse_mode' => 'HTML'
    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $err = curl_error($ch);
    curl_close($ch);

    if ($err) {
        file_put_contents($log_file, "[" . date('Y-m-d H:i:s') . "] CURL Error: $err\n", FILE_APPEND);
    } else {
        $res = json_decode($response, true);
        if (!$res || !isset($res['ok']) || !$res['ok']) {
            file_put_contents($log_file, "[" . date('Y-m-d H:i:s') . "] Telegram Error: " . $response . "\n", FILE_APPEND);
        }
    }
    return $response;
}

// Send Telegram
$tg_result = sendTelegram($TELEGRAM_TOKEN, $TELEGRAM_CHAT_ID, $message, $LOG_FILE);

// --- BACKUP EMAIL ---
$headers = "MIME-Version: 1.0" . "\r\n";
$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";
$headers .= "From: leads@eliteluxurybookings.com\r\n";
$headers .= "Reply-To: " . (isset($data['email']) ? $data['email'] : $BACKUP_EMAIL) . "\r\n";

$email_content = str_replace("\n", "<br>", $message);
mail($BACKUP_EMAIL, "New Lead: " . (isset($data['name']) ? $data['name'] : 'Inquiry'), $email_content, $headers);

// --- RESPONSE ---
echo json_encode(['status' => 'success', 'tg' => json_decode($tg_result)]);
