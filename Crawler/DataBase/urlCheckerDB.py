import sqlite3

def createDB():
    conn = sqlite3.connect("URLS.db", timeout=30)
    cur = conn.cursor()
    #Status: 0 - Unbearbeitet | 1 - Geladen | 2 - Fehler | 3 - Fertig
    cur.execute("CREATE TABLE IF NOT EXISTS visitedURL (url TEXT PRIMARY KEY UNIQUE, status INT, number INT AUTO_INCREMENT)")
    conn.commit()
    return conn

# == ÜBERARBEITEN ==

def delete():
    conn = createDB()
    conn.execute("DELETE FROM visitedURL WHERE url = (?)", ("wikipedia.com",))
    conn.commit()
    conn.close()

#links zurücksetzen
def resetDB():
    conn = createDB()
    conn.execute("UPDATE visitedURL SET status = (?) Where status != (?)", (0, 0,))
    conn.commit()
    conn.close()

#error handling links
def errorLink(link):
    conn = createDB()
    conn.execute("UPDATE visitedURL SET status = (?) Where url = (?)", (2, link,))
    conn.commit()
    conn.close()

def linksabgeschlossen(links):
    conn = createDB()
    for link in links:
        conn.execute("UPDATE visitedURL SET status = (?) Where url = (?) AND status != 2", (3, link,))
    conn.commit()
    conn.close()

#liste an links holen
def getUnbearbeiteteURL(limit):
    conn = createDB()
    cur = conn.cursor()

    # Links holen
    cur.execute(
        "SELECT url FROM visitedURL WHERE status = 0 LIMIT ?",
        (limit,)
    )

    rows = cur.fetchall()

    urls = [row[0] for row in rows]

    # Status auf bearbeitet setzen
    cur.executemany(
        "UPDATE visitedURL SET status = 1 WHERE url = ?",
        [(url,) for url in urls]
    )

    conn.commit()
    conn.close()

    return urls

#links einfügen
def insertLinks(link):
    if link.__contains__("https://") or link.__contains__("http://"):
        conn = createDB()
        try:
            conn.execute("INSERT INTO visitedURL(url, status) VALUES (?, ?)", (link, 0,))
        except Exception as e:
            print(f"Fehler in insertLinks bei {link}: {e}")
            return False
        conn.commit()
        conn.close()
        return True
    return False

def insertLink(link):
    conn = createDB()
    conn.execute("INSERT OR IGNORE INTO visitedURL(url, status) VALUES (?, ?)", (link, 0,))
    conn.commit()

def getAll():
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM visitedURL")
    ans = cur.fetchall()
    return ans
   
#get anzahl links
def getAnzahlLinks():
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM visitedURL")
    ans = cur.fetchone()[0]
    return ans

def getAnzahlFertigerLinks():
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM visitedURL WHERE status = 3")
    ans = cur.fetchone()[0]
    return ans

def getAnzahlFehlerLinks():
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM visitedURL WHERE status = 2")
    ans = cur.fetchone()[0]
    return ans
    
def getAnzahlAndererLinks():
    conn = createDB()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*)FROM visitedURL WHERE status = 0 AND url LIKE '%wikipedia%';")
    ans = cur.fetchone()[0]
    print(f"Anzahl anderer Links: {ans}")
    return ans

if __name__ == "__main__":
    getAnzahlAndererLinks()

