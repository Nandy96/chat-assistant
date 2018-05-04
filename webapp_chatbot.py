from commonlib.utils.appfactory import create_app
from commonlib.auth import login
from views import chat_api
from conf.settings import Config

from jupiter.logger import logging
log = logging.getLogger(__name__)

# Initialize app
app = create_app(__name__)
login.login_manager.init_app(app)


# Register Application BluePrints
app.register_blueprint(chat_api.app, url_prefix='/chat_bot')

if __name__ == "__main__":
    app.run(debug=True, port=Config.service_port)