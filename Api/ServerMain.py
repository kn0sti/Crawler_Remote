from fastapi import FastAPI
from Crawler.CrawlerMain import CrawlerMain
import uvicorn

#dauerhafte instanzen
app = FastAPI()
crawler = CrawlerMain()

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

if __name__ == "__main__":
    uvicorn.run("Api.ServerMain:app", host="0.0.0.0", port=8080)