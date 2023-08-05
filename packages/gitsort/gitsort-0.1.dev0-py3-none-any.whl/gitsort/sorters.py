from __future__ import annotations
from typing import Tuple, List
import requests
import re

token = "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"


def run_query(query: str, headers: dict | None = None) -> Tuple[any, str]:
    if not headers:
        headers = {"Authorization": "Bearer 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"}
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json(), request.headers["X-RateLimit-Remaining"]
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


class InvalidUrlException(BaseException):
    """Exception when url/path is invalid"""


class BaseSorter:
    def __init__(self, path: str, options: dict, token: str) -> None:
        self.path = path
        self.options = options
        self.token = token

    def __new__(cls, *args, **kwargs):
        if cls is BaseSorter:
            raise Exception("Base class cannot be created")
        return super().__new__(cls)

    def get_url_info(self) -> Tuple[str, str] | List[str]:
        is_link = re.compile(r"^(git(hub)?|https?)")
        is_git_path = re.compile(r"^[a-zA-Z0-9\-_.]+/[a-zA-Z0-9\-_.]+")
        git_url_regex = re.compile(r"^(https|git)?(://|@)?([^/:]+)[/:](?P<owner>[^/:]+)/(?P<name>.+)(.git)?$")
        is_git_repo = re.compile(r"((.git)|/)$")
        is_valid_username = re.compile(r"^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", re.IGNORECASE)

        if is_link.match(self.path):
            if is_git_path.match(self.path):
                return self.path.split("/")[:2]

            match = git_url_regex.match(self.path)
            if not match:
                raise InvalidUrlException("Invalid path")

            name = match.group("name").split("/")[0]
            name = is_git_repo.sub("", name)
            owner = match.group("owner")

            return owner, name
        else:
            if self.path.count("/") > 0:
                return self.path.split("/")[:2]
            if is_valid_username.match(self.path):
                return [self.path]
            raise InvalidUrlException("Invalid username")


class ForkSorter(BaseSorter):
    ...


if __name__ == "__main__":
    path = "user/repo/whatever"
    s = ForkSorter(path, {}, "w")
    print(s.get_url_info())