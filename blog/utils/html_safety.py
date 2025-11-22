import bleach
from django.utils.html import escape
from django.utils.safestring import mark_safe
from markdown import markdown

ALLOWED_HTML_TAGS = bleach.sanitizer.ALLOWED_TAGS | {
    'p',
    'br',
    'div',
    'span',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'strong',
    'em',
    'code',
    'pre',
    'blockquote',
    'ul',
    'ol',
    'li',
}

ALLOWED_HTML_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'code': ['class'],
    'span': ['class'],
}


def safe_markdown_to_html(markdown_text):
    """
    Безопасное преобразование Markdown в HTML с экранированием
    """
    if not markdown_text:
        return ''

    escaped_text = escape(markdown_text)

    html_content = markdown(escaped_text)

    clean_html = bleach.clean(
        html_content,
        tags=ALLOWED_HTML_TAGS,
        attributes=ALLOWED_HTML_ATTRIBUTES,
        strip=True,
    )

    clean_html = bleach.linkify(clean_html, callbacks=[bleach.callbacks.nofollow])

    return mark_safe(clean_html)  # noqa: S308


def safe_text_to_html(text):
    """
    Безопасное преобразование простого текста в HTML
    """
    if not text:
        return ''

    escaped_text = escape(text)

    html_content = escaped_text.replace('\n', '<br>')

    clean_html = bleach.clean(html_content, tags=['br'], attributes={}, strip=True)

    return mark_safe(clean_html)  # noqa: S308
