# Rugby Pundit Show 🏉

An AI-powered rugby analysis system that generates detailed Six Nations Championship reports and analysis using a panel of virtual rugby experts.

## Features

- 🎙️ Virtual pundit panel featuring rugby legends
- 📊 Live match results and standings
- 🔍 Detailed match analysis
- 🔮 Match predictions
- 📈 Team statistics and performance tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rugby-pundit.git
cd rugby-pundit
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export OPENAI_API_KEY="your-api-key"
export GOOGLE_API_KEY="your-google-api-key"
export GOOGLE_CSE_ID="your-custom-search-engine-id"
```

## Usage

Run the show generator:
```bash
python __main__.py
```

This will:
1. Generate a detailed rugby analysis report
2. Save the report as `rugby_report.md`
3. Include match results, standings, and expert analysis

## Project Structure

```
rugby_pundit/
├── data/
│   └── six_nations_data.py     # Data structures and storage
├── tools/
│   ├── match_tools.py          # Match-related tools
│   ├── standings_tools.py      # Standings and statistics tools
│   └── web_tools.py           # Web search tools
├── crew.py                    # Main crew management
├── __init__.py
└── __main__.py               # Entry point
```

## Virtual Pundits

- 🇮🇪 **Brian O'Driscoll**: Irish rugby legend, known for tactical insight
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Matt Dawson**: England World Cup winner, focuses on game management
- 🇫🇷 **Sébastien Chabal**: French enforcer, emphasizes power and intensity

## Dependencies

- Python 3.9+
- crewai
- langchain
- pydantic
- python-dotenv

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 