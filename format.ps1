$argList = "format .\src\megaman-x8-tools\"
Start-Process "poetry run ruff" -ArgumentList $argList -Wait -NoNewWindow