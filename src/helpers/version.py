import requests
import semver
from helpers.logger import Logger

log = Logger().get_logger()

__version__ = "1.0.3"

def check_version(mute = False):
    local_version = __version__
    remote_version = "0.0.1"

    # find newest release on github
    gh_api = requests.get("https://api.github.com/repos/combahton/combahton-cli/tags")
    available_versions = (tag for tag in gh_api.json() if tag["name"] != "latest")
    for tag in available_versions:
        test_version = tag["name"][1:]
        if semver.compare(test_version, remote_version) > 0:
            remote_version = test_version

    # comparing remote to local
    version_test = semver.compare(remote_version, local_version)
    if not mute:
        if version_test == 0:
            log.info("Your version of combahton-cli is up to date.")
        elif version_test > 0:
            log.warning("""Your version of combahton-cli is outdated.\nLocal Version: {local:s}\nRemote Version: {remote:s}
Please update at your earliest convenience: https://github.com/combahton/combahton-cli""".format(local = local_version, remote = remote_version))
        elif version_test < 0:
            log.info("Your version of combahton-cli is newer than the latest public release. | Local Version: {local:s} | Remote Version: {remote:s}".format(local = local_version, remote = remote_version))

    return version_test == 0

if __name__ == "__main__":
    check_version()
