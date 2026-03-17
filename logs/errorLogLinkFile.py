from pathlib import Path

ROOT = Path(__file__).parent.parent
log = ROOT / "logs" / "errorLogLinkFile.log"


def writeFileLog(link, Error, date):
    with open(log, "a") as f:
            f.write("Error: " + Error + " - Link: " + link + " - Datum: " + date +"\n")

if __name__ == "__main__":
    writeFileLog("Test", "https://www.test.de", "2024-06-01 12:00:00")