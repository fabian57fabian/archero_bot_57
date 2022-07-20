from requests import get


class UpdatesManager:
    def __init__(self):
        self.request_url = "http://217.160.188.167:3000/api/archero_updates"
        self.CURRENT_VERSION = "v2"

    def get_my_update_code(self):
        # better if have hash of last commit.
        return ""

    def ask_for_updates(self):
        try:
            params = {"my_app_update": self.get_my_update_code(), "version": self.CURRENT_VERSION}
            r = get(url=self.request_url, json=params)
            if r.ok:
                data = r.json()
                if "result" in data:
                    if data["result"] != "OK":
                        print("Wrong request for updates: got " + data["result"])
                        return False
                    else:
                        res = data["data"]
                        if type(res) == str:
                            if str(res) == "NO_NEW_UPDATES":
                                print("Updates checked. All right.")
                                return False
                            elif str(res) == "NEW_UPDATE_AVAILABLE":
                                server_ver = "V99"
                                if "version" in data: server_ver = data["version"]
                                print("Server have a different version: {}".format(server_ver))
                                return True
                            else:
                                #unknown
                                return False
            else:
                print("Unable to request for updates, got {}".format(r.status_code))
                return False
            return False
        except Exception as e:
            print("Unable to request for updates. skipping")
            return False


if __name__ == '__main__':
    man = UpdatesManager()
    man.ask_for_updates()
