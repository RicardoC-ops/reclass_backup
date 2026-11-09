<?php

include_once("conexao.php");

$titulo = $_POST['titulo'];
$data = $_POST['data'];
$horario = $_POST['horario'];
$vagas = $_POST['vagas'];
$unidade = $_POST['unidade'];
$observacoes = $_POST['observacoes'];


$sql = "INSERT INTO aulas 
(titulo, data, horario, vagas, unidade, observacoes)

VALUES

('$titulo',
'$data',
'$horario',
'$vagas',
'$unidade',
'$observacoes')";


if(mysqli_query($conn,$sql)){

    header("Location: tdsaulas.php");
    exit;

}else{

    echo "Erro: ".mysqli_error($conn);

}

?>