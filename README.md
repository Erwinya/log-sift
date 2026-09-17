# log-sift

Parse application / access logs and summarize status codes, top endpoints, and error samples.

## Status

Status-code and top-path parsing are in place. Level/error samples and `--json` output will land in follow-up commits.

## Run

```powershell
python src\log_sift.py --file samples\app.log
```

## Requirements

- Python 3.10+
- Standard library only

## License

MIT
