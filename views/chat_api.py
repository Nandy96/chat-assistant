from flask import Blueprint, request, url_for, jsonify, session
from flask_login import login_required, current_user
from data_api import data_api
from jupiter.logger import logging
log = logging.getLogger(__name__)

app = Blueprint('chat_bot', __name__, url_prefix='/chat_bot')


@app.route("/")
@login_required
def index():
    return jsonify(session.get('context'))


@app.route("/chat", methods=["POST"])
@login_required
def chat():
    user_input = request.data
    cid = current_user.cid
    try:
        chat_context = {}
        if session.get('context'):
            chat_context = session['context']
        luis_resp = data_api.get_luis_response(user_input)

        # Send pre-canned response in case of unknown intents / Utility intents
        top_scoring_intent = luis_resp.get_top_intent()
        pre_canned_response = data_api.get_pre_canned_response(top_scoring_intent)
        if pre_canned_response:
            return jsonify(pre_canned_response)

        # Call central APIs to give suitable response to user
        central_resp, params = data_api.get_central_response(luis_resp, cid, current_user.name,
                                                             contextual_params=chat_context.get(
                                                                 'params'))
        # Save context for later use
        if chat_context.get('params'):
            chat_context['params'].update(params)
        else:
            chat_context['params'] = params
        session['context'] = chat_context
        resp = data_api.get_chat_response(central_resp, top_scoring_intent)
    except Exception as exp:
        log.exception('Failed to provide response cid {} query {}: reason {}'.format(
            cid, user_input, exp.message))
        resp = {"status": "failed", "resp": "Ooops some problem. Please try after sometime :-)"}
    return jsonify(resp)
