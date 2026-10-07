# log-sift

Parse application / access logs and summarize status codes, top endpoints, and error samples.

## Status

Ready for use: analysis, `--json`, packaging, unit tests, and CI.

## Run

```powershell
python src\log_sift.py --file samples\app.log
python src\log_sift.py --file samples\app.log --json
```

Install locally (optional):

```powershell
pip install -e .
log-sift --file samples\app.log
```

## Development

```powershell
pip install -e ".[dev]"
pytest
```

## Exit codes

- `0` — success
- `2` — file not found / usage error

In PowerShell, check `$LASTEXITCODE` after a run:

```powershell
python src\log_sift.py --file samples\app.log
if ($LASTEXITCODE -ne 0) { Write-Error "log-sift failed with exit code $LASTEXITCODE" }
```

## Requirements

- Python 3.10+
- Standard library only (pytest optional for tests)

## License

MIT
