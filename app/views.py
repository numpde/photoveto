import markdown

from django.http import HttpResponse
from django.conf import settings
from pathlib import Path


def zero_tolerance(request):
    # Path to your Markdown file using pathlib
    md_file_path = Path(settings.BASE_DIR) / "app" / "content" / "zero-tolerance.md"

    # Read the file
    with md_file_path.open('r') as file:
        md_content = file.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    return HttpResponse(html_content)
