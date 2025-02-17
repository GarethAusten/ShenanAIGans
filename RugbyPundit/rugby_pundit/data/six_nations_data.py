"""Data structures and storage for Six Nations rugby data."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

@dataclass
class TeamStats:
    played: int = 0
    won: int = 0
    lost: int = 0
    drawn: int = 0
    points_for: int = 0
    points_against: int = 0
    bonus_points: int = 0
    
    @property
    def total_points(self) -> int:
        return (self.won * 4) + (self.drawn * 2) + self.bonus_points

@dataclass
class Match:
    date: datetime
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    venue: str

class SixNationsData:
    def __init__(self):
        self.standings: Dict[str, TeamStats] = {
            "Ireland": TeamStats(),
            "France": TeamStats(),
            "Scotland": TeamStats(),
            "England": TeamStats(),
            "Wales": TeamStats(),
            "Italy": TeamStats()
        }
        self.matches: List[Match] = []

    def update_team_stats(self, team: str, stats: TeamStats):
        """Update statistics for a team."""
        if team in self.standings:
            self.standings[team] = stats

    def add_match(self, match: Match):
        """Add a match result."""
        self.matches.append(match)
        # Update team statistics based on match result
        self._update_stats_from_match(match)

    def _update_stats_from_match(self, match: Match):
        """Update team statistics based on match result."""
        # Update home team stats
        home_stats = self.standings[match.home_team]
        home_stats.played += 1
        home_stats.points_for += match.home_score
        home_stats.points_against += match.away_score

        # Update away team stats
        away_stats = self.standings[match.away_team]
        away_stats.played += 1
        away_stats.points_for += match.away_score
        away_stats.points_against += match.home_score

        # Determine winner and update W/L/D
        if match.home_score > match.away_score:
            home_stats.won += 1
            away_stats.lost += 1
        elif match.away_score > match.home_score:
            away_stats.won += 1
            home_stats.lost += 1
        else:
            home_stats.drawn += 1
            away_stats.drawn += 1

    def get_team_stats(self, team: str) -> TeamStats:
        """Get statistics for a specific team."""
        return self.standings.get(team, TeamStats())

    def get_recent_matches(self, limit: int = 10) -> List[Match]:
        """Get the most recent matches, up to the specified limit."""
        sorted_matches = sorted(self.matches, key=lambda x: x.date, reverse=True)
        return sorted_matches[:limit] 