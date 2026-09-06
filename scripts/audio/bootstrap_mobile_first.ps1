$ErrorActionPreference = 'Stop'

$Repo = 'zufkin/zmierenie-listening-edition'
$LegacyDir = 'C:\Users\zufki\Claude\Projects\web tf.truni.sk\scripts\listening-edition'
$EnvFile = Join-Path $LegacyDir '.env'

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'GitHub CLI (gh) is not installed or not on PATH.'
}

& gh auth status | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw 'GitHub CLI is not authenticated.'
}

if (-not (Test-Path -LiteralPath $EnvFile)) {
    throw 'Legacy ElevenLabs .env was not found.'
}

$line = Get-Content -LiteralPath $EnvFile | Where-Object { $_ -match '^\s*ELEVENLABS_API_KEY\s*=' } | Select-Object -First 1
if (-not $line) {
    throw 'ELEVENLABS_API_KEY was not found in the legacy .env.'
}

$value = ($line -replace '^\s*ELEVENLABS_API_KEY\s*=\s*', '').Trim()
if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
    $value = $value.Substring(1, $value.Length - 2)
}
if ([string]::IsNullOrWhiteSpace($value)) {
    throw 'ELEVENLABS_API_KEY is empty.'
}

# gh reads the secret from standard input when --body is omitted.
# The secret is never written to stdout, source code, Drive, or a receipt.
$value | & gh secret set ELEVENLABS_API_KEY --repo $Repo --app actions
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to set the managed GitHub Actions secret.'
}

$verified = & gh secret list --repo $Repo --app actions --json name --jq '.[] | select(.name=="ELEVENLABS_API_KEY") | .name'
if ($verified -ne 'ELEVENLABS_API_KEY') {
    throw 'Secret name readback failed.'
}

Write-Output 'MOBILE_FIRST_SECRET_BOOTSTRAP_PASS'
