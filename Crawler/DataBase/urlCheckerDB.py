import sqlite3

def createDB():
    conn = sqlite3.connect("URLS.db")
    cur = conn.cursor()
    #Status: 0 - Unbearbeitet | 1 - Geladen | 2 - Fehler | 3 - Fertig
    cur.execute("CREATE TABLE IF NOT EXISTS visitedURL (url TEXT PRIMARY KEY, status INT, number INT AUTO_INCREMENT)")
    conn.commit()
    return conn

# == ÜBERARBEITEN ==

#liste an links holen
def getUnbearbeiteteURL(finish):
    conn = createDB()
    cur = conn.cursor()
    ans = []
    for i in range(finish + 1):
        #Nächstest link objekt holen
        cur.execute("SELECT * FROM visitedURL where status = 0")
        #link zur liste hinzu fügen
        ans.append(cur.fetchall())
        #kurze zwischen bearbeitung
        url = ans[i]
        #link auf 1 also geladen setzen
        conn.execute("UPDATE visitedURL set status = 1 where (?)", (url[0]))
        conn.commit()
    #verbindung schließen
    conn.close()
    #liste zurückgeben
    return ans

#links einfügen
def insertLinks(link):
    if link.__contains__("https://") or link.__contains__("http://"):
        conn = createDB()
        try:
            conn.execute("INSERT INTO visitedURL(url, status) VALUES (?, ?)", (link, 0,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Fehler in {link}: {e}")
            return False
        conn.close()
        return True
    return False

def checkDB(link) -> bool:
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM visitedURL WHERE url = (?)", (link,))
    b00l = cur.fetchone() is not None
    conn.close()
    return b00l

def insertLink(link):
    conn = createDB()
    conn.execute("INSERT INTO visitedURL(url, status) VALUES (?, ?)", (link, 0,))
    conn.commit()

def getAll():
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM visitedURL")
    ans = cur.fetchall()
    return ans

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
    insertLink("wikipedia.com")

