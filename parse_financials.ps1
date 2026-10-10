
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Read-ExcelText($filePath) {
    $zip = [System.IO.Compression.ZipFile]::OpenRead($filePath)
    $sstEntry = $zip.GetEntry('xl/sharedStrings.xml')
    $sst = @()
    if ($sstEntry) {
        $stream = $sstEntry.Open()
        $reader = New-Object System.IO.StreamReader($stream)
        $xml = [xml]$reader.ReadToEnd()
        $stream.Close()
        foreach ($si in $xml.sst.si) {
            $sst += $si.InnerText
        }
    }
    
    $sheetEntry = $zip.GetEntry('xl/worksheets/sheet1.xml')
    $stream = $sheetEntry.Open()
    $reader = New-Object System.IO.StreamReader($stream)
    $sheetXml = [xml]$reader.ReadToEnd()
    $stream.Close()
    $zip.Dispose()

    Write-Output "=== $filePath ==="
    foreach ($row in $sheetXml.worksheet.sheetData.row) {
        $parts = @()
        foreach ($c in $row.c) {
            $val = $c.v
            if ($c.t -eq 's' -and $val -ne $null) {
                $idx = [int]$val
                $val = $sst[$idx]
            }
            $parts += ($c.r + ": " + $val)
        }
        Write-Output ("Row " + $row.r + " -> " + ($parts -join " ; "))
    }
}

Read-ExcelText "C:\ANDINA_ARCHIVOS\ARCHIVO\estado_de_resultados.xlsx"
Write-Output "`n-----------------------------------------`n"
Read-ExcelText "C:\ANDINA_ARCHIVOS\ARCHIVO\balance_general.xlsx"
Write-Output "`n-----------------------------------------`n"
Read-ExcelText "C:\ANDINA_ARCHIVOS\ARCHIVO\estado_flujo_efectivo.xlsx"
