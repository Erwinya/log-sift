# log-sift

Parse application / access logs and summarize status codes, top endpoints, and error samples.

## Status

Status codes, top paths, log levels, error samples, and `--json` output are in place. Packaging / tests will land in follow-up commits.

## Run

```powershell
python src\log_sift.py --file samples\app.log
python src\log_sift.py --file samples\app.log --json
```

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
