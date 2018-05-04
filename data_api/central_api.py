def get_client_bandwidth_usage(**kwargs):
    cid = kwargs.pop('cid', None)
    if not cid:
        print ('mandatory param cid missing')
    return {'a': 1}
