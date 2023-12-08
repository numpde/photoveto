import base64
import markdown

from io import BytesIO
from pathlib import Path

from photoveto.twig import log

from qrcode.image.pil import PilImage

from django.conf import settings
from django.shortcuts import render
from qrcode.main import QRCode


def _get_content(filename: str):
    md_file_path = Path(settings.BASE_DIR) / "app" / "content" / filename

    try:
        with md_file_path.open('r') as file:
            return markdown.markdown(file.read())
    except FileNotFoundError:
        return "<p>Markdown file not found.</p>"


def _get_qr_code_src(url: str):
    try:
        qr = QRCode(version=1, box_size=10, border=1, error_correction=0)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')

        assert isinstance(img, PilImage)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Encode the image to base64
        qr_code_data = base64.b64encode(buffer.getvalue()).decode()
        qr_code_src = f"data:image/png;base64,{qr_code_data}"
    except:
        log.exception(f"Could not build the QR code for this page ({url = }).")
        qr_code_src = None

    return qr_code_src


def index(request):
    url = request.build_absolute_uri().replace("http:", "https:")

    context = {
        'title': "PhotoVeto digital licenses",
        'html_content': _get_content("introduction.md"),
    }

    return render(request, 'app/basic.html', context=context)


def zero_tolerance(request):
    url = request.build_absolute_uri().replace("http:", "https:")

    context = {
        'title': "Zero-tolerance digital license",
        'html_content': _get_content("zero-tolerance.md"),
        'qr_code_url': url,
        'qr_code_src': _get_qr_code_src(url),
    }

    return render(request, 'app/basic.html', context=context)
