class CrawlerMain:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        print("Crawler started")

    def stop(self):
        self.running = False
        print("Crawler stopped")