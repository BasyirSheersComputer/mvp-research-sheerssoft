$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("H:\Source\repos\mvp-research-floyd\The Hospitality Revenue & Operational Blueprint - ver. Floyd_responses.docx")
$doc.Content.Text | Out-File "H:\Source\repos\mvp-research-floyd\blueprint_text.txt" -Encoding UTF8
$doc.Close()
$word.Quit()
