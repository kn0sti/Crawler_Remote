import webbrowser, requests, datetime, time, csv, HtmlLogik as hE, Chunks as ch, json
from logs import errorLogNetwork as eL, errorLogLinkFile as elF
from DataBase import urlCheckerDB as db

def openPage(link, url):
    link = link + url
    webbrowser.open(link)

class Logik:
    #methode zur auswertung einfacher links
    def getHtml(self):
        try:
            headers = {'User-Agent': 'KonstiCrawler (educational project, polite crawler) (contact: konstikollmaier@gmail.com)'}
            answer = requests.get(self.link, headers=headers)
            html = answer.content.decode("utf-8")
            self.indE.updateLadeBar(40)
            return html
        except Exception as e:
            print(f"Fehler beim getHtml: {e}")
            eL.writeLog(answer, self.link, str(datetime.datetime.now()))
            return answer

    #methode zum auswerten der listen
    def getArray(self):
        typ = self.link.split(".")
        counter = 0
        if(typ[-1] == "csv"):
            with open(self.link, mode="r") as Datei:
                csvDatei = csv.reader(Datei)
                for Zeilen in csvDatei:
                    #counter für anzeige
                    counter += 1
                    self.indE.counter(counter, len(Zeilen))
                    for obj in Zeilen:
                        if(obj != ""):
                            if not (db.checkDB(str(obj))):
                                self.link = obj
                                self.startCrawl()
                                print(f"Fertig mit{self.link}")
                                time.sleep(60)
                            else:
                                print(f"Datensatz wurde schon bearbeitet: {str(obj)}")
                                time.sleep(10)
                                continue
                print("Alle Daten durch!")

    #methode zum link zerlegen
    def getHost(self):
        try:
            self.uncutHttps = self.link.split("//")
            self.host = self.uncutHttps[1].split("/")
            self.DateiName = self.host[0] + ".jsonl"
            return self.DateiName
        except Exception as e:
            print(f"Fehler in getHost() bei {self.link} : {e}")

    #methode zur jsonl dateierstellung
    def createData(self):
        dateiname = self.getHost()
        link = "".join(self.ordner)
        link = link + "/" + str(dateiname)
        try:
            html = self.getHtml()
            if not(isinstance("Response", type(html))):
                print("Rückgabe Fehlerhaft!")
                return None
            else:
                #jsonl datei öffnen mit hostname von seite           
                self.data = open(link, "a", encoding='UTF-8')
                try:
                    #html von request filter und in list zurück geben
                    self.cleanHtml = hE.getTitelandMain(html)
                    db.newLinks(self.cleanHtml[2], self.host[0])
                except Exception as e:
                    elF.writeFileLog(self.link, str(e), str(datetime.datetime.now()))
                    print("Fehler bei Tags entfernen", e)
                    return None
                try:
                    #chunken in längen von 1500 zeichen
                    self.chunks = ch.getTextInChunks(self.cleanHtml[1])
                except Exception as e:
                    #elF.writeFileLog(self.link, str(e), str(datetime.datetime.now()))
                    print("Fehler beim chunken", e)
                    return None
                #für jeden chunk ein objekt erstellen und in text datei schreiben
                for i, chunk in enumerate(self.chunks):
                    jsonObjekt = {
                        "id": f"{self.cleanHtml[0]}_{i}",
                        "url": f"{self.link}",
                        "datum": f"{str(datetime.datetime.now())}",
                        "chunk": f"{chunk}"
                    }
                    self.data.write(json.dumps(jsonObjekt, ensure_ascii=False ))
                self.indE.updateLadeBar(100)
                db.insertLink(self.link)
                return None
        except Exception as e:
            elF.writeFileLog(self.link, str(e), str(datetime.datetime.now()))
            print("Fehler beim öffnen: ", e)
            return None
    
    #start
    def startCrawl(self):
        #startet denn vorgang
        self.createData()
        
    #konstruktor
    def __init__(self, ordner, list, link, instanceDE, test = False):
        self.indE = instanceDE  
        self.link = link
        self.list = list
        self.ordner = ordner

        if test:
            print(f"Test für lokale ausführung")
            a = self.getHost()
            print(f"Dateiname: {self.DateiName}")
            a = self.ordner + "/" + a
            print(f"Veränderter Dateiname: {a}")

        else:
            if self.list:
                self.array = self.getArray()
            else:
                self.startCrawl()
                print(f"Fertig mit {self.host[1]}")
        


#unittest oder so
if __name__ == "__main__":
    m = Logik("c:/Users/Konstantin/Documents/Orivan/TestDaten/Objekte", "", "https://de.wikipedia.org/wiki/Personal_Computear", "", True)
    print()