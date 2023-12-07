from django import template


register = template.Library()


@register.filter()
def censor(text):
    words = ['участие', 'новость', 'музыки', 'мира', 'ситуация', 'борьбу',
             'бесплатно', 'удобно', 'заявил', 'глава', 'музыкальный',
             'внимания', 'поле', 'пройдут', 'вопрос', 'возможности', 'система', 'образовательных']

    text_words = text.split()
    text = []

    for word in text_words:
        if word.lower() in words:
            word = f"{word[0]}{'*'*(len(word)-1)}"
            text.append(word)
        else:
            text.append(word)

    return ' '.join(text)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()