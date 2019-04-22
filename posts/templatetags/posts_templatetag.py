from django import template

register = template.Library()

@register.filter
def hashtag_link(post):     # 필터 앞에 들어가는 인자를 써줌 - post
    content = post.content+' '
    hashtags = post.hashtags.all()
    
    # hashtags를 순회하면서, content 내에서 해당 문자열(hashtag)를 링크를 포함한 문자열<a>로 치환

    for hashtag in hashtags:
        # 1
        # content = content.replace(hashtag.content , f'<a href="/posts/hashtag/{hashtag.pk}/">{hashtag.content}</a>)
        # 2
        content = content.replace(hashtag.content+' ', f'<a href="/posts/hashtag/{hashtag.pk}/">{hashtag.content}</a> ')
        # 3
        # content = re.sub(fr'hashtag.content'{})
    return content