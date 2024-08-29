import base64
import qrcode


def get_encoded_str(original_str, start_position=0, length=8):
    if start_position < 0:
        start_position = 0

    end_position = start_position + length

    encoded_str = base64.urlsafe_b64encode(original_str.encode('utf-8'))
    truncated_str = encoded_str[start_position:end_position]
    return truncated_str.decode('utf-8')


def create_qr_code(string):
    img = qrcode.make(string)
    return img
