param(
    [string]$EnvFile = ".env"
)

$ErrorActionPreference = "Stop"

function Read-DotEnv {
    param([string]$Path)

    $values = @{}
    if (-not (Test-Path $Path)) {
        return $values
    }

    Get-Content $Path | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq "" -or $line.StartsWith("#") -or -not $line.Contains("=")) {
            return
        }

        $key, $value = $line.Split("=", 2)
        $values[$key.Trim()] = $value.Trim()
    }

    return $values
}

$envValues = Read-DotEnv $EnvFile

function Get-EnvValue {
    param([hashtable]$Values, [string]$Key, [string]$Default)

    if ($Values.ContainsKey($Key) -and $Values[$Key] -ne "") {
        return $Values[$Key]
    }

    return $Default
}

$dbName = Get-EnvValue $envValues "POSTGRES_DB" "SushiRoll"
$dbUser = Get-EnvValue $envValues "POSTGRES_USER" "postgres"
$dbPassword = Get-EnvValue $envValues "POSTGRES_PASSWORD" ""
$dbHost = Get-EnvValue $envValues "POSTGRES_HOST" "localhost"
$dbPort = Get-EnvValue $envValues "POSTGRES_PORT" "5433"

if ($dbPassword -ne "") {
    $env:PGPASSWORD = $dbPassword
}

$exists = psql -h $dbHost -p $dbPort -U $dbUser -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$dbName'"
if ($exists.Trim() -ne "1") {
    psql -h $dbHost -p $dbPort -U $dbUser -d postgres -c "CREATE DATABASE ""$dbName"""
}

& ".\.venv\Scripts\python.exe" manage.py migrate
& ".\.venv\Scripts\python.exe" manage.py ensure_superuser
