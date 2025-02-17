import os
from rugby_pundit.crew import RugbyPunditCrew

os.environ["REQUESTS_CA_BUNDLE"] = os.environ.get("REQUESTS_CA_BUNDLE", "")
os.environ["SSL_CERT_FILE"] = os.environ.get("SSL_CERT_FILE", "")

def generate_report():
    crew = RugbyPunditCrew()
    report = crew.run()
    
    # Save to markdown file
    with open("rugby_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print("Report generated successfully!") 