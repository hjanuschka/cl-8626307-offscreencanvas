#!/usr/bin/env python3
"""Serves this directory on port 8765 for the cross-site repro.

Chrome needs the parent and the child on different sites, so start it with
both hostnames pointed at this server:

    python3 serve.py &
    chrome --host-resolver-rules="MAP * 127.0.0.1" \
           http://a.test:8765/parent.html
"""

import functools
import http.server
import os

PORT = 8765

handler = functools.partial(
    http.server.SimpleHTTPRequestHandler,
    directory=os.path.dirname(os.path.abspath(__file__)),
)
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler).serve_forever()
