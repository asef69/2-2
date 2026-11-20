param([string]$Docx, [string]$Pdf)
$w = $null
for ($i = 0; $i -lt 4; $i++) {
  try {
    $w = New-Object -ComObject Word.Application
    $w.Visible = $false
    $d = $w.Documents.Open($Docx, $false, $true)
    $d.SaveAs2($Pdf, 17)
    $d.Close($false)
    $w.Quit()
    Write-Output "ok $Pdf"
    break
  } catch {
    Write-Output "retry: $_"
    if ($w) { try { $w.Quit() } catch {} }
    Start-Sleep -Seconds 20
  }
}
