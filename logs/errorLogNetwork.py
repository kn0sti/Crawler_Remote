from pathlib import Path

ROOT = Path(__file__).parent.parent
log = ROOT / "logs" / "errorLogNetwork.log"

def writeLog(status, link, date):
    status = str(status.status_code) 
    with open(log, "a") as f:
            f.write("Status: " + status + " - Link: " + link + " - Datum: " + date +"\n")

