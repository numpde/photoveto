import base64
import markdown
from PIL.Image import Image
from qrcode.image.pil import PilImage

from photoveto.twig import log

from io import BytesIO

from pathlib import Path

from django.conf import settings
from django.shortcuts import render
from qrcode.main import QRCode


def zero_tolerance(request):
    md_file_path = Path(settings.BASE_DIR) / "app" / "content" / "zero-tolerance.md"

    try:
        with md_file_path.open('r') as file:
            license_html = markdown.markdown(file.read())
    except FileNotFoundError:
        license_html = "<p>Markdown file not found.</p>"

    url = request.build_absolute_uri().replace("http:", "https:")

    try:
        # Generate QR code
        qr = QRCode(version=1, box_size=10, border=1, error_correction=0)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color='white', back_color='black')

        assert isinstance(img, PilImage)

        # Save QR code to a BytesIO buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Encode the image to base64
        qr_code_data = base64.b64encode(buffer.getvalue()).decode()
        qr_code_url = f"data:image/png;base64,{qr_code_data}"
    except:
        log.exception(f"Could not build the QR code for this page ({url = }).")
        qr_code_url = None

    context = {
        'title': "Zero-tolerance digital license",
        'html_content': license_html,
        'qr_code_url': qr_code_url,
    }

    return render(request, 'app/basic-license.html', context=context)
