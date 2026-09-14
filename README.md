# log-sift

Parse application / access logs and summarize status codes, top endpoints, and error samples.

## Run

```powershell
python src\log_sift.py --file samples\app.log
```

JSON output:

```powershell
python src\log_sift.py --file samples\app.log --json
```

## Options

- `--file` — log file to analyze (required)
- `--json` — emit a JSON summary instead of plain text

## Exit codes

- `0` — report generated successfully
- `2` — log file not found

## License

MIT
