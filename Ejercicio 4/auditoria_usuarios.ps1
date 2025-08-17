#Script de auditoría básica de usuarios - Cristian Bravo

$usuarios = Get-LocalUser
$sinLogon = @()
$conLogon = @()

ForEach($u in $usuarios){

    if(-not $u.LastLogon){

        $sinLogon += "$($u.Name): Estado = $($u.Enabled), Último acceso = NUNCA"

    } else {

        $conLogon += "$($u.Name): Estado = $($u.Enabled), Último acceso = $($u.LastLogon)"
    }
}

$sinLogon | Out-File -FilePath "C:\Users\Cris\Desktop\Practicas\sin_logon.txt"
$conLogon | Out-File -FilePath "C:\Users\Cris\Desktop\Practicas\con_logon.txt"

Write-Output " "
Write-Output "------------------------- Auditoria -------------------------"
Write-Output " "
Write-Output " + Usuarios que NUNCA han iniciado sesión:"
Write-Output " "
$sinLogon | ForEach-Object {Write-Output "`t - $($_)"}

Write-Output " "
Write-Output " + Usuarios que SÍ han iniciado sesión:"
Write-Output " "
$conLogon | ForEach-Object {Write-Output "`t - $($_)"}