def getTextInChunks(text):
    chunks = []
    zeichenAnzahl = 0
    größeEinesChunks = 1500

    while zeichenAnzahl < len(text):
        Ende = zeichenAnzahl + größeEinesChunks
        #damit kann man einfach text ausschneiden
        abschnitt = text[zeichenAnzahl:Ende]
        chunks.append(abschnitt.strip())
        #soll anscheinend besser sein wenn überlappend
        zeichenAnzahl = Ende - 150

    return chunks
