def add_keys_to_elements(keys, elements, start=0, term_str=''):
    """
    Append the user keys to the elements.

    :param term_str:
    :param keys: keys entered by the user in the app
    :param elements: web elements required by the controller
    :param start: element index to start appending keys from
    """
    for i in range(start, len(elements)):
        if 'action' in elements[i] and 'keys' in elements[i]:
            if 'send-keys' in elements[i]['action']:
                elements[i]['keys'] = keys[elements[i]['keys']] + term_str
