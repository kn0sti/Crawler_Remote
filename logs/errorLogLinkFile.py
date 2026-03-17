def writeFileLog(link, Error, date):
    with open(r"C:/Users/Konstantin/Documents/Orivan/TestDaten/Objekte/Error/linkLog.txt", "a") as f:
            f.write("Error: " + Error + " - Link: " + link + " - Datum: " + date +"\n")