
$replacement='DataRouterUrl="' + $args[0] + '"'

$filename2="C:/UnrealEngine/Engine/Programs/CrashReportClient/Config/DefaultEngine.ini"
Set-ItemProperty -Path $filename2 -Name IsReadOnly -Value $false
((Get-Content $filename2) `
    | ForEach-Object{ $_ -replace '\s*DataRouterUrl\s*=.*$', $replacement }).Trim() `
    | Set-Content $filename2
