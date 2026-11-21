from refmanager.app import App
from refmanager.config import DATABASE_FILE
from refmanager.db.sqlite_reference_repository import SqliteReferenceRepository
from refmanager.io.console_io import ConsoleIO

def main() -> None:
    console_io = ConsoleIO()
    repository = SqliteReferenceRepository(db_file=DATABASE_FILE)
    app = App(ref_repository=repository, io=console_io)
    
    while True:
        query = input("1 = Lisää viite, 0 = Lopeta: ")
        
        if query == "0":
            break
        
        if query == "1":
            app.run(command="new")
        else:
            print("Virheellinen valinta")

    repository.get_db_connection().close()

if __name__ == "__main__":
    main()