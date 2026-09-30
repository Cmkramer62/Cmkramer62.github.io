"""Serve this static portfolio locally with byte-range support for video seeking."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import re


class RangeRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def send_head(self):
        self._range_length = None
        range_header = self.headers.get("Range")
        if not range_header or not range_header.startswith("bytes="):
            return super().send_head()

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()

        try:
            file_handle = open(path, "rb")
        except OSError:
            return super().send_head()

        size = os.fstat(file_handle.fileno()).st_size
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
        if not match:
            return self._reject_range(file_handle, size)

        first, last = match.groups()
        if first:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        elif last:
            suffix_length = int(last)
            if suffix_length == 0:
                return self._reject_range(file_handle, size)
            start = max(0, size - suffix_length)
            end = size - 1
        else:
            return self._reject_range(file_handle, size)

        if start >= size or start > end:
            return self._reject_range(file_handle, size)

        length = end - start + 1
        self.send_response(206)
        self.send_header("Content-type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(length))
        self.send_header("Last-Modified", self.date_time_string(os.fstat(file_handle.fileno()).st_mtime))
        self.end_headers()
        file_handle.seek(start)
        self._range_length = length
        return file_handle

    def _reject_range(self, file_handle, size):
        file_handle.close()
        self.send_response(416)
        self.send_header("Content-Range", f"bytes */{size}")
        self.send_header("Content-Length", "0")
        self.end_headers()
        return None

    def copyfile(self, source, outputfile):
        if self._range_length is None:
            return super().copyfile(source, outputfile)

        remaining = self._range_length
        while remaining:
            block = source.read(min(64 * 1024, remaining))
            if not block:
                break
            outputfile.write(block)
            remaining -= len(block)


if __name__ == "__main__":
    site_root = Path(__file__).resolve().parent
    handler = partial(RangeRequestHandler, directory=str(site_root))
    server = ThreadingHTTPServer(("127.0.0.1", 8000), handler)
    print(f"Serving {site_root} at http://localhost:8000 (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
