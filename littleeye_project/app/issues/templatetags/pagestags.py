from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def safe_query_string(context, **kwargs) -> str:
    """create url-encoded string from GET-parameters.

    get querydict from GET:
    <QueryDict: {'q': ['a'], 'page': ['2']}>

    next_page:
    return q=a&page=3

    previous_page:
    return q=a&page=1
    """
    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
