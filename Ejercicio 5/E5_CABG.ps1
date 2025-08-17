function Validar-Archivo {
    param ([string]$Ruta)

    try{
        if (Test-Path $Ruta){

            $contenido = Get-Content $Ruta -ErrorAction Stop
            #Obtener el tamaño edl archivo
            $tamaño = $Ruta.Length
            return "Archivo encontrado. Tamaño: $tamaño bytes. Ruta: $Ruta"
        } else{

            throw "El archivo no existe"
        }
    }catch{

        return "Error $_"

    }finally{
        Write-Host "Validación finalizada para: $Ruta" -ForegroundColor Cyan
    }
}

#Prueba de funcion con archivo fake
Validar-Archivo -Ruta "C:\archivo_inexistente.txt"

#Prueba de función con archivo real
Validar-Archivo -Ruta "$env:USERPROFILE\Desktop\Practicas\E5\archivo.txt"