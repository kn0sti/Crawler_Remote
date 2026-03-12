def writeFileLog(link, Error, date):
    with open(r"C:\Users\Kollmaier\OneDrive - Private Berufsakademie für Aus- und Weiterbildung Passau gGmbH\Dokumente\Privat\PrivatNeu\pythonTest\PyScript\errorLog\linkLog.txt", "a") as f:
            f.write("Error: " + Error + " - Link: " + link + " - Datum: " + date +"\n")