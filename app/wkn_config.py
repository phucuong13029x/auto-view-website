import os
from configparser import ConfigParser


# DEFAULT
info_title = "Auto Viewer Website"
info_version = "1.1"
info_author = "phucuongds.com"
basedir = os.getcwd()

# FOLDER & FILE
os.makedirs(basedir + os.sep + 'Extensions', exist_ok=True)
basedir_extensions = basedir + os.sep + 'Extensions'
basedir_log = basedir_extensions + os.sep + 'Logs'
file_proxy = basedir_extensions + os.sep + 'proxy.txt'
file_link = basedir_extensions + os.sep + 'link.txt'
file_config = basedir_extensions + os.sep + 'config.ini'

# LOAD CONFIG USER
configini = ConfigParser()
configini.read(file_config, encoding = "utf8")

# ## License
# configini_access_token = configini.get("LICENSE", "access_token")
# configini_license = configini.get("LICENSE", "license")
## Windows screen
configini_screen = configini.get("WINDOWS", "screen")
configini_hidden = configini.get("WINDOWS", "hidden")
## Browser
configini_browser_max = int(configini.get("BROWSER", "maxbrowser"))
configini_browser_profile = configini.get("BROWSER", "profile")
configini_browser_random_time = configini.get("BROWSER", "random_time").split(",")
## Proxy
configini_proxy = configini.get("PROXY", "proxy")
configini_proxy_protocol = configini.get("PROXY", "protocol")
configini_proxy_timeout = configini.get("PROXY", "timeout")
configini_proxy_country = configini.get("PROXY", "country")
configini_proxy_ssl = configini.get("PROXY", "ssl")
configini_proxy_anonymity = configini.get("PROXY", "anonymity")
