from bs4 import BeautifulSoup as BS
import re
from DataBase import urlCheckerDB as dB

#link finder
def getAllLinks(soup):
    #suchen nach a tags in html
    links = BS.find_all(soup, "a")
    listelinks = []
    externLink = []
    filters = ["#", "https://", "http://", ".jpg", ".mov", ".mp4", ":", ".php", ".js"]
    #jeden a durchgehen
    for link in links:
        #value vom link bekommen
        href = link.get("href")
        #gleich mal schauen ob es nur der homelink ("/") is
        if len(href) < 2:
            #print(f"Zu kurz: {href}")
            continue

        #schauen ob es ein anderer dateityp is
        if href.__contains__(filters[0]) or href.__contains__(filters[6]) or href.__contains__(filters[7]) or href.__contains__(filters[8]):
            #print(f"Url ist JS oder eine ander Unterseite: {href}")
            continue

        #schauen ob es ein link nach außerhalb ist
        if href.__contains__(filters[1]) or href.__contains__(filters[2]):
            externLink.append(href)
            continue

        listelinks.append(href)

    #externe links
    dB.externLinks(externLink)
    return listelinks

# Methode zum entfernen unnützer tags
def unnützeTags(html):
    soup = BS(html, "html.parser")
    newLinks = None
    #
    try:
        newLinks = getAllLinks(soup)
    except Exception as e:
        print(f"Fehler bei Methoden Aufruf - getAllLinks: {e}")
    # Tags die nicht gebraucht werden entfernen
    unbrauchbar = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'iframe', 'noscript', 'svg', 'head', 'code']
    for element in soup(unbrauchbar):
        element.decompose()
    return soup, newLinks

# Main content rausfinden und titel
def getTitelandMain(html):
    # Andere methode aufrufen zum tags entfernen
    soup = None
    links = None
    try:
        answer = unnützeTags(html)
        soup = answer[0]
        links = answer[1]
    except Exception as e:
        print(f"Fehler in htmlExtractor - unnütze Tags: {e}")
    
    #titel für den artikel rausfinden
    h1_tag = soup.find("h1")
    if h1_tag:
        head = h1_tag.get_text(separator=" ", strip=True)
    elif soup.title:
        head = soup.title.get_text(separator=" ", strip=True)
    else:
        head = "Kein Titel gefunden"

    #herausfinden ob seite moderne tags nutzt
    moderneTags = soup.find('article') or soup.find('main')

    # Abfrage
    if moderneTags:
        #moderne tags werden hergenommen
        text = moderneTags.get_text(separator=" ", strip=True)
    else:
        #keine modernen tags und wenn kein body dann alles
        if soup.body:
            text = soup.body.get_text(separator=" ", strip=True)
        else:
            text = soup.get_text(separator=" ", strip=True)

    #danke an gemini für das entfernen von patterns
    body = re.sub(r'\s+', ' ', text).strip()
    
    return head, body, links

if __name__ == "__main__":
    text= """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Mein Blog - Python Crawler Tipps</title>
    <style> body { font-family: sans-serif; } .ads { color: red; } </style>
    <script> function trackUser() { console.log("Tracking..."); } </script>
</head>
<body>

    <header>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/shop">Shop</a></li>
                <li><a href="/login">Anmelden</a></li>
                <li><a href="#try">try</a></li>
            </ul>
        </nav>
    </header>

    <aside class="sidebar">
        <div class="ads">
            <h3>WERBUNG</h3>
            <p>Kaufen Sie jetzt diese Socken für nur 9,99€!</p>
        </div>
        <div class="related">
            <h4>Beliebte Beiträge</h4>
            <ul>
                <li>Wetter heute</li>
                <li>Kuchenrezepte</li>
            </ul>
        </div>
    </aside>

    <main>
        <article>
            <h1>Warum Web-Scraping mit Python Spaß macht</h1>
            <p>Hier beginnt der wertvolle Text für deine KI. Web-Scraping ist eine Technik, um Daten von Webseiten zu extrahieren. Mit Bibliotheken wie BeautifulSoup kann man den HTML-Baum durchsuchen.</p>
            <p>Man sollte darauf achten, die Server nicht zu überlasten. Ein kleines <code>time.sleep()</code> wirkt oft Wunder und verhindert Sperren.</p>
        </article>
    </main>

    <div id="cookie-banner">
        Diese Seite nutzt Cookies. <button>Akzeptieren</button>
    </div>

    <footer>
        <p>&copy; 2026 Mein Webcrawler-Blog. Alle Rechte vorbehalten.</p>
        <a href="/impressum">Impressum</a> | <a href="/datenschutz">Datenschutz</a>
    </footer>

</body>
</html>"""
#getTitelandMain(text)