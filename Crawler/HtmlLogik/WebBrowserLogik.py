import webbrowser, requests, datetime, time, csv, json
from Crawler.HtmlLogik import htmlExtractor as hE
from Crawler.Chunks import chunker as ch
import logs.errorLogNetwork as eL
import logs.errorLogLinkFile as elF
from Crawler.DataBase import urlCheckerDB as db

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
            return html
        except Exception as e:
            print(f"Fehler beim getHtml: {e}")
            db.errorLink(self.link)
            eL.writeLog(answer, self.link, str(datetime.datetime.now()))
            return answer

    #Auswertung von Datenbank und vorladen der links
    def getLinkList(self):
        liste = []
        try:
            liste = db.getUnbearbeiteteURL(50)
            return liste
        except Exception as e:
            print(f"Fehler in getLinkList(): {e}")
        return False
    
    #methode zum auswerten der listen
    #def getArray(self):
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
                db.errorLink(self.link)
                print("Rückgabe Fehlerhaft!")
                return None
            else:
                #jsonl datei öffnen mit hostname von seite           
                self.data = open(link, "a", encoding='UTF-8')
                try:
                    #html von request filter und in list zurück geben
                    self.cleanHtml = hE.getTitelandMain(html)
                    #interne links parsen und speichern
                    for link in self.cleanHtml[2]:
                        try:
                            link = "http://" + self.host[0] + "/" + link
                            db.insertLink(link)
                        except Exception as e:
                            elF.writeFileLog(link, str(e), str(datetime.datetime.now()))
                            print(f"Fehler beim parsen interner Links: {e}")
                except Exception as e:
                    elF.writeFileLog(self.link, str(e), str(datetime.datetime.now()))
                    print("Fehler bei Tags entfernen", e)
                    return None
                try:
                    #chunken in längen von 1500 zeichen
                    self.chunks = ch.getTextInChunks(self.cleanHtml[1])
                except Exception as e:
                    elF.writeFileLog(self.link, str(e), str(datetime.datetime.now()))
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
                db.insertLink(self.link)
                return None
        except Exception as e:
            elF.writeFileLog(self.link, str(e), str(datetime.datetime.now()))
            print("Fehler beim öffnen: ", e)
            return None
    
    #start
    def startCrawl(self):
        #startet denn vorgang
        while self.running:
            links = self.getLinkList()
            print(f"Anzahl geholter Links: {len(links)}")
            for link in links:
                if not self.running: break
                self.link = link
                self.createData()
                time.sleep(1)
            db.linksabgeschlossen(links)

    #neuer konstruktor
    def __init__(self, test = False):
        self.ordner = "c:/Users/Konstantin/Documents/Orivan/TestDaten/Objekte/Jsonl"
        print(f"Gestartet im Testmodus")
        self.running = False

    def start(self):
        self.running = True
        self.startCrawl()

    def stop(self):
        self.running = False
        print("Crawler stopped")
        
        

#unittest oder so
if __name__ == "__main__":
    m = Logik("c:/Users/Konstantin/Documents/Orivan/TestDaten/Objekte", "", "https://de.wikipedia.org/wiki/Personal_Computear", "", True)
    print()