<?php
/**
 * Atlantis Travel – form ayarları.
 * Şifre gibi gizli bilgileri BU dosyaya yazmayın. Onlar için aynı klasörde
 * config.local.php oluşturun (config.local.example.php'yi kopyalayın).
 * config.local.php Git'e gönderilmez (.gitignore).
 */
$config = [
    // Taleplerin gideceği adres
    'to_email'   => 'info@atlantistraveltr.com',
    'to_name'    => 'Atlantis Travel',

    // Gönderen adres. Sunucunun kendi alan adında bir adres olmalı.
    // Boş bırakılırsa noreply@<site alan adı> kullanılır.
    'from_email' => 'emrah@atlantistravel.com.tr',
    'from_name'  => 'Atlantis Travel Web Sitesi',

    // 'mail'  : PHP mail() (Hostinger'da ek ayar gerektirmez)
    // 'smtp'  : Bir e-posta hesabıyla SMTP üzerinden (daha güvenilir teslimat)
    'transport'  => 'mail',
    'smtp' => [
        'host'   => 'smtp.hostinger.com',
        'port'   => 465,          // 465 = SSL
        'user'   => '',           // config.local.php içinde doldurun
        'pass'   => '',           // config.local.php içinde doldurun
    ],

    // Kötüye kullanım sınırı: aynı IP'den belirli sürede en fazla gönderim
    'rate_limit_max'     => 5,
    'rate_limit_seconds' => 600,
    // Formun en az kaç saniye sonra gönderilebileceği (bot koruması)
    'min_fill_seconds'   => 3,
];

$local = __DIR__ . '/config.local.php';
if (is_file($local)) {
    $override = require $local;
    if (is_array($override)) {
        $config = array_replace_recursive($config, $override);
    }
}
return $config;
