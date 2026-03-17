def writeLog(status, link, date):
    status = str(status.status_code) 
    with open(r"C:/Users/Konstantin/Documents/Orivan/TestDaten/Objekte/Error/networkLog.txt", "a") as f:
            f.write("Status: " + status + " - Link: " + link + " - Datum: " + date +"\n")

