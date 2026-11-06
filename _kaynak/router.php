<?php
/**
 * YALNIZCA YEREL TEST İÇİN: .htaccess kurallarını PHP yerleşik sunucusunda taklit eder.
 * Kullanım (depo kökünde):  php -S localhost:8080 _kaynak/router.php
 */
$root = dirname(__DIR__);
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if (preg_match('#^/(_kaynak|inc|storage|\.git)(/|$)#', $path) || preg_match('#^/(README\.md|KURULUM\.md|\.gitignore)$#', $path)) {
    http_response_code(403); echo 'Forbidden'; return true;
}
$redirects = ['/turlar' => '/services', '/team' => '/about', '/index.html' => '/', '/en' => '/en/'];
if (isset($redirects[rtrim($path, '/')]) && $path !== '/en/') {
    header('Location: ' . $redirects[rtrim($path, '/')], true, 301); return true;
}
if (preg_match('#^(.+)\.html$#', $path, $m) && $path !== '/404.html') {
    header('Location: ' . $m[1], true, 301); return true;
}
if ($path === '/form.php') {
    require $root . '/form.php'; return true;
}
$file = $root . $path;
if ($path !== '/' && substr($path, -1) === '/' && !is_dir($file)) {
    header('Location: ' . rtrim($path, '/'), true, 301); return true;
}
if (is_dir($file) && is_file(rtrim($file, '/') . '/index.html')) {
    $file = rtrim($file, '/') . '/index.html';
} elseif (!is_file($file) && is_file($file . '.html')) {
    $file .= '.html';
}
if (is_file($file)) {
    $types = ['html' => 'text/html; charset=utf-8', 'css' => 'text/css', 'js' => 'application/javascript',
              'webp' => 'image/webp', 'jpg' => 'image/jpeg', 'png' => 'image/png', 'xml' => 'application/xml', 'txt' => 'text/plain'];
    $ext = pathinfo($file, PATHINFO_EXTENSION);
    header('Content-Type: ' . ($types[$ext] ?? 'application/octet-stream'));
    readfile($file); return true;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile($root . '/404.html');
return true;
