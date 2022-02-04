from scheduler.src.models import Event


def get_events(items: list) -> list[Event]:
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

    return events


def create_chunks(list_name, step):
    for i in range(0, len(list_name), step):
        yield list_name[i: i + step]
