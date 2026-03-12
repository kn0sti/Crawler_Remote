def writeLog(status, link, date):
    status = str(status.status_code) 
    with open(r"C:\Users\Kollmaier\OneDrive - Private Berufsakademie für Aus- und Weiterbildung Passau gGmbH\Dokumente\Privat\PrivatNeu\pythonTest\PyScript\errorLog\networkLog.txt", "a") as f:
            f.write("Status: " + status + " - Link: " + link + " - Datum: " + date +"\n")

