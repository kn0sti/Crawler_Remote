from fastapi import FastAPI
from Crawler.CrawlerMain import CrawlerMain
import uvicorn

#dauerhafte instanzen
app = FastAPI()
crawler = CrawlerMain()

@app.get("/")
def root():
    return {"status" : "server running"}

@app.post("/startCrawler")
def startCrawler():
    if not crawler.running:
        crawler.start()
    return {"status" : "start"}

@app.post("/stopCrawler")
def stopCrawler():
    crawler.stop()
    return {"status" : "stop"}

if __name__ == "__main__":
    uvicorn.run("Api.ServerMain:app", host="0.0.0.0", port=8080)