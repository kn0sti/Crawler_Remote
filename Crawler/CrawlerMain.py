from Crawler.HtmlLogik import WebBrowserLogik as wBL
import threading

class CrawlerMain:
    def __init__(self):
        self.running = False
        self.logik = None
        self.thread = None

    def start(self):
        try:
            if not self.running:
                self.logik = wBL.Logik(test=False)
                self.thread = threading.Thread(target=self.logik.start)
                self.thread.start()
                self.running = True
            print("\nCrawler started\n")
        except Exception as e:
            print("Fehler beim Starten des Crawlers: ", e)
            return
        
    def test(self):
        try:
            if not self.running:
                self.logik = wBL.Logik(test=True, link = "")
                self.thread = threading.Thread(target=self.logik.test)
                self.thread.start()
                self.running = True
            print("\nCrawler im Testmodus gestartet\n")
        except Exception as e:
            print("Fehler beim Starten des Crawlers im Testmodus: ", e)
            return


    def stop(self):
        if self.logik:
            self.logik.stop()
        self.running = False
        print("\nCrawler stopped\n")