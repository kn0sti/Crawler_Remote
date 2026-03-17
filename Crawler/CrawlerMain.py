from Crawler.HtmlLogik import WebBrowserLogik as wBL

class CrawlerMain:
    def __init__(self):
        self.running = False
        self.logik = None

    def start(self):
        try:
            self.logik = wBL.Logik(True)
            self.running = True
            print("\nCrawler started\n")
        except Exception as e:
            print("Fehler beim Starten des Crawlers: ", e)
            return
        

    def stop(self):
        if self.logik:
            self.logik.stop()
        self.running = False
        print("\nCrawler stopped\n")