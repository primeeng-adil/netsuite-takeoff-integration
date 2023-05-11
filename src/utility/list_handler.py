def add_keys_to_elements(keys, elements, start=0):
    """

    :param keys:
    :param elements:
    :param start:
    """
    for i in range(start, len(elements)):
        if 'action' in elements[i]:
            if elements[i]['action'] in ('send-keys', 'select'):
                elements[i]['keys'] = keys.pop(0)
