import asyncio
import io
import os
import re
from django.http import HttpRequest, HttpResponse
from django.views.static import serve


class RangeFileReader:

    block_size = 8192

    def __init__(self, file_like: io.IOBase, start: int, stop: int):
        self.file = file_like
        self.start = start
        self.stop = stop

    def close(self):
        try:
            self.file.close()
        except Exception as e:
            return

    def __iter__(self):
        self.file.seek(self.start)
        position = self.start
        while position < self.stop:
            data = self.file.read(min(self.block_size, self.stop - position))
            if not data:
                break
            yield data
            position += self.block_size


RANGE_RE = re.compile(
    r'^bytes=\s*(\d*)\s*-\s*(\d*)', re.IGNORECASE)


def parse_range(range: str, size: int):
    match = RANGE_RE.match(range)
    if match:
        start, stop = match.groups()
        start = int(start or '0')
        stop = int(stop or str(size))
        return start, stop


async def range_serve(request: HttpRequest, *args, **kwargs):
    response = serve(request, *args, **kwargs)
    range = request.META.get('HTTP_RANGE')
    if range and hasattr(response, 'file_to_stream'):
        # wait a second for each partial range request
        await asyncio.sleep(1)
        file = response.file_to_stream
        f_stat = os.fstat(file.fileno())
        size = f_stat.st_size
        try:
            start, stop = parse_range(range, size)
        except Exception as e:
            return response
        if start > stop or stop > size:
            return HttpResponse(status=416)
        response.streaming_content = RangeFileReader(file, start, stop)
        response['Accept-Ranges'] = 'bytes'
        response['Content-Range'] = 'bytes %d-%d/%d' % (start, stop - 1, size)
        response['Content-Length'] = stop - start
        response.status_code = 206
    return response
