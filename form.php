<?php
/**
 * Atlantis Travel – teklif, fuar ve iletişim formu işleyicisi.
 * Veriler kaydedilmez; yalnızca e-posta olarak iletilir.
 */
declare(strict_types=1);
date_default_timezone_set('Europe/Istanbul');

$cfg = require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/mailer.php';

header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false
    || ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') !== '';
$lang = (($_POST['lang'] ?? '') === 'en') ? 'en' : 'tr';

$M = [
    'tr' => [
        'method'  => 'Geçersiz istek.',
        'invalid' => 'Lütfen zorunlu alanları eksiksiz ve doğru doldurun.',
        'rate'    => 'Çok fazla deneme yapıldı. Lütfen birkaç dakika sonra tekrar deneyin veya WhatsApp üzerinden yazın.',
        'fail'    => 'Talebiniz şu anda gönderilemedi. Lütfen WhatsApp veya telefonla bize ulaşın.',
        'ok'      => 'Teşekkürler, talebiniz alındı. Ekibimiz en kısa sürede size dönüş yapacak.',
    ],
    'en' => [
        'method'  => 'Invalid request.',
        'invalid' => 'Please complete the required fields correctly.',
        'rate'    => 'Too many attempts. Please try again in a few minutes or write to us on WhatsApp.',
        'fail'    => 'Your request could not be sent right now. Please contact us via WhatsApp or phone.',
        'ok'      => 'Thank you, your request has been received. Our team will get back to you shortly.',
    ],
][$lang];

function respond(bool $ok, string $msg, bool $json, string $lang, int $code = 200): void
{
    if ($json) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $msg], JSON_UNESCAPED_UNICODE);
        exit;
    }
    // JavaScript kapalıysa: teşekkür sayfasına ya da geri yönlendir
    if ($ok) {
        header('Location: ' . ($lang === 'en' ? '/en/thank-you' : '/tesekkurler'), true, 303);
    } else {
        $back = $lang === 'en' ? '/en/request-a-quote' : '/teklif-al';
        header('Location: ' . $back . '?hata=1', true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(false, $M['method'], true, $lang, 405);
}

// Aynı sitedan gelmeyen gönderimleri reddet (Origin/Referer kontrolü)
$host = $_SERVER['HTTP_HOST'] ?? '';
$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
if ($origin !== '' && parse_url($origin, PHP_URL_HOST) !== parse_url('http://' . $host, PHP_URL_HOST)) {
    respond(false, $M['method'], $wantsJson, $lang, 403);
}

// Bot koruması: gizli alan dolu ise veya form çok hızlı gönderildiyse sessizce "başarılı" de
$honeypot = trim((string) ($_POST['website'] ?? ''));
$ts = (int) ($_POST['ts'] ?? 0);
$elapsed = $ts > 0 ? (time() * 1000 - $ts) / 1000 : 999;
if ($honeypot !== '' || $elapsed < $cfg['min_fill_seconds']) {
    respond(true, $M['ok'], $wantsJson, $lang);
}

// IP başına gönderim sınırı (IP adresi saklanmaz, yalnızca özeti)
$store = __DIR__ . '/storage';
if (!is_dir($store)) {
    @mkdir($store, 0750, true);
}
$ipKey = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . '|atlantis');
$rateFile = $store . '/rate_' . substr($ipKey, 0, 32) . '.json';
$now = time();
$hits = [];
if (is_file($rateFile)) {
    $hits = json_decode((string) @file_get_contents($rateFile), true) ?: [];
}
$hits = array_values(array_filter($hits, fn($t) => is_int($t) && $t > $now - $cfg['rate_limit_seconds']));
if (count($hits) >= $cfg['rate_limit_max']) {
    respond(false, $M['rate'], $wantsJson, $lang, 429);
}

// Alanlar
$f = function (string $k, int $max = 200): string {
    $v = (string) ($_POST[$k] ?? '');
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr(trim($v), 0, $max);
};

$type = in_array($_POST['form_type'] ?? '', ['teklif', 'fuar', 'iletisim'], true) ? $_POST['form_type'] : 'teklif';
$data = [
    'company'    => $f('company', 150),
    'name'       => $f('name', 120),
    'email'      => $f('email', 160),
    'phone'      => $f('phone', 30),
    'service'    => $f('service', 60),
    'date_start' => $f('date_start', 10),
    'date_end'   => $f('date_end', 10),
    'guests'     => $f('guests', 5),
    'rooms'      => $f('rooms', 5),
    'fair_name'  => $f('fair_name', 150),
    'subject'    => $f('subject', 150),
    'message'    => $f('message', 3000),
];
$consent = !empty($_POST['kvkk']);

$required = [
    'teklif'   => ['company', 'name', 'email', 'phone', 'service'],
    'fuar'     => ['name', 'email', 'phone', 'fair_name', 'guests', 'date_start', 'date_end'],
    'iletisim' => ['name', 'email', 'message'],
][$type];

$errors = [];
foreach ($required as $k) {
    if ($data[$k] === '') $errors[] = $k;
}
if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'email';
if ($data['phone'] !== '' && !preg_match('/^[+0-9()\s\-]{7,20}$/', $data['phone'])) $errors[] = 'phone';
foreach (['date_start', 'date_end'] as $d) {
    if ($data[$d] !== '' && !preg_match('/^\d{4}-\d{2}-\d{2}$/', $data[$d])) $errors[] = $d;
}
if ($data['date_start'] !== '' && $data['date_end'] !== '' && $data['date_end'] < $data['date_start']) $errors[] = 'date_end';
foreach (['guests', 'rooms'] as $n) {
    if ($data[$n] !== '' && (!ctype_digit($data[$n]) || (int) $data[$n] < 1 || (int) $data[$n] > 5000)) $errors[] = $n;
}
$services = ['kurumsal-konaklama', 'vip-transfer', 'saglik-turizmi', 'fuar-konaklama', 'grup-heyet', 'diger'];
if ($data['service'] !== '' && !in_array($data['service'], $services, true)) $errors[] = 'service';
if (!$consent) $errors[] = 'kvkk';

if ($errors) {
    respond(false, $M['invalid'], $wantsJson, $lang, 422);
}

// E-posta içeriği
$serviceNames = [
    'kurumsal-konaklama' => 'Kurumsal otel konaklama',
    'vip-transfer'       => 'VIP havalimanı transferi',
    'saglik-turizmi'     => 'Sağlık turizmi konaklama / transfer',
    'fuar-konaklama'     => 'Fuar konaklama',
    'grup-heyet'         => 'Grup, heyet veya spor takımı',
    'diger'              => 'Diğer',
];
$titles = ['teklif' => 'Yeni teklif talebi', 'fuar' => 'Yeni fuar konaklama talebi', 'iletisim' => 'Yeni iletişim mesajı'];
$labels = [
    'company' => 'Şirket / kurum', 'name' => 'Ad soyad / yetkili kişi', 'email' => 'E-posta', 'phone' => 'Telefon',
    'service' => 'Talep edilen hizmet', 'fair_name' => 'Fuar adı', 'date_start' => 'Başlangıç / giriş tarihi',
    'date_end' => 'Bitiş / çıkış tarihi', 'guests' => 'Kişi sayısı', 'rooms' => 'Oda sayısı',
    'subject' => 'Konu', 'message' => 'Açıklama / mesaj',
];
$lines = [$titles[$type] . ' – atlantistravel web sitesi', str_repeat('-', 48)];
foreach ($labels as $k => $label) {
    if ($data[$k] === '') continue;
    $v = $k === 'service' ? ($serviceNames[$data[$k]] ?? $data[$k]) : $data[$k];
    $lines[] = $label . ': ' . $v;
}
$lines[] = str_repeat('-', 48);
$lines[] = 'Form dili: ' . strtoupper($lang) . ' · KVKK onayı: Evet · Tarih: ' . date('d.m.Y H:i');

$subjectParts = [$titles[$type]];
if ($data['company'] !== '') $subjectParts[] = $data['company'];
elseif ($data['name'] !== '') $subjectParts[] = $data['name'];
$subject = implode(' – ', $subjectParts);

if (($cfg['transport'] ?? 'mail') === 'dryrun') {
    // Yalnızca yerel test içindir: e-posta yerine dosyaya yazar.
    @file_put_contents($store . '/outbox_last.txt', 'Subject: ' . $subject . "\n\n" . implode("\n", $lines));
    $sent = [true, ''];
} else {
    $sent = at_send_mail($cfg, $subject, implode("\n", $lines), $data['email'], $data['name']);
}

if (!$sent[0]) {
    error_log('Atlantis form: ' . $sent[1]);
    respond(false, $M['fail'], $wantsJson, $lang, 502);
}

$hits[] = $now;
@file_put_contents($rateFile, json_encode($hits), LOCK_EX);
respond(true, $M['ok'], $wantsJson, $lang);
