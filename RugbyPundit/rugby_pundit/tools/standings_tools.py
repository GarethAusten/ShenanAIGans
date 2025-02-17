"""Tools for getting information about team standings."""
from langchain.tools import Tool
from pydantic import BaseModel, Field
from ..data.six_nations_data import SixNationsData, TeamStats

class StandingsInput(BaseModel):
    team: str = Field(
        description="Team name (e.g., 'Ireland', 'England') or empty string for full standings",
        default=""  # Make the field optional with a default empty string
    )

class TeamStatsInput(BaseModel):
    team: str = Field(description="Team name (e.g., 'Ireland', 'England')")

class StandingsTools:
    def __init__(self):
        self.standings = {}  # Initialize with empty standings
        
    def get_standings(self, team: str = "") -> str:
        """Get the current Six Nations championship standings."""
        # Mock standings data
        standings = {
            "Ireland": {"position": 1, "played": 2, "won": 2, "points": 10},
            "England": {"position": 2, "played": 2, "won": 1, "points": 6},
            "France": {"position": 3, "played": 2, "won": 1, "points": 5},
            "Scotland": {"position": 4, "played": 2, "won": 1, "points": 5},
            "Wales": {"position": 5, "played": 2, "won": 0, "points": 1},
            "Italy": {"position": 6, "played": 2, "won": 0, "points": 0}
        }
        
        if team:
            if team in standings:
                return f"{team} standings: {standings[team]}"
            return f"Team {team} not found in standings"
        
        return "\n".join([f"{k}: {v}" for k, v in standings.items()])

    def get_team_stats(self, team: str) -> str:
        """Get detailed statistics for a specific team."""
        # Mock team stats
        team_stats = {
            "Ireland": {"tries": 8, "conversions": 6, "penalties": 4},
            "England": {"tries": 5, "conversions": 4, "penalties": 3},
            "France": {"tries": 6, "conversions": 5, "penalties": 2},
            "Scotland": {"tries": 4, "conversions": 3, "penalties": 4},
            "Wales": {"tries": 3, "conversions": 2, "penalties": 3},
            "Italy": {"tries": 2, "conversions": 1, "penalties": 2}
        }
        
        if team in team_stats:
            return f"{team} stats: {team_stats[team]}"
        return f"Stats for team {team} not found"

    @property
    def get_standings_tool(self) -> Tool:
        return Tool(
            name="get_standings",
            func=self.get_standings,
            description="Get the current Six Nations championship standings.",
            args_schema=StandingsInput
        )

    @property
    def get_team_stats_tool(self) -> Tool:
        return Tool(
            name="get_team_stats",
            func=self.get_team_stats,
            description="Get detailed statistics for a specific team",
            args_schema=TeamStatsInput
        )

    _data = SixNationsData()

    def update_team_stats(
        self,
        team: str,
        played: int,
        won: int,
        lost: int,
        drawn: int,
        points_for: int,
        points_against: int,
        bonus_points: int
    ) -> str:
        """Update statistics for a specific team.
        
        Args:
            team: Team name (e.g., 'Ireland', 'England')
            played: Number of matches played
            won: Number of matches won
            lost: Number of matches lost
            drawn: Number of matches drawn
            points_for: Points scored by team
            points_against: Points conceded by team
            bonus_points: Bonus points earned
        """
        stats = TeamStats(
            played=played,
            won=won,
            lost=lost,
            drawn=drawn,
            points_for=points_for,
            points_against=points_against,
            bonus_points=bonus_points
        )
        self._data.update_team_stats(team, stats)
        return f"Updated statistics for {team}" 