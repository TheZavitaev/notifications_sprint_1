from scheduler.src.models import Event


def get_events(items):
    events = []
    for item in items:
        context = item['context']
        try:
            user_ids = context['user_ids']
            del context['user_ids']
        except KeyError:
            user_ids = []
        try:
            user_categories = context['user_categories']
            del context['user_categories']
        except KeyError:
            user_categories = []
        item['context'] = context
        event = Event(
            **item,
            user_ids=user_ids,
            user_categories=user_categories,
        )
        events.append(event)
