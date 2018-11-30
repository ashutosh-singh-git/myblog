from django import template

register = template.Library()


@register.filter
def strip_double_quotes(quoted_string):
    return quoted_string.replace('"', '')


@register.filter
def process_image(html):
    return html.replace('<img', '<figure class="figure text-center" style="margin:0"><img class="figure-img img-fluid w-100 rounded"') \
        .replace('/caption>', '/figcaption></figure>') \
        .replace('<caption', '<figcaption class="figure-caption"') \
        .replace('<p></p>','')
