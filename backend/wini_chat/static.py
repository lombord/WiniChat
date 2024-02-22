"""Static file request handlers"""

import io
import os
import re
from django.http import HttpRequest, HttpResponse
from django.views.static import serve

io.BufferedReader


class RangeFileReader:
    """Class to read range of bytes from file like object"""

    # block size in bytes to yield each time
    block_size = 8192

    def __init__(self, file_like: io.IOBase, start: int, stop: int):
        """Initializes a RangeFileReader

        Args:
            file_like (io.IOBase): file like object to read
            start (int): start point
            stop (int): stop point
        """

        self.file = file_like
        self.start = start
        self.stop = stop

    def close(self):
        try:
            self.file.close()
        except Exception:
            return

    def __iter__(self):
        """
        Returns generator object that yields 'block_size' of bytes
        from file starting at 'start' until 'stop'
        """
        # seek to start point
        self.file.seek(self.start)
        position = self.start
        while position < self.stop:
            data = self.file.read(min(self.block_size, self.stop - position))
            if not data:
                return
            yield data
            position += self.block_size


# regex pattern to parse range query string
RANGE_RE = re.compile(r"^bytes=\s*(\d*)\s*-\s*(\d*)", re.IGNORECASE)


def parse_range(range: str, size: int):
    """Parses range string and returns (start, stop) range"""
    match = RANGE_RE.match(range)
    if match:
        start, stop = match.groups()
        start = int(start or "0")
        stop = int(stop or str(size))
        return start, stop


async def range_serve(request: HttpRequest, *args, **kwargs):
    """Base server function for media file requests"""

    response = serve(request, *args, **kwargs)
    range = request.META.get("HTTP_RANGE")
    # check if range is requested
    if range and hasattr(response, "file_to_stream"):
        # get file stream
        file = response.file_to_stream
        # get file statuses
        f_stat = os.fstat(file.fileno())
        # get file size to parse the range
        size = f_stat.st_size
        try:
            start, stop = parse_range(range, size)
        except Exception:
            return response
        # If range is bad response with 416 code
        if start > stop or stop > size:
            return HttpResponse(status=416)
        response.streaming_content = RangeFileReader(file, start, stop)
        response["Accept-Ranges"] = "bytes"
        response["Content-Range"] = "bytes %d-%d/%d" % (start, stop - 1, size)
        response["Content-Length"] = stop - start
        response.status_code = 206
    return response
