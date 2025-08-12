import re
import os

from django import template
from django.core.files.storage import default_storage

register = template.Library()

# @register.filter(name='replace')
# def replace(text, buzzwords):
#     for buzzword in buzzwords:
#         pattern = rf'(?i)(?<!\w){re.escape(buzzword.buzzword)}(?!\w|\.)'
#         def replace_case(match):
#             matched_text = match.group(0)
#             return f"<span class='buzzword' onclick=\"openModal('{buzzword.linked_file.file.url}', '{buzzword.id}', event)\">{matched_text}</span>"
#         text = re.sub(pattern, replace_case, text)
#     return text

@register.filter(name='replace')
def replace(text, buzzwords):
    for buzzword in buzzwords:
            pattern = rf'(?i)(?<!\w){re.escape(buzzword.buzzword)}(?!\w|\.)'

            def replace_case(match):
                matched_text = match.group(0)
                file_url = ''
                file_type = ''

                if buzzword.linked_file and buzzword.linked_file.file:
                    file_type = buzzword.linked_file.file_type
                    base = os.path.splitext(os.path.basename(buzzword.linked_file.file.name))[0]

                    if file_type.lower() == 'video':
                        optimized_path = f"optimized/media_files/{base}.mp4"
                    else:
                        optimized_path = f"optimized/media_files/{base}.webp"

                    file_url = default_storage.url(optimized_path)

                return (
                    f"<span class='buzzword' "
                    f"onclick=\"openModal('{file_url}', '{buzzword.id}', '{file_type}', event)\">"
                    f"{matched_text}</span>"
                )

            text = re.sub(pattern, replace_case, text)

    return text

@register.filter
def storage_url(path: str) -> str:
    return default_storage.url(path)
