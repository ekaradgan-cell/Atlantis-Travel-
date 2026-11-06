<?php
/**
 * Küçük, bağımlılıksız e-posta gönderici: PHP mail() veya SMTP (SSL/STARTTLS, AUTH LOGIN).
 */

function at_clean_header(string $v): string
{
    return trim(str_replace(["\r", "\n", "\0"], ' ', $v));
}

function at_encode_header(string $v): string
{
    return '=?UTF-8?B?' . base64_encode($v) . '?=';
}

/**
 * @return array{0:bool,1:string} [başarılı mı, hata açıklaması]
 */
function at_send_mail(array $cfg, string $subject, string $body, string $replyTo = '', string $replyName = ''): array
{
    $host = preg_replace('/[^a-z0-9.\-]/i', '', $_SERVER['HTTP_HOST'] ?? 'localhost');
    $host = preg_replace('/^www\./i', '', $host);
    $from = $cfg['from_email'] !== '' ? $cfg['from_email'] : ('noreply@' . $host);
    $from = at_clean_header($from);
    $to   = at_clean_header($cfg['to_email']);

    $headers = [
        'From: ' . at_encode_header($cfg['from_name']) . ' <' . $from . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
        'X-Mailer: AtlantisTravel-Site',
    ];
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $headers[] = 'Reply-To: ' . ($replyName !== '' ? at_encode_header(at_clean_header($replyName)) . ' ' : '')
            . '<' . at_clean_header($replyTo) . '>';
    }
    $encSubject = at_encode_header(at_clean_header($subject));
    $body = str_replace(["\r\n", "\r"], "\n", $body);

    if (($cfg['transport'] ?? 'mail') === 'smtp') {
        return at_smtp_send($cfg['smtp'], $from, $to, $encSubject, $headers, $body);
    }

    $ok = @mail($to, $encSubject, str_replace("\n", "\r\n", $body), implode("\r\n", $headers), '-f' . $from);
    return [$ok, $ok ? '' : 'mail() başarısız'];
}

function at_smtp_send(array $s, string $from, string $to, string $encSubject, array $headers, string $body): array
{
    if (($s['user'] ?? '') === '' || ($s['pass'] ?? '') === '') {
        return [false, 'SMTP kullanıcı/şifre tanımlı değil'];
    }
    $port = (int) ($s['port'] ?? 465);
    $remote = ($port === 465 ? 'ssl://' : 'tcp://') . $s['host'] . ':' . $port;
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client($remote, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) {
        return [false, 'SMTP bağlantı hatası'];
    }
    stream_set_timeout($fp, 15);

    $read = function () use ($fp): string {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) {
            $data .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') break;
        }
        return $data;
    };
    $cmd = function (string $c, array $okCodes) use ($fp, $read): bool {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        return in_array((int) substr($r, 0, 3), $okCodes, true);
    };

    $ehloHost = preg_replace('/[^a-z0-9.\-]/i', '', $_SERVER['HTTP_HOST'] ?? 'localhost');
    $steps = $cmd('', [220]) && $cmd('EHLO ' . $ehloHost, [250]);
    if ($steps && $port === 587) {
        $steps = $cmd('STARTTLS', [220])
            && stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)
            && $cmd('EHLO ' . $ehloHost, [250]);
    }
    $steps = $steps
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode($s['user']), [334])
        && $cmd(base64_encode($s['pass']), [235])
        && $cmd('MAIL FROM:<' . $from . '>', [250])
        && $cmd('RCPT TO:<' . $to . '>', [250, 251])
        && $cmd('DATA', [354]);

    if (!$steps) {
        fclose($fp);
        return [false, 'SMTP oturum hatası'];
    }

    $msg = 'To: <' . $to . ">\r\n"
        . 'Subject: ' . $encSubject . "\r\n"
        . 'Date: ' . date('r') . "\r\n"
        . 'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . substr(strrchr($from, '@'), 1) . ">\r\n"
        . implode("\r\n", $headers) . "\r\n\r\n";
    $lines = explode("\n", $body);
    foreach ($lines as $l) {
        $msg .= (isset($l[0]) && $l[0] === '.' ? '.' : '') . $l . "\r\n";
    }
    $ok = $cmd($msg . '.', [250]);
    $cmd('QUIT', [221]);
    fclose($fp);
    return [$ok, $ok ? '' : 'SMTP gönderim hatası'];
}
