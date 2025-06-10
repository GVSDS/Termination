from .T_imports import *
from .T_GodKeys import GodKeys


class TWNetworkIO:
    def __init__(self):
        self.__init_values__()
    def __init_values__(self):
        self.GodKeysEncryption=False
    def __init_set__(self, GodKeys: GodKeys):
        self.GodKeys=GodKeys
    def _get(self, url, params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,):
        return requests.get(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
    def _post(self, url, params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,):
        return requests.post(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
    def get(self, url, params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,):
        try:
            _=self._get(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
            return self.GodKeys.decrypt(_) if self.GodKeysEncryption else _
        except:
            return None
    def post(self, url, params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,):
        try:
            _=self._post(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
            _.content=self.GodKeys.decrypt(_.content) if self.GodKeysEncryption else _.content
        except:
            return None
    def CheckNetworkEnvironment(self):
        try:
            requests.get("https://www.baidu.com")
        except:
            return False
        else:
            return True