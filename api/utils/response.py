
def response_msg(status, message=None, payload=None, http_status=400):

    response = {'status': f'{status}',}

    response.__setitem__('message', message) if message is not None else None
    response.__setitem__('payload', payload) if payload is not None else None

    return response, http_status
