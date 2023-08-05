from .errors import ConfigurationError


class PaylenseConfig(object):

    def __init__(self, conf):
        """

        config={

            PAYLENSE_ENVIRONMENT: os.environ.get("PAYLENSE_ENVIRONMENT"),
            PAYLENSE_VERSION: os.environ.get("PAYLENSE_VERSION"),
            PAYLENSE_APP_ID: os.environ.get("PAYLENSE_APP_ID"),
            PAYLENSE_USERNAME: os.environ.get("PAYLENSE_USERNAME"),
            PAYLENSE_PASSWORD: os.environ.get("PAYLENSE_PASSWORD"),


        }


        """
        self._config = conf

    def get_property(self, property_name):
        if property_name not in self._config.keys():
            return None
        return self._config[property_name]

    @property
    def environment(self):
        return self.get_property('PAYLENSE_ENVIRONMENT') or "sandbox"

    @property
    def version(self):
        return self.get_property('PAYLENSE_VERSION') or "v1"

    @property
    def baseUrl(self):
        if self.environment == "sandbox":
            return "https://api-sandbox.paylense.com/" + self.version
        else:
            return "https://api.paylense.com/" + self.version

    @property
    def app_id(self):
        key = self.get_property('PAYLENSE_APP_ID')
        if not key:
            raise ConfigurationError(
                "PAYLENSE_APP_ID is missing in the configuration")
        else:
            key

    @property
    def username(self):
        key = self.get_property('PAYLENSE_USERNAME')
        if not key:
            raise ConfigurationError(
                "PAYLENSE_USERNAME is missing in the configuration")
        else:
            key

    @property
    def password(self):
        key = self.get_property('PAYLENSE_PASSWORD')
        if not key:
            raise ConfigurationError(
                "PAYLENSE_PASSWORD is missing in the configuration")
        else:
            return key
