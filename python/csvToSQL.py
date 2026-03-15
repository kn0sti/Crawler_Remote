from Crawler.DataBase import urlCheckerDB as DB
import csv, sqlite3
from pathlib import Path

if __name__ == "__main__":

    ROOT = Path(__file__).resolve().parent.parent
    csv_path = ROOT / "nextLinks.csv"

    counter = 0
    fehlgeschlagen = 0

    conn = sqlite3.connect("URLS.db")
    cur = conn.cursor()

    with open(csv_path, "r") as file:
        csvFile = csv.reader(file)

        for zeile in csvFile:
            link = zeile[0]

            try:
                cur.execute(
                "INSERT INTO visitedURL (url, status) VALUES (?, ?)",
                (link, 0,)
                )
            except Exception as e:
                fehlgeschlagen += 1
            counter += 1

    conn.commit()
    conn.close()

    print(f"Hinzugefügt: {counter - fehlgeschlagen} Fehlgeschlagen: {fehlgeschlagen}")