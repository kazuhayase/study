# eMudhra / emSign CA key compromise — response notes (2026-10-24)

## Incident

In October 2026 the private keys of eight eMudhra intermediate CA certificates
were found to be trivially recoverable (P-384 keys generated in April 2025 with
values smaller than 256). Browsers blocked them on 17 October; eMudhra revoked
them on 18 October; Mozilla removed `emSign ECC Root CA - G3` from NSS.

This is **not** a PyPI or npm breach. The exposure is an attacker who can also
intercept traffic, which they could then do while posing as pypi.org or
python.org. Non-browser clients that carry their own CA bundle are the part
browsers cannot fix.

`pip` always loads its vendored `certifi` bundle **in addition to** the system
trust store, so refreshing the OS trust store alone does not help — pip itself
must be upgraded.

Primary source:
<https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576>

## Minimum fixed versions

| Tool | Minimum |
|---|---|
| certifi | 2026.10.19 |
| pip | 26.2.2 |
| uv | 0.13.4 |
| sigstore | 4.5.1 |
| pixi | 0.82.1 |
| conda | 26.9.4 |
| Node.js | 22.23.4 / 24.22.1 / 26.12.1 |

## State of this machine (Windows 11, 2026-10-24)

| Target | Before | After |
|---|---|---|
| Store Python 3.11.9 — pip | 24.0 | 26.2.2 |
| Store Python 3.11.9 — certifi | 2024.2.2 | 2026.10.23 |
| `LLM/act-MLS2024/python/sample-server/.venv` | pip 26.1, no certifi | pip 26.2.2, certifi 2026.10.23 |
| `LLM/DA-Elyza2024/python/sample-server/.venv` | pip 26.1, no certifi | pip 26.2.2, certifi 2026.10.23 |
| Node.js | 24.19.0 | 24.22.1 (npm 11.19.1) |

Repo manifests needed no change from here: `mls-seminar/requirements.txt`
(certifi==2026.10.23) and `LLM/model-compare/uv.lock` (certifi 2026.10.23) were
already fixed on the Debian machine in c978ae8, and this machine converged on
the same versions independently. `LLM/openmythos-test/uv.lock` has no certifi at
all — it resolves `truststore`, which defers to the OS trust store.

Not installed on this machine, so no action taken: `uv`, `pixi`, `conda`,
`sigstore`.

Windows trust stores (`LocalMachine\Root`, `\CA`, `CurrentUser\Root`, `\CA`)
contain no emSign or eMudhra certificates at all, so nothing to remove there.

Verified after the update: `emSign ECC Root CA - G3` is absent from every
certifi bundle and from Node's bundled roots. The `emSign Root CA - G1` entry
that remains is one of the unaffected roots that certifi 2026.10.19
deliberately restored.

## Known residual risk

The Microsoft Store Python 3.11 ships `ensurepip` with **pip 24.0**, and
patching it would mean writing into
`C:\Program Files\WindowsApps\...` (a Store app install). That was left alone.

Consequence: a plain `python -m venv` creates a venv with the vulnerable pip
24.0 again. Use the helper instead:

```powershell
./scripts/security/new-safe-venv.ps1 -Path .venv
```

It pins the pip and certifi wheel SHA256s (cross-checked against the advisory
and the PyPI JSON API) and installs with `--no-index`, so the stale pip never
validates a certificate chain.

## How to verify an environment

```bash
python -m pip --version
python -c "import certifi; from pip._vendor import certifi as v; print(certifi.__version__, v.__version__)"
node -e "const t=require('tls'),c=require('crypto');console.log(t.rootCertificates.filter(p=>/emSign|eMudhra/i.test(new c.X509Certificate(p).subject)).length)"
```
