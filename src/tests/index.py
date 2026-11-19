while input != "2":
    query = input("1 = uusi viite,  2 = lopeta: ")

    author = input("Tekijä(t): ")
    title = input("Otsikko: ")

    print(f"Luotu viite: {author}, {title}")

    if query == "2":
        break