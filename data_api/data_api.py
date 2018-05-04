from luis_sdk import LUISClient

APPID = '594deced-2f12-44f3-9a90-db5f0c7c75ec'
APPKEY = 'a4f33440a27b4f4481d8462c8b4798e4'
CLIENT = LUISClient(APPID, APPKEY, True)
from central_api import get_client_bandwidth_usage
intent_api_map = {'MonitoringIntent': [get_client_bandwidth_usage]}


def process_res(res):
    """
    A function that processes the luis_response object and prints info from it.
    :param res: A LUISResponse object containing the response data.
    :return: None
    """
    print(u'---------------------------------------------')
    print(u'LUIS Response: ')
    print(u'Query: ' + res.get_query())
    print(u'Top Scoring Intent: ' + res.get_top_intent().get_name())
    if res.get_dialog() is not None:
        if res.get_dialog().get_prompt() is None:
            print(u'Dialog Prompt: None')
        else:
            print(u'Dialog Prompt: ' + res.get_dialog().get_prompt())
        if res.get_dialog().get_parameter_name() is None:
            print(u'Dialog Parameter: None')
        else:
            print('Dialog Parameter Name: ' + res.get_dialog().get_parameter_name())
        print(u'Dialog Status: ' + res.get_dialog().get_status())
    print(u'Entities:')
    for entity in res.get_entities():
        print(u'"%s":' % entity.get_name())
        print(u'Type: %s, Score: %s' % (entity.get_type(), entity.get_score()))


def get_luis_response(user_input):
    try:
        res = CLIENT.predict(user_input)
        process_res(res)
        return res
        # while res.get_dialog() is not None and not res.get_dialog().is_finished():
        #     TEXT = raw_input(u'%s\n'%res.get_dialog().get_prompt())
        #     res = CLIENT.reply(TEXT, res)

    except Exception as exc:
        print(exc)


def get_central_response(luis_response, cid, user_name, contextual_params=None):
    intent = luis_response.get_top_intent().get_name()
    params = {'cid': cid, 'user_name': user_name}
    if contextual_params:
        params.update(contextual_params)
    for entity in luis_response.get_entities():
        print(u'"%s":' % entity.get_name())
        print(u'Type: %s, Score: %s' % (entity.get_type(), entity.get_score()))
        params[entity.get_name()] = entity.get_resolution()
    for api in intent_api_map.get(intent):
        # TODO: Need to combine responses from multiple central api
        return api(**params), params


def get_chat_response(central_response, top_scoring_intent):
    intent_name = top_scoring_intent.get_name()
    if intent_name == 'None':
        return {'resp': "I'm not able to understand the question. Could you please rephrase it"}
    if intent_name == 'Utilities.Stop':
        return {'resp': "Thanks for using Central Chat Assistant"}
    if intent_name == 'Utilities.Help':
        return {'resp': "Welcome to Central Chat Assistant Service. "
                        "You can ask me questions about central and your network. "
                        "Example may include: How is my network is doing"
                        "What are the highlights today"}
    return central_response


def get_pre_canned_response(top_scoring_intent):
    intent_name = top_scoring_intent.get_name()
    if intent_name == 'None':
        return {'resp': "I'm not able to understand the question. Could you please rephrase it"}
    if intent_name == 'Utilities.Stop':
        return {'resp': "Thanks for using Central Chat Assistant"}
    if intent_name == 'Utilities.Help':
        return {'resp': "Welcome to Central Chat Assistant Service. "
                        "You can ask me questions about central and your network. "
                        "Example may include: How is my network is doing"
                        "What are the highlights today"}

