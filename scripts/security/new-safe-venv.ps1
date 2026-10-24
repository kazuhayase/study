<#
.SYNOPSIS
    Create a virtualenv with a pip/certifi that do NOT trust the compromised
    eMudhra "emSign ECC Root CA - G3" intermediate CA keys.

.DESCRIPTION
    Background: in October 2026 the private keys of eight eMudhra intermediate
    CAs were found to be trivially recoverable. pip always loads its own
    vendored certifi bundle in addition to the system trust store, so updating
    the OS trust store is not enough -- pip itself must be >= 26.2.2.

    This machine's Python ships ensurepip with pip 24.0, so a plain
    `python -m venv` re-introduces the vulnerable pip every time. This script
    creates the venv and then immediately replaces pip and certifi from wheels
    whose SHA256 is pinned below, matching the hash published in the Python
    advisory. The hash check means the download does not depend on TLS trust at
    all, and the install runs with --no-index so the stale pip that ensurepip
    dropped in never opens a TLS connection of its own.

.PARAMETER Path
    Directory of the venv to create. Defaults to .venv in the current directory.

.EXAMPLE
    ./scripts/security/new-safe-venv.ps1 -Path .venv

.LINK
    https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576
#>
param(
    [string]$Path = ".venv",
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

# Pinned artifacts. Hashes are from the Python security advisory and were
# cross-checked against the PyPI JSON API.
$artifacts = @(
    @{
        Name = "pip-26.2.2-py3-none-any.whl"
        Url  = "https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl"
        Hash = "fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
    },
    @{
        Name = "certifi-2026.10.23-py3-none-any.whl"
        Url  = "https://files.pythonhosted.org/packages/32/d1/a3652fe2c19134d0d15922177821d863cbd7e842d53a21bbe7e8e3a1b5ac/certifi-2026.10.23-py3-none-any.whl"
        Hash = "e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1"
    }
)

$cache = Join-Path ([System.IO.Path]::GetTempPath()) "safe-pip-wheels"
New-Item -ItemType Directory -Force -Path $cache | Out-Null

foreach ($a in $artifacts) {
    $dest = Join-Path $cache $a.Name
    if (-not (Test-Path $dest)) {
        Write-Host "Downloading $($a.Name)"
        Invoke-WebRequest -Uri $a.Url -OutFile $dest -UseBasicParsing
    }
    $actual = (Get-FileHash -Path $dest -Algorithm SHA256).Hash.ToLower()
    if ($actual -ne $a.Hash) {
        Remove-Item $dest -Force
        throw "SHA256 mismatch for $($a.Name): expected $($a.Hash), got $actual"
    }
    Write-Host "Verified $($a.Name)"
}

Write-Host "Creating venv at $Path"
& $Python -m venv $Path
if ($LASTEXITCODE -ne 0) { throw "venv creation failed" }

$venvPython = Join-Path $Path "Scripts/python.exe"
if (-not (Test-Path $venvPython)) { $venvPython = Join-Path $Path "bin/python" }

# --no-index keeps this strictly local, so the pip that ensurepip installed is
# replaced without it ever validating a certificate chain.
Write-Host "Replacing pip and certifi from verified wheels"
& $venvPython -m pip install --no-index --find-links $cache --upgrade pip certifi
if ($LASTEXITCODE -ne 0) { throw "pip bootstrap failed" }

& $venvPython -m pip --version
& $venvPython -c "import certifi; from pip._vendor import certifi as v; print('certifi', certifi.__version__, '| pip vendored certifi', v.__version__)"
