import re
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
            file_url = buzzword.linked_file.file.url if buzzword.linked_file.file else ''
            file_type = buzzword.linked_file.file_type  # 'image' или 'video'
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
