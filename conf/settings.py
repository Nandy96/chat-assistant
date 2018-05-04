import os
from jupiter.conf import Config as JupiterConfig
from commonlib.auth.constants import AuthServerConstants, DeploymentConstants


class FrontEndConfig(object):
    def __init__(self):
        self.jupiter_config = JupiterConfig
        self.jupiter_config.depends_on(["cloud_guest", "toggles"])

    def __getattr__(self, name):
        # if the attribute is found through the normal mechanism, __getattr__() is not called
        # if the attribute is not found normally, it gets lookedup in jupiter_config object
        # Or, it raises an AttribuetError when attribute is not there in jupiter_config too
        return getattr(self.jupiter_config, name)

    @property
    def google_account(self):
        return self.static.get('google', {})

    @property
    def google_analytics(self):
        return self.static.get('google_analytics', {})

    @property
    def integrated_apps(self):
        return self.system_apps.get('integrated_apps', {})

    @property
    def visualrf(self):
        return self.system_apps.get('visualrf', {})

    @property
    def default_css_bundle(self):
        try:
            return self.css_bundles.get("default")
        except Exception:
            return "base-stylesheets-app.css"

    @property
    def static_file_config(self):
        static_fpath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    'static-file-config.yml')
        return static_fpath

    @property
    def service_port(self):
        return self.assigned_service_config["frontend"]["port"]

    @property
    def get_auth_server(self):
        return self.cluster_info.get('auth_server', AuthServerConstants.ARUBASSO)

    @property
    def get_deployment_type(self):
        return self.cluster_info.get('deployment', DeploymentConstants.PUBLIC)

    @property
    def get_enable_troubleshooting_hp_switch(self):
        return self.toggles.get('enable_troubleshooting_hp_switch', True)

    @property
    def mapbox(self):
        return self.static.get('mapbox', {})

    @property
    def cdn(self):
        return self.static.get('cdn', {"enabled": False})

    @property
    def att_env(self):
        return self.cluster_info.get('att_env', False)


Config = FrontEndConfig()
