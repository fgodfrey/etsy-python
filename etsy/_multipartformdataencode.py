import mimetypes

"""
Functions for encoding multipart/form-data

From http://code.activestate.com/recipes/146306/ (PSF License)
"""

class byteEncoder:
    def __init__(self, sep):
        self.b = None
        self.sep = bytes(sep)

    def append(self, val):
        if self.b is None:
            self.b = bytes(val)
            return

        self.b = self.b + self.sep + bytes(val)

    def value(self):
        return self.b


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = byteEncoder(CRLF)
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append(
            'Content-Disposition: '
            'form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = L.value()
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
