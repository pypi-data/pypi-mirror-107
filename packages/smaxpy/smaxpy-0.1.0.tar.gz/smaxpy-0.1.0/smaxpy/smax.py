from __future__ import annotations
from typing import Callable, Optional

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests.models import Response

from .request import cfscrape_wrapper, request_wrapper
from .errors import SoupParseError


class Smax(BeautifulSoup):
    def __init__(
        self,
        website: str,
        request_function: Optional[
            Callable[[str], Response]
        ] = None,  # a custom function wrapper
        headers: Optional[dict] = None,
        cloudflare: bool = False,
    ) -> None:
        """
        New Smax simple client wrapper.

        Args:
            `website` (str): [the website to scrape]
            `request_function` (Optional[Callable[[str], Response]], optional): [your custom function wrapper].
            Defaults to None.
            `cloudflare` (bool, optional): [use cloudflare]. Defaults to False.

        Raises:
            `SoupParseError`: [it errors if the result from the request_function is
            blank or None]
        """

        # TODO: future better implementation of request_function

        self.website = website
        self.__html = (
            request_function(website).text
            if request_function is not None
            else (
                request_wrapper(website, headers).text
                if not cloudflare
                else cfscrape_wrapper(website, headers).text
            )
        )

        if not self.__html:
            raise SoupParseError("Output from request function is blank.")

        self.__soup = BeautifulSoup(self.__html, "lxml")

        # inherit from `BeautifulSoup` class
        super().__init__(self.__html, "lxml")

    def __repr__(self) -> str:
        # TODO: change,
        return "New Smax Class"

    @property
    def title(self) -> str:
        """Return the scraped website's title.
        It overrides the BeautifulSoup's `.title.text`

        Returns:
            str: [website title]
        """
        return self.__soup.title.text  # type: ignore

    def find_all_links(self, limit: Optional[int]) -> ResultSet:
        """Return all links found on the document.

        Args:
            limit (int, optional): [limit of links to return]. Defaults to None.

        Returns:
            ResultSet: [the list of found links]
        """
        return self.__soup.find_all("a", limit=limit)

    def get_script(self) -> None:
        """
        [!NOTE:: FUNCTION IS BLANK] Parse the <script></script> tag.
        """
