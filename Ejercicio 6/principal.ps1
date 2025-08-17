Clear-Host
Import-Module AuditoriaBasica

Write-Host "=== Auditoría básica de usuarios y servicios ==="
Write-Host "1. Mostrar usuarios inactivos"
Write-Host "2. Mostrar servicios externos activos"
$opcion = Read-Host "Selecciona una opción (1 o 2)"

switch($opcion){
    "1"{
        $usuarios = Obtener-UsuariosInactivos
        $usuarios | Format-Table Name, Enabled, LastLogon -AutoSize
        $usuarios | Export-Csv -Path "$env:USERPROFILE\Desktop\Practicas\E6\users_inac.csv" -NoTypeInformation
        Write-Host "Reporte generado: ussers_inac.csv"
    }
    "2"{
        $servicios = Obtener-ServiciosExternos
        $servicios | Format-Table DisplayName, Status, StartType -AutoSize
        $servicios | ConvertTo-Html | Out-File "$env:USERPROFILE\Desktop\Practicas\E6\serv_e.html"
        Write-Host "Reporte generado: serv_e.html"
    }
    default{
        Write-Host "Opción no válida"
    }
}
