# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subscribe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'subscribe',
    'version': '0.1.0',
    'description': 'Library for managing subscriptions',
    'long_description': '# Subscribe\n\nA simple yet powerfull subscription library in Python for managing subscriptions.\n\n## Concepts\n\nEvery subscription consists of\n\n- *subscription_list* - a unique identification (just a string) for a list to which is subscribed\n- *prio* - a integer with the prio of the subscription which will be used to order the subscriptions\n  (from low to high)\n- *subscriber* - The object which is subscribed. Can be anything. Often a function.\n\n\n## Quick start\n\n   Import subscribe\n\n    >>> import subscribe\n\n### Create a SubscriptionList\n\n    Make a subscription list\n\n    >>> new_user = subscribe.SubscriptionList("new_user")\n\n### Subscribe to the subscription_list\n\n    Add a first subscriber, ie a function.\n\n    >>> @new_user.subscribe()\n    ... def send_mail(user):\n    ...     pass\n\n### Get the subscriptions\n\n    Get the subscriptions, ie so you call the subscribed functions.\n\n    >>> [i for i in new_user.get_subscriptions()]\n    [Subscription(subscription_list=<SubscriptionList id=\'new_user\'>, prio=0, subscriber=<function send_mail at ...>)]\n\n    Or just the subscribers, which is most of the time what you want\n\n    >>> [i.__name__ for i in new_user.get_subscribers()]\n    [\'send_mail\']\n\n    Often the subscribers are callables. You can call them all with\n    same parameters.\n    \n    >>> new_user.call_subscribers(user="marc")\n\n### Priority\n\n    You can subscribe multiple times to the same SubscriptionList.\n    The subscriptions will be sorted in order of prio. When no prio is given, the prio\n    will be equal to 0 and the subscriptions will be in order of addition.\n\n    >>> @new_user.subscribe(prio=-1)\n    ... def compute_age(user):\n    ...     pass\n\n    Get the subscribers.\n\n    >>> [i.__name__ for i in new_user.get_subscribers()]\n    [\'compute_age\', \'send_mail\']\n\n    You can subscribe anything, not just functions. It is up to you.  \n    Ie it can be a string.\n\n    >>> sentence = subscribe.SubscriptionList("sentence")\n\n    >>> word = sentence.subscribe()("Python")\n    >>> word = sentence.subscribe()("is")\n    >>> word = sentence.subscribe(prio=5)("language")\n    >>> word = sentence.subscribe(prio=2)("nice")\n    >>> word = sentence.subscribe(prio=1)("a")\n\n    And you can get the strings in the order of the prio.\n\n    >>> \' \'.join([i for i in sentence.get_subscribers()])\n    \'Python is a nice language\'\n\n### Advanced Usage\n\n#### Class based SubscriptionList\n\n    An important use case is to subscribe to classes. Ie if\n    you have a class NewUserEvent\n\n    >>> class NewUserEvent:\n    ...   pass\n\n    You can create a class subscription, which will convert the class into\n    a subscription list with the fully qualified name as id.\n\n    >>> new_user_event = subscribe.ClassSubscriptionList(NewUserEvent)\n    >>> new_user_event\n    <ClassSubscriptionList class=\'__main__.NewUserEvent\'>\n\n    >>> new_user_event.subscribe()("1")\n    \'1\'\n    >>> new_user_event.subscribe()("2")\n    \'2\'\n    >>> [i for i in new_user_event.get_subscribers()]\n    [\'1\', \'2\']\n\n#### Multiple instantiation\n\n    A subscription list can be created multiple times\n\n    >>> first = subscribe.SubscriptionList("my list")\n    >>> second = subscribe.SubscriptionList("my list")\n\n    Both can be used to subscribe.\n\n    >>> first.subscribe()("subscribe to first")\n    \'subscribe to first\'\n    >>> second.subscribe()("subscribe to second")\n    \'subscribe to second\'\n\n    Both will have the same subscriptions.\n\n    >>> [i.subscriber for i in first.get_subscriptions()]\n    [\'subscribe to first\', \'subscribe to second\']\n    >>> [i.subscriber for i in second.get_subscriptions()]\n    [\'subscribe to first\', \'subscribe to second\']\n    \n#### Subclass SubscriptionList\n\n    You can subclass SubscriptionList, like we did for ClassSubscriptionList.\n\n    For example, if you have users.\n\n    >>> class User:\n    ...     def __init__(self, username):\n    ...         self.username = username\n\n    Which could be used to subscribe to, like subscribing to Twitter accounts\n\n    >>> class UserSubscriptionList(subscribe.SubscriptionList):\n    ...     def __init__(self, user: User):\n    ...         super().__init__(f"user:{user.username}")\n\n    Note: the subscription list is in memory and not persistent. You can implement your own \n    persistency for your SubscriptionList subclass when appropriate.',
    'author': 'Marc Rijken',
    'author_email': 'marc@rijken.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrijken/subscribe',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
