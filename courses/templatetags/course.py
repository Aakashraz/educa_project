from django import template


# create a Library instance to register custom template tags/filters
register = template.Library()

# register this function as a template filter
@register.filter
def model_name(obj):
    """
    Returns the model name of a Django model instance.
    Usage in template: {{ item|model_name }}
    Returns: 'text', 'video', 'image', 'file', etc.
    """
    try:
        return obj._meta.model_name
    except AttributeErrr:
        # If obj doesn't have _meta (not a model instance), returns None.
        return None