<?php
session_start();
header('Content-Type: application/json; charset=utf-8');

// Permite se estiver logado como professor OU se for chamada local (localhost)
$is_professor = (isset($_SESSION['tipo_usuario']) && $_SESSION['tipo_usuario'] === 'professor');
$remote = $_SERVER['REMOTE_ADDR'] ?? '';
$is_local = in_array($remote, ['127.0.0.1', '::1', 'localhost']) || str_starts_with($remote, '192.168.') || str_starts_with($remote, '10.');

if (!$is_professor && !$is_local) {
    http_response_code(403);
    echo json_encode([
        'status' => 'error',
        'message' => 'Acesso negado. Apenas professores autenticados podem abrir o aplicativo.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

$dir = __DIR__;
$scriptPath = $dir . DIRECTORY_SEPARATOR . 'reclass_desktop.py';

if (!file_exists($scriptPath)) {
    http_response_code(404);
    echo json_encode([
        'status' => 'error',
        'message' => 'Arquivo reclass_desktop.py não encontrado.'
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// Procurar executável pythonw / python válido
$possiveis = [
    'C:\\Program Files\\PyManager\\pythonw.exe',
    'C:\\Users\\secre\\AppData\\Local\\Programs\\Python\\Python314\\pythonw.exe',
    'pythonw',
    'python'
];

$pyExe = 'pythonw';
foreach ($possiveis as $candidato) {
    if (file_exists($candidato)) {
        $pyExe = $candidato;
        break;
    }
}

// Criar/atualizar launch_reclass.bat para execução limpa e desanexada no Windows
$batFile = $dir . DIRECTORY_SEPARATOR . 'launch_reclass.bat';
$batContent = "@echo off\r\ncd /d \"%~dp0\"\r\nstart \"Reclass Desktop\" \"" . $pyExe . "\" \"%~dp0reclass_desktop.py\"\r\nexit\r\n";
file_put_contents($batFile, $batContent);

// Executar em segundo plano no Windows
$cmd = 'start "" /min "' . $batFile . '"';
pclose(popen($cmd, 'r'));

echo json_encode([
    'status' => 'success',
    'message' => 'Aplicativo Reclass Desktop iniciado com sucesso!',
    'protocol_url' => 'reclass://open'
], JSON_UNESCAPED_UNICODE);
