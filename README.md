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

## Requirements

- Python 3.10+
- Standard library only (pytest optional for tests)

## License

MIT
