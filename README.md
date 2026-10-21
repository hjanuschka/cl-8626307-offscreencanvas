# OffscreenCanvas cross-process transfer repro

Repro for [crbug.com/40819284](https://issues.chromium.org/issues/40819284),
fixed by Chromium CL
[8626307](https://chromium-review.googlesource.com/c/chromium/src/+/8626307).

A canvas is moved to an `OffscreenCanvas` with
`transferControlToOffscreen()` and posted to an iframe on another site, so
the receiving document lives in a different renderer process. Drawing into
that canvas made the receiver hand the sending process' frame sink ids to
viz, and the browser killed it with `RESULT_CODE_KILLED_BAD_MESSAGE`
("Invalid client ID").

The page pings the child once per 300ms and shows whether it still answers.

## Run

```bash
python3 serve.py &
chrome --host-resolver-rules="MAP * 127.0.0.1" http://a.test:8765/parent.html
```

- Current Chrome: the status turns red, the child renderer is gone.
- With the CL: the status stays green; the transferred canvas is treated as
  standalone, so nothing reaches the placeholder canvas, but no renderer is
  killed.
