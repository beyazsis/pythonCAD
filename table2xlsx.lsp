(defun c:table2xlsx ()
 (command "._shell" "powershell -WindowStyle Hidden -Command \"Start-Process python.exe -ArgumentList 'C:\\python-cad\\table-xlsx.py' -NoNewWindow -RedirectStandardOutput table2xlsx.output -RedirectStandardError table2xlsx.error\"")
)
