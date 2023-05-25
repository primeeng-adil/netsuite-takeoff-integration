def add_keys_to_elements(keys, elements, start=0):
    """
    Append the user keys to the elements.

    :param keys: keys entered by the user in the app
    :param elements: web elements required by the controller
    :param start: element index to start appending keys from
    """
    for i in range(start, len(elements)):
        if 'action' in elements[i]:
            if elements[i]['action'] in ('send-keys', 'select'):
                elements[i]['keys'] = keys.pop(0)
