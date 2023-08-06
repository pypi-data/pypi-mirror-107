# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ebay_feedsdk',
 'ebay_feedsdk.config',
 'ebay_feedsdk.constants',
 'ebay_feedsdk.enums',
 'ebay_feedsdk.errors',
 'ebay_feedsdk.examples',
 'ebay_feedsdk.filter',
 'ebay_feedsdk.oauthclient',
 'ebay_feedsdk.oauthclient.model',
 'ebay_feedsdk.tests.oauthclient',
 'ebay_feedsdk.tests.sdk',
 'ebay_feedsdk.utils']

package_data = \
{'': ['*'],
 'ebay_feedsdk': ['sample-config/*'],
 'ebay_feedsdk.tests.oauthclient': ['config/*'],
 'ebay_feedsdk.tests.sdk': ['test-data/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.3.8,<2.0.0',
 'aenum>=3.00,<4.0',
 'certifi>=2020.12.5,<2021.0.0',
 'pandas>=1.1.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.4,<2.0.0']

setup_kwargs = {
    'name': 'ebay-feedsdk',
    'version': '0.2.1',
    'description': 'Port of https://github.com/eBay/FeedSDK-Python and https://github.com/eBay/ebay-oauth-python-client to python3',
    'long_description': 'Feed SDK\n==========\nPython SDK for downloading and filtering item feed files including oauth authentication.\n\nForked and merged from [https://github.com/eBay/FeedSDK-Python](https://github.com/eBay/FeedSDK-Python) and [https://github.com/eBay/ebay-oauth-python-client](https://github.com/eBay/ebay-oauth-python-client) and ported to python3\n\nNothing serious changed, made it barely working. \n\nCode is not improved yet and would need some maintenance. \n\nAutomatic Tests not working due to the nature the tests were original programmed (you need to provide actual token etc.)\n\nAvailable as PyPI package under https://pypi.org/project/ebay-feedsdk/\n\nExample code to retrieve oauth token and download file (you need working ebay-config.yaml)\n```\nimport logging\n\nfrom errors.custom_exceptions import DownloadError\nfrom feed import Feed\nfrom filter.feed_filter import GetFeedResponse\nfrom oauthclient.credentialutil import Credentialutil\nfrom oauthclient.model.model import Environment, OauthToken, EnvType\nfrom oauthclient.oauth2api import Oauth2api\n\n\nclass EbayDownloadExample:\n    app_scopes = ["https://api.ebay.com/oauth/api_scope", "https://api.ebay.com/oauth/api_scope/buy.item.feed"]\n    config_file = \'ebay-config.yaml\'\n\n    def __init__(self, market_place: str, env: EnvType, feed_scope, download_location: str):\n        self.env = env\n        self.feed_scope = feed_scope\n        self.market_place = market_place\n        self.download_location = download_location\n\n    def download(self, category_id: str):\n        logging.info(\n            f\'Downloading category {category_id} for {self.market_place} with scope {self.feed_scope}\'\n            f\'to {self.download_location}\')\n\n        token = self.get_token()\n\n        feed_obj = Feed(feed_type=\'item\', feed_scope=self.feed_scope, category_id=category_id,\n                        marketplace_id=self.market_place,\n                        token=token.access_token, environment=self.env.name, download_location=self.download_location)\n\n        feed_response: GetFeedResponse = feed_obj.get()\n\n        if feed_response.status_code != 0:\n            raise DownloadError(f\'Download failed see: {feed_response.message}\')\n\n        logging.info(f\'File was downloaded under {feed_response.file_path}\')\n\n        return feed_response.file_path\n\n    def get_token(self) -> OauthToken:\n        Credentialutil.load(self.config_file)\n        oauth2api = Oauth2api()\n\n        token = oauth2api.get_application_token(self.env, self.app_scopes)\n        if not token.access_token:\n            raise DownloadError(f\'Got no token, check: {token.error}\')\n\n        return token\n\n\nif __name__ == "__main__":\n    market_place = \'EBAY_DE\'\n    feed_scope = \'ALL_ACTIVE\'\n    download_location = \'/tmp/feed\'\n    category_id = \'2984\'  # string ..\n    ebay_download = EbayDownloadExample(market_place, Environment.PRODUCTION, feed_scope, download_location)\n    file_path = ebay_download.download(category_id)\n```\nSee also for details:\n\n* [https://github.com/eBay/ebay-oauth-python-client/blob/master/README.adoc](https://github.com/eBay/ebay-oauth-python-client/blob/master/README.adoc)\n* [https://github.com/eBay/FeedSDK-Python/blob/master/README.md](https://github.com/eBay/FeedSDK-Python/blob/master/README.md)\n',
    'author': 'Lars Erler',
    'author_email': 'lars@xaospage.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/taxaos/FeedSDK-Python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
