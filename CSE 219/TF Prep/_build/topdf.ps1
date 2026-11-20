param([string]$docx, [string]$pdf)
$w = New-Object -ComObject Word.Application; $w.Visible = $false
try { $d = $w.Documents.Open($docx, $false, $true); $d.SaveAs2($pdf, 17); $d.Close($false) } finally { $w.Quit() }
