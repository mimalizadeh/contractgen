from django import template

register = template.Library()

@register.filter
def render_contract(content, context_dict):
    try:
        return content.format(**context_dict)
    except Exception as e:
        return f"[Error when format content in render_contract tag {e}]"