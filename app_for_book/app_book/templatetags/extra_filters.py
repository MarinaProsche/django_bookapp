import re
from django import template

register = template.Library()

# @register.filter(name='replace')
# def replace(text, buzzwords):
#     for buzzword in buzzwords:
#         pattern = rf'(?i)(?<!\w){re.escape(buzzword.buzzword)}(?!\w|\.)'
#         def replace_case(match):
#             matched_text = match.group(0)
#             return f"<a href='{buzzword.linked_file.link_to_image}' class='text-lavender' style='color: #9654c5'>{matched_text}</a>"
#         text = re.sub(pattern, replace_case, text)

#     return text

@register.filter(name='replace')
def replace(text, buzzwords):
    for buzzword in buzzwords:
        pattern = rf'(?i)(?<!\w){re.escape(buzzword.buzzword)}(?!\w|\.)'
        def replace_case(match):
            matched_text = match.group(0)
            return f"<span class='buzzword' onclick=\"openModal('{buzzword.linked_file.file.url}', '{buzzword.id}', event)\">{matched_text}</span>"
        text = re.sub(pattern, replace_case, text)
    return text
