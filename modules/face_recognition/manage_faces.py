from modules.face_recognition.face_database import FaceDatabase


def show_menu():
    print("\n====== Face Management Menu ======")
    print("1. View enrolled identities")
    print("2. Delete a person")
    print("3. Update (re-enroll) a person")
    print("4. Database statistics")
    print("5. Exit")
    print("=================================")


def view_identities(db):
    identities = db.count_identities()
    samples = db.count_faces()

    print(f"\n[INFO] Total identities : {identities}")
    print(f"[INFO] Total face samples : {samples}")


def delete_person(db):
    name = input("Enter person name to delete: ").strip()
    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()

    if confirm == "y":
        db.secure_delete_person(name)
    else:
        print("[INFO] Delete operation cancelled")


def update_person(db):
    name = input("Enter person name to update: ").strip()
    confirm = input(f"Re-enroll '{name}'? Old data will be deleted (y/n): ").lower()

    if confirm == "y":
        db.update_person(name)
        print("[INFO] Now run the enrollment script to re-add the person")
    else:
        print("[INFO] Update operation cancelled")


def database_stats(db):
    print("\n====== Database Statistics ======")
    print(f"Total identities : {db.count_identities()}")
    print(f"Total face samples : {db.count_faces()}")
    print("================================")


def main():
    db = FaceDatabase()

    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            view_identities(db)

        elif choice == "2":
            delete_person(db)

        elif choice == "3":
            update_person(db)

        elif choice == "4":
            database_stats(db)

        elif choice == "5":
            print("[INFO] Exiting Face Management Tool")
            break

        else:
            print("[WARN] Invalid option. Please select again.")


if __name__ == "__main__":
    main()
