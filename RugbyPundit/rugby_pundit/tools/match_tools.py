"""Tools for getting information about rugby matches."""
from langchain.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from ..data.six_nations_data import SixNationsData, Match
from datetime import datetime

class MatchInput(BaseModel):
    limit: str = Field(description="Number of matches to return (default '6')")

class AddMatchInput(BaseModel):
    date: str = Field(description="Match date (format: 'YYYY-MM-DD HH:MM')")
    home_team: str = Field(description="Home team name")
    away_team: str = Field(description="Away team name")
    home_score: int = Field(description="Home team score")
    away_score: int = Field(description="Away team score")
    venue: str = Field(description="Match venue")

class MatchTools:
    _data = SixNationsData()

    @staticmethod
    @tool
    def get_recent_matches(limit: str = "5") -> str:
        """Get results from the most recent matches.
        
        Args:
            limit: Number of matches to return (default "5")
        """
        data = MatchTools._data
        try:
            num_matches = int(limit)
        except ValueError:
            num_matches = 3
            
        recent_matches = data.get_recent_matches(num_matches)
        if not recent_matches:
            return "No recent matches found"
            
        result = "Recent Match Results:\n\n"
        for match in recent_matches:
            result += (
                f"{match.date.strftime('%d %B %Y')}\n"
                f"{match.home_team} {match.home_score} - {match.away_score} {match.away_team}\n"
                f"Venue: {match.venue}\n\n"
            )
        return result 

    @staticmethod
    def add_match(
        date: str,
        home_team: str,
        away_team: str,
        home_score: int,
        away_score: int,
        venue: str
    ) -> str:
        """Add a match result to the database.
        
        Args:
            date: Match date (format: 'YYYY-MM-DD HH:MM')
            home_team: Home team name
            away_team: Away team name
            home_score: Home team score
            away_score: Away team score
            venue: Match venue
        """
        match_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        match = Match(
            date=match_date,
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            venue=venue
        )
        MatchTools._data.add_match(match)
        return f"Added match: {home_team} {home_score} - {away_score} {away_team}"

    # Create structured tool
    get_recent_matches_tool = StructuredTool.from_function(
        func=get_recent_matches,
        name="get_recent_matches",
        description="Get results from the most recent matches.",
        args_schema=MatchInput
    )

    add_match_tool = StructuredTool.from_function(
        func=add_match,
        name="add_match",
        description="Add a match result to the database.",
        args_schema=AddMatchInput
    ) 