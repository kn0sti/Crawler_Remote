import sqlite3

def createDB():
    conn = sqlite3.connect("visistedURL.db")
    cur = conn.cursor()
    #Status: 0 - Unbearbeitet | 1 - Geladen | 2 - Fehler | 3 - Fertig
    cur.execute("CREATE TABLE IF NOT EXISTS visitedURL (url TEXT PRIMARY KEY, status INT, number INT AUTO INCREMENT)")
    conn.commit()
    return conn

# == ÜBERARBEITEN ==

def checkDB(link) -> bool:
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM visitedURL WHERE url = (?)", (link,))
    b00l = cur.fetchone() is not None
    conn.close()
    return b00l

def insertLink(link):
    conn = createDB()
    conn.execute("INSERT INTO visitedURL(url) VALUES (?)", (link,))
    conn.commit()

def getAll():
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM visitedURL")
    ans = cur.fetchall()
    print(ans)

def externLinks(links):
    try:
        for link in links:
            with open(r'C:\Users\Kollmaier\OneDrive - Private Berufsakademie für Aus- und Weiterbildung Passau gGmbH\Dokumente\Privat\PrivatNeu\pythonTest\nextLinks.csv', "a") as f:
                f.write(link +",\n")
    except Exception as e:
        print(f"Fehler beim externen Link schreiben: {e}")

def newLinks(links, url):
    try:
        fertigerLink = []
        for link in links:
            fertigerLink.append(url + link)
        for link in fertigerLink:
            with open(r'C:\Users\Kollmaier\OneDrive - Private Berufsakademie für Aus- und Weiterbildung Passau gGmbH\Dokumente\Privat\PrivatNeu\pythonTest\nextLinks.csv', "a") as f:
                f.write("http://" + link +",\n")
    except Exception as e:
        print(f"Fehler in newLinks: {e}")
    

if __name__ == "__main__":
    getAll()
