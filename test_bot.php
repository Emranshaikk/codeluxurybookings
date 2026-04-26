<?php
/**
 * Elite Luxury Bookings - Telegram Bot Tester
 * Run this by visiting: yourdomain.com/test_bot.php
 */

$TELEGRAM_TOKEN = '8274022771:AAHDPmDq6vfAttktCf1iOeNAwqSAuUFgP2g';
$TELEGRAM_CHAT_ID = '5875175296';

echo "<h1>Telegram Bot Connectivity Test</h1>";
echo "Sending test message to ID: $TELEGRAM_CHAT_ID...<br>";

$url = "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage";
$params = [
    'chat_id' => $TELEGRAM_CHAT_ID,
    'text' => "🔔 <b>Test Notification</b>\nIf you see this, your Elite Luxury Bookings lead system is correctly connected to Telegram!",
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
    echo "<h2 style='color:red;'>CURL Error: $err</h2>";
    echo "This usually means your server's firewall is blocking the connection to Telegram.";
} else {
    $res = json_decode($response, true);
    if ($res && isset($res['ok']) && $res['ok']) {
        echo "<h2 style='color:green;'>SUCCESS!</h2>";
        echo "The message was sent. Check your Telegram!";
    } else {
        echo "<h2 style='color:red;'>TELEGRAM ERROR:</h2>";
        echo "<pre>" . print_r($res, true) . "</pre>";
        echo "<br><b>IMPORTANT:</b> Make sure you have messaged the bot <b>@Elbleads_bot</b> and clicked <b>START</b> first.";
    }
}
