from fastapi import FastAPI
from Crawler.CrawlerMain import CrawlerMain
from Crawler.DataBase import urlCheckerDB as db
import uvicorn

#dauerhafte instanzen
app = FastAPI()
crawler = CrawlerMain()

#Wenn windows Ausgeführt wird, http://192.168.178.102:8080/startCrawler
#App wird mit Main.py ausgeführt
def startServer(port = 8080):
    uvicorn.run("Api.ServerMain:app", host="0.0.0.0", port=port)

@app.get("/")
def root():
    return {"status" : "server running"}

@app.get("/startCrawler")
def startCrawler():
    if not crawler.running:
        crawler.start()
    return {"status" : "start"}

@app.get("/stopCrawler")
def stopCrawler():
    crawler.stop()
    return {"status" : "stop"}

@app.get("/testCrawler")
def testCrawler():
    if not crawler.running:
        crawler.test()
    return {"status" : "test"}

@app.get("/getStatus")
def getStatus():
    anzahlLinks = db.getAnzahlLinks(), db.getAnzahlFertigerLinks()
    return {"running" : crawler.running, "Links" : anzahlLinks[0], "Fertig" : anzahlLinks[1]}

if __name__ == "__main__":
    uvicorn.run("Api.ServerMain:app", host="0.0.0.0", port=8080)