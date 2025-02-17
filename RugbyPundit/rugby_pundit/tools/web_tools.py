"""Tools for searching the web for rugby information."""
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper
from typing import Dict
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query")

class RugbyWebTools:
    def __init__(self):
        self.search = GoogleSearchAPIWrapper()

    def search_six_nations(self, query: str) -> str:
        """Search for recent news and information about Six Nations Rugby"""
        return self.search.run(query)

    def search_team_news(self, query: str) -> str:
        """Search for recent news about a specific team"""
        return self.search.run(query)

    @property
    def search_six_nations_tool(self) -> Tool:
        return Tool(
            name="search_six_nations",
            func=self.search_six_nations,
            description="Search for recent news and information about Six Nations Rugby",
            args_schema=SearchInput
        )

    @property
    def search_team_news_tool(self) -> Tool:
        return Tool(
            name="search_team_news",
            func=self.search_team_news,
            description="Search for recent news about a specific team",
            args_schema=SearchInput
        )

    def search_match_reports(self, query: str) -> str:
        return self.search.run(f"2025 Six Nations {query} match report")

    @property
    def search_match_reports_tool(self) -> Tool:
        return Tool(
            name="search_match_reports",
            func=self.search_match_reports,
            description="Search for match reports between two teams",
            args_schema=SearchInput
        ) 