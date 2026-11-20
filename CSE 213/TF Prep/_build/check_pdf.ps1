param([string]$name, [string]$pages = "1-9")
# Converts notes\<name>.docx to a PDF in the scratchpad and makes a contact sheet of the given pages.
$S = "C:\Users\Lenovo\AppData\Local\Temp\claude\C--Users-Lenovo-OneDrive-Desktop-Academics-2-2\4af4348d-82fd-42c2-91a3-457e99c48f65\scratchpad"
$root = "C:\Users\Lenovo\OneDrive\Desktop\Academics\2-2"
$pdf = "$S\$name.pdf"
$w = New-Object -ComObject Word.Application; $w.Visible = $false
$d = $w.Documents.Open("$root\CSE 213\TF Prep\notes\$name.docx", $false, $true)
$d.SaveAs2($pdf, 17); $d.Close($false); $w.Quit()
$a, $b = $pages.Split("-")
python -P "$root\_tfprep\tools.py" sheet $pdf "$S\$name.png" $a $b --cols 3 --dpi 50
python -P -c "import pymupdf;print('pages',pymupdf.open(r'$pdf').page_count)"
