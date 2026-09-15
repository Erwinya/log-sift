# log-sift

Parse application / access logs and summarize status codes, top endpoints, and error samples.

## Status

CLI scaffolding and log file loading are in place. Status/path parsing and JSON reports will land in follow-up commits.

## Run (current)

```powershell
python src\log_sift.py --file samples\app.log
```

Prints file path, byte size, and non-empty line count. Exit `2` if the file is missing.

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
