import re
from django import template

register = template.Library()

# @register.filter(name='replace')
# def replace(text, buzzwords):
#     for buzzword in buzzwords:
#         # if buzzword.buzzword in text.lower():
#         text = re.sub(
#             rf'(?i)\b{re.escape(buzzword.buzzword)}\b',
#             f"<a href='{buzzword.linked_file.link_to_image}'>{buzzword.buzzword}</a>",
#             text
#         )
#     return text


@register.filter(name='replace')
def replace(text, buzzwords):
    for buzzword in buzzwords:
        pattern = rf'(?i)\b{re.escape(buzzword.buzzword)}\b' #case-insensitive, includes spec symbols just in case
        def replace_case(match):
            matched_text = match.group(0)
            output_ex = f"<a href='{buzzword.linked_file.link_to_image}'>{matched_text}</a>"
            return output_ex
        text = re.sub(pattern, replace_case, text)
    
    return text
