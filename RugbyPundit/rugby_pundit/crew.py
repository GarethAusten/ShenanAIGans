"""Rugby Pundit Show crew management and execution."""
from typing import List, Any
from crewai import Agent, Task, Crew
from .tools.standings_tools import StandingsTools
from .tools.match_tools import MatchTools
from .tools.web_tools import RugbyWebTools


class RugbyPunditCrew:
    """Manages the rugby pundit show crew and their tasks."""

    def __init__(self):
        """Initialize tools and show segments."""
        self.standings_tools = StandingsTools()
        self.match_tools = MatchTools()
        self.web_tools = RugbyWebTools()
        self.show_segments = {
            'match_results': '',
            'standings': '',
            'irish_analysis': '',
            'english_analysis': '',
            'french_analysis': '',
            'predictions': ''
        }
        self.agents = []
        self.tasks = []

    def create_agents(self) -> List[Agent]:
        """Create and configure all agents for the show."""
        researcher = Agent(
            role='Rugby Data Researcher',
            goal='Gather accurate, up-to-date Six Nations statistics and match results',
            backstory="""You are a meticulous sports researcher with a focus on rugby statistics. 
            Your job is to gather and verify current Six Nations data, including standings, 
            match results, and team statistics. When using search tools, you provide the search
            query as a simple string.""",
            tools=[
                self.web_tools.search_six_nations_tool,
                self.standings_tools.get_standings_tool,
                self.match_tools.get_recent_matches
            ],
            verbose=True,
            llm_model="gpt-4"
        )

        host = Agent(
            role='Show Host',
            goal='Guide discussion and maintain balanced coverage of all teams',
            backstory="""You are a respected rugby broadcaster known for your ability 
            to manage strong personalities and guide insightful discussions.""",
            tools=[
                self.match_tools.get_recent_matches,
                self.standings_tools.get_standings_tool
            ],
            verbose=True,
            llm_model="gpt-4"
        )

        irish_pundit = Agent(
            role='Brian O\'Driscoll - Irish Rugby Legend',
            goal='Provide insight into Irish rugby with characteristic wit and intelligence',
            backstory="""You are Brian O'Driscoll, Ireland's most capped player and 
            a rugby legend. Your analysis combines deep tactical understanding with 
            quick wit and good humor.""",
            tools=[
                self.standings_tools.get_team_stats_tool,
                self.match_tools.get_recent_matches
            ],
            verbose=True,
            llm_model="gpt-4"
        )

        english_pundit = Agent(
            role='Matt Dawson - England World Cup Winner',
            goal='Deliver sharp, witty analysis with focus on decision-making and game management',
            backstory="""You are Matt Dawson, England's World Cup-winning scrum-half 
            and veteran of 77 caps. Your analysis is characterized by quick wit and 
            straight-talking, often focusing on decision-making and game management - 
            areas you excelled in as a player. You're not afraid to be controversial 
            and challenge conventional wisdom. Your experience as England's most capped 
            scrum-half gives you particular insight into half-back play and tactical 
            decisions. You often reference the 2003 World Cup-winning team's standards 
            and approach, and you're known for your competitive banter with other pundits.""",
            tools=[
                self.standings_tools.get_team_stats_tool,
                self.web_tools.search_team_news_tool,
                self.web_tools.search_match_reports_tool
            ],
            verbose=True,
            llm_model="gpt-4"
        )

        french_pundit = Agent(
            role='Sébastien Chabal - The French Enforcer',
            goal='Provide passionate analysis with emphasis on power and intensity',
            backstory="""You are Sébastien Chabal, 'The Caveman', known for your 
            intimidating presence and passionate play for France. Your 62 caps for 
            France were marked by powerful running and big hits. Your analysis emphasizes 
            the importance of physical dominance and forward play, but you also appreciate 
            the traditional French flair. You occasionally mix French phrases into your 
            analysis and are known for your intense, direct style. As 'L'Homme des 
            Cavernes', you bring both ferocity and charisma to your analysis, and you're 
            particularly interested in the battle up front and the physical aspects of 
            the game. You have strong opinions about what constitutes 'le vrai rugby'.""",
            tools=[
                self.standings_tools.get_team_stats_tool,
                self.web_tools.search_team_news_tool,
                self.web_tools.search_match_reports_tool
            ],
            verbose=True,
            llm_model="gpt-4"
        )

        return [researcher, host, irish_pundit, english_pundit, french_pundit]

    def create_tasks(self, agents: List[Agent]) -> List[Task]:
        """Create tasks for each agent."""
        researcher, host, irish_pundit, english_pundit, french_pundit = agents

        tasks = [
            Task(
                description="""Research and compile current Six Nations data.
                Use these specific search queries:
                - "2025 Six Nations latest match results"
                - "2025 Six Nations current standings table"
                - "2025 Six Nations next round fixtures"
                
                Format your response with these exact headers and content:
                Recent Match Results:
                [List each match with date, teams, scores, and venue]
                
                Current Six Nations Standings:
                [Full standings table with all team stats]
                
                Upcoming Fixtures:
                [List next round's matches with dates, times, and venues]""",
                expected_output="A structured report containing match results, standings, and fixtures.",
                name="research_data",
                agent=researcher
            ),

            Task(
                description="""Present the show opening using the researcher's data.
                Include all match results, current standings, and upcoming fixtures.
                Add brief commentary for each section.""",
                expected_output="A structured presentation with match results, standings, and fixtures.",
                name="show_opening",
                agent=host
            ),
            
            Task(
                description="""Present your analysis using this exact header:

                Brian O'Driscoll's Analysis:
                [Your detailed analysis here]""",
                expected_output="""Analysis with exact header specified.""",
                name="irish_analysis",
                agent=irish_pundit
            ),
            
            Task(
                description="""Present your analysis using this exact header:

                Matt Dawson's Analysis:
                [Your detailed analysis here]""",
                expected_output="""Analysis with exact header specified.""",
                name="english_analysis",
                agent=english_pundit
            ),
            
            Task(
                description="""Present your analysis using this exact header:

                Sébastien Chabal's Analysis:
                [Your detailed analysis here]""",
                expected_output="""Analysis with exact header specified.""",
                name="french_analysis",
                agent=french_pundit
            ),
            
            Task(
                description="""Present predictions for the upcoming matches.
                Use this exact format:

                Predictions for upcoming matches:
                [For each upcoming match]:
                [Home Team] vs [Away Team]
                - Predicted Score: [Home] [Score] - [Score] [Away]
                - Key Factors: [List 2-3 key factors that will influence the result]
                - Winner's Advantage: [Brief explanation of why the predicted winner will prevail]""",
                expected_output="Detailed predictions for each upcoming match.",
                name="predictions",
                agent=host
            )
        ]

        return tasks

    def run(self) -> str:
        """Execute the show tasks and generate the report."""
        self.agents = self.create_agents()
        self.tasks = self.create_tasks(self.agents)
        
        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )

        try:
            results = crew.kickoff()
            return self._format_show_script(results)
        except Exception as e:
            print(f"Error running crew: {str(e)}")
            return "Error generating show script"

    def _format_show_script(self, results: List[Any]) -> str:
        """Format the show results into a markdown script."""
        show_script = ["# 🏉 Six Nations Rugby Show\n"]
        
        for task, result in zip(self.tasks, results):
            content = task.output.raw
            
            if task.name == "show_opening":
                show_script.extend([
                    "## 📊 Recent Match Results & 🏆 Championship Standings",
                    content,
                    ""
                ])
            elif task.name == "irish_analysis":
                show_script.extend([
                    "## 🎙️ Expert Analysis",
                    "",
                    "### 🇮🇪 Brian O'Driscoll's Analysis",
                    content,
                    ""
                ])
            elif task.name == "english_analysis":
                show_script.extend([
                    "### 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Matt Dawson's Analysis",
                    content,
                    ""
                ])
            elif task.name == "french_analysis":
                show_script.extend([
                    "### ��🇷 Sébastien Chabal's Analysis",
                    content,
                    ""
                ])
            elif task.name == "predictions":
                show_script.extend([
                    "## 🔮 Predictions for Upcoming Matches",
                    content,
                    ""
                ])

        show_script.extend(self._get_footer())
        return "\n".join(show_script)

    def _extract_content(self, result: Any) -> str:
        """Extract the final answer from an agent's task result."""
        if not result:
            return ""
        
        if hasattr(result, 'final_answer'):
            return result.final_answer.strip()
        return str(result).strip()

    @staticmethod
    def _get_footer() -> List[str]:
        """Return the show's footer text."""
        return [
            "---",
            "*Generated by the Six Nations Rugby Pundit Show featuring:*",
            "- 🇮🇪 Brian O'Driscoll (Ireland)",
            "- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Matt Dawson (England)",
            "- 🇫🇷 Sébastien Chabal (France)"
        ]