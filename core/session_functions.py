import requests


def get_new_session(url, headers):
    """
    Makes a new session and get required cookies from the target site

    :param url: Target site url
    :param headers: Required headers
    :return: New session with headers and cookies
    :rtype: requests.Session
    """

    session = requests.Session()
    session.headers = headers
    session.get(url)
    return session
