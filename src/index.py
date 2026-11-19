TYPES = {"1": "kirja", "2": "artikkeli", "3": "verkkosivu"}

while True:
    query = input("1 = Lisää viite, 0 = Lopeta: ") # kysely ja lisää tai lopeta 
    if query == "0":
        break

    if query == "1":
        author = input("Tekijä(t): ")
        title = input("Otsikko: ")
        year = input("Julkaisuvuosi: ")

        while (choice := input("Tyyppi (1 = kirja, 2 = artikkeli, 3 = verkkosivu): ")) not in TYPES:
            print("Virheellinen valinta.")

        source_type = TYPES[choice]
        key = input("Avain (esim. ABC12): ")

        print(f"Lisätty viite: {author}, {title}, {year}, {source_type}, {key}")