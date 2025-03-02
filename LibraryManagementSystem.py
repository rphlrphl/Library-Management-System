import datetime

class Book:
    def __init__(self, title="", author="", isbn="", available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available
        
    books = {
        1: {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'isbn': '9780345339683',
            'available': False
        },
        2: {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '9780451524935',
            'available': False
        },
        3: {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'isbn': '9780060850524',
            'available': True
        }
    }
        
    def book_record(self):
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'available': self.available
        }
        
    @classmethod
    def show_available_books(cls):
        available_books = [(key, book['title']) for key, book in cls.books.items() if book['available']]
        if available_books:
            for key, title in available_books:
                print(f'[ID: {key}] {title}')
            return True
        else:
            print('No Books Available.')
            return False
    
    @classmethod
    def add_book(cls, title, author, isbn):
        new_id = max(cls.books.keys()) + 1 if cls.books else 1
        cls.books[new_id] = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'available': True
        }
        print(f"Book '{title}' has been added with ID: {new_id}")
        
class FineSystem:
    FINE_RATE = 5
    
    @staticmethod
    def calculate_fine(return_date_str, actual_date=None):
        """
        Calculate fine based on days overdue
        return_date_str: string in format YYMMDD
        actual_date: datetime object (default is today)
        """
        if not return_date_str:
            return 0
            
        if actual_date is None:
            actual_date = datetime.datetime.now()
            
        try:
            # Parse the return date (YYMMDD format)
            year = int("20" + return_date_str[:2])  # Assuming 20XX years
            month = int(return_date_str[2:4])
            day = int(return_date_str[4:6])
            return_date = datetime.datetime(year, month, day)
            
            # Calculate days overdue
            if actual_date > return_date:
                days_overdue = (actual_date - return_date).days
                return days_overdue * FineSystem.FINE_RATE
            else:
                return 0
        except (ValueError, IndexError):
            print("Error in date calculation. Using zero fine.")
            return 0
    
    @staticmethod
    def format_date(date_str):
        """Convert YYMMDD to a readable date format"""
        if not date_str:
            return "N/A"
            
        try:
            year = int("20" + date_str[:2])
            month = int(date_str[2:4])
            day = int(date_str[4:6])
            return f"{year}-{month:02d}-{day:02d}"
        except (ValueError, IndexError):
            return date_str
            
class Member:
    members = {
        1: {
            'name': 'John James',
            'id_num': '202356789',
            'contact_num': '09123456789',
            'borrowed_book': {
                'title': 'The Hobbit',
                'return_date': '240301',  # Format changed to YYMMDD
                'book_id': 1
            },
            'fine_balance': 50,  # New field for tracking fines
            'fine_history': [
                {'amount': 50, 'date': '240305', 'paid': False, 'book': 'The Hobbit'}
            ]
        },
        2: {
            'name': 'James John',
            'id_num': '202309876',
            'contact_num': '09876543219',
            'borrowed_book': {
                'title': '1984',
                'return_date': '240310',
                'book_id': 2
            },
            'fine_balance': 0,
            'fine_history': []
        }
    }
    
    def __init__(self, name, id_num, contact_num):
        self.name = name
        self.id_num = id_num
        self.contact_num = contact_num
        
    def add_member(self):
        Member.members.update(
            {
                len(self.members) + 1: {
                    'name': self.name,
                    'id_num': self.id_num,
                    'contact_num': self.contact_num,
                    'borrowed_book': {
                        'title': None,
                        'return_date': None,
                        'book_id': None
                    },
                    'fine_balance': 0,
                    'fine_history': []
                }
            }
        )
            
    @classmethod
    def show_all_members(cls):
        if not cls.members:
            print("No members registered.")
            return
        
        print("\n----- MEMBER LIST -----")
        for key, member in cls.members.items():
            fine_status = " (Has unpaid fines)" if member['fine_balance'] > 0 else ""
            print(f"[ID: {key}] {member['name']} (ID: {member['id_num']}){fine_status}")
        print("----------------------")

class CurrentMemberDetails(Member):
    def account_details(self):
        for key in Member.members:
            if Member.members[key]['id_num'] == self.id_num:
                member = Member.members[key]
                fine_amount = member['fine_balance']
                borrowed_book = member['borrowed_book']['title'] or 'None'
                return_date = member['borrowed_book']['return_date']
                
                # Calculate current fine if book is borrowed
                current_fine = 0
                if borrowed_book != 'None' and return_date:
                    current_fine = FineSystem.calculate_fine(return_date)
                    
                print(f"""
                ----- ACCOUNT DETAILS -----
                Name: {member['name']}
                ID Number: {member['id_num']}
                Contact Number: {member['contact_num']}
                Borrowed Book: {borrowed_book}
                Return Date: {FineSystem.format_date(return_date) if return_date else 'N/A'}
                Outstanding Fine: ${fine_amount}
                Current Book Late Fee: ${current_fine} (if returned today)
                --------------------------
                """)
                return
        print("Member not found.")
                
    def borrowed_books(self):
        for key in Member.members:
            if Member.members[key]['id_num'] == self.id_num:
                book_title = Member.members[key]['borrowed_book']['title']
                return_date = Member.members[key]['borrowed_book']['return_date']
                
                if book_title:
                    # Check if the book is overdue
                    fine = FineSystem.calculate_fine(return_date)
                    overdue_msg = ""
                    if fine > 0:
                        overdue_msg = f"\n                    OVERDUE! Current late fee: ${fine}"
                        
                    print(f"""
                    ----- BORROWED BOOKS -----
                    Book: {book_title}
                    Return Date: {FineSystem.format_date(return_date)}{overdue_msg}
                    --------------------------
                    """)
                else:
                    print("\nYou haven't borrowed any books yet.")
                return
        print("Member not found.")
                
    def borrow_book(self, book_id, return_date):
        # Find the member
        member_key = None
        for key, member in Member.members.items():
            if member['id_num'] == self.id_num:
                member_key = key
                break
                
        if member_key is None:
            print("Member not found.")
            return False
            
        # Check for unpaid fines
        if Member.members[member_key]['fine_balance'] > 0:
            print(f"You have an outstanding fine of ${Member.members[member_key]['fine_balance']}.")
            print("Please pay your fine before borrowing another book.")
            return False
            
        # Check if member already has a book
        if Member.members[member_key]['borrowed_book']['title'] is not None:
            print("You already have a borrowed book. Please return it before borrowing another.")
            return False
            
        # Check if book exists and is available
        if book_id not in Book.books:
            print("Book not found.")
            return False
            
        if not Book.books[book_id]['available']:
            print("This book is not available for borrowing.")
            return False
            
        # Borrow the book
        book_title = Book.books[book_id]['title']
        Member.members[member_key]['borrowed_book']['title'] = book_title
        Member.members[member_key]['borrowed_book']['return_date'] = return_date
        Member.members[member_key]['borrowed_book']['book_id'] = book_id
        Book.books[book_id]['available'] = False
        
        print(f"You have successfully borrowed '{book_title}'!")
        print(f"Please return it by {FineSystem.format_date(return_date)}.")
        return True
        
    def return_book(self):
        # Find the member
        member_key = None
        for key, member in Member.members.items():
            if member['id_num'] == self.id_num:
                member_key = key
                break
                
        if member_key is None:
            print("Member not found.")
            return False
            
        # Check if member has a borrowed book
        book_title = Member.members[member_key]['borrowed_book']['title']
        if book_title is None:
            print("You don't have any books to return.")
            return False
            
        # Get book details
        book_id = Member.members[member_key]['borrowed_book']['book_id']
        return_date = Member.members[member_key]['borrowed_book']['return_date']
        
        if book_id is None or book_id not in Book.books:
            print("Error: Book not found in records.")
            return False
            
        # Calculate fine if any
        fine = FineSystem.calculate_fine(return_date)
        if fine > 0:
            print(f"Your book is late. Fine amount: ${fine}")
            Member.members[member_key]['fine_balance'] += fine
            
            # Add to fine history
            today_date = datetime.datetime.now().strftime("%y%m%d")
            Member.members[member_key]['fine_history'].append({
                'amount': fine,
                'date': today_date,
                'paid': False,
                'book': book_title
            })
            
        # Return the book
        Book.books[book_id]['available'] = True
        Member.members[member_key]['borrowed_book']['title'] = None
        Member.members[member_key]['borrowed_book']['return_date'] = None
        Member.members[member_key]['borrowed_book']['book_id'] = None
        
        print(f"You have successfully returned '{book_title}'.")
        return True
        
    def view_fine_history(self):
        for key in Member.members:
            if Member.members[key]['id_num'] == self.id_num:
                fine_history = Member.members[key]['fine_history']
                fine_balance = Member.members[key]['fine_balance']
                
                if not fine_history:
                    print("\nYou have no fine history.")
                    return
                    
                print("\n----- FINE HISTORY -----")
                for i, fine in enumerate(fine_history, 1):
                    status = "Unpaid" if not fine['paid'] else "Paid"
                    print(f"{i}. Amount: ${fine['amount']} - Date: {FineSystem.format_date(fine['date'])} - Book: {fine['book']} - Status: {status}")
                    
                print(f"\nTotal outstanding balance: ${fine_balance}")
                return
                
        print("Member not found.")
        
    def pay_fine(self, amount):
        for key in Member.members:
            if Member.members[key]['id_num'] == self.id_num:
                fine_balance = Member.members[key]['fine_balance']
                
                if fine_balance == 0:
                    print("You don't have any outstanding fines.")
                    return False
                    
                if amount > fine_balance:
                    print(f"Payment amount (${amount}) exceeds your fine balance (${fine_balance}).")
                    return False
                    
                # Update fine balance
                Member.members[key]['fine_balance'] -= amount
                
                # Mark fines as paid in history (oldest first)
                remaining_payment = amount
                for fine in Member.members[key]['fine_history']:
                    if not fine['paid'] and remaining_payment > 0:
                        if remaining_payment >= fine['amount']:
                            fine['paid'] = True
                            remaining_payment -= fine['amount']
                        else:
                            # This would require splitting the fine record
                            # For simplicity, we'll wait until full payment
                            pass
                            
                print(f"Payment of ${amount} successful.")
                print(f"Remaining fine balance: ${Member.members[key]['fine_balance']}")
                return True
                
        print("Member not found.")
        return False

class LibrarianFunctions:
    @staticmethod
    def add_new_book():
        print("\n----- ADD NEW BOOK -----")
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")
        
        if not title or not author or not isbn:
            print("All fields are required.")
            return
            
        Book.add_book(title, author, isbn)
    
    @staticmethod
    def view_all_books():
        print("\n----- ALL BOOKS -----")
        if not Book.books:
            print("No books in the library.")
            return
            
        for key, book in Book.books.items():
            status = "Available" if book['available'] else "Not Available"
            print(f"[ID: {key}] {book['title']} by {book['author']} - {status}")
    
    @staticmethod
    def view_all_members():
        Member.show_all_members()
        
    @staticmethod
    def search_book():
        print("\n----- SEARCH BOOK -----")
        search_term = input("Enter search term: ").lower()
        
        found = False
        for key, book in Book.books.items():
            if (search_term in book['title'].lower() or 
                search_term in book['author'].lower() or 
                search_term in book['isbn']):
                
                status = "Available" if book['available'] else "Not Available"
                print(f"[ID: {key}] {book['title']} by {book['author']} ({status})")
                found = True
                
        if not found:
            print("No matching books found.")
            
    @staticmethod
    def view_member_details():
        member_id = input("Enter member ID number: ")
        
        found = False
        for key, member in Member.members.items():
            if member['id_num'] == member_id:
                found = True
                
                # Show member details
                book_status = member['borrowed_book']['title'] or "No borrowed books"
                return_date = member['borrowed_book']['return_date']
                formatted_date = FineSystem.format_date(return_date) if return_date else "N/A"
                
                print(f"""
                ----- MEMBER DETAILS -----
                Name: {member['name']}
                ID Number: {member['id_num']}
                Contact Number: {member['contact_num']}
                Borrowed Book: {book_status}
                Return Date: {formatted_date}
                Outstanding Fine: ${member['fine_balance']}
                ----------------------------
                """)
                
                # Show fine history
                if member['fine_history']:
                    print("Fine History:")
                    for i, fine in enumerate(member['fine_history'], 1):
                        status = "Unpaid" if not fine['paid'] else "Paid"
                        print(f"{i}. Amount: ${fine['amount']} - Date: {FineSystem.format_date(fine['date'])} - Book: {fine['book']} - Status: {status}")
                break
                
        if not found:
            print("Member not found.")
            
    @staticmethod
    def manage_fines():
        print("\n----- FINE MANAGEMENT -----")
        member_id = input("Enter member ID number: ")
        
        found = False
        for key, member in Member.members.items():
            if member['id_num'] == member_id:
                found = True
                
                if member['fine_balance'] == 0:
                    print(f"Member {member['name']} has no outstanding fines.")
                    return
                    
                print(f"Member: {member['name']}")
                print(f"Current Fine Balance: ${member['fine_balance']}")
                
                # Show fine details
                if member['fine_history']:
                    print("\nFine Details:")
                    for i, fine in enumerate(member['fine_history'], 1):
                        if not fine['paid']:
                            print(f"{i}. Amount: ${fine['amount']} - Date: {FineSystem.format_date(fine['date'])} - Book: {fine['book']}")
                
                # Option to adjust fine
                action = input("\nDo you want to [P]ay, [W]aive, or [C]ancel? ").upper()
                
                if action == 'P':
                    amount = float(input("Enter payment amount: $"))
                    if amount <= 0:
                        print("Invalid amount.")
                        return
                        
                    if amount > member['fine_balance']:
                        print(f"Amount exceeds fine balance (${member['fine_balance']}).")
                        continue_anyway = input("Process anyway? [Y/N]: ").upper()
                        if continue_anyway != 'Y':
                            return
                        amount = member['fine_balance']
                        
                    # Process payment
                    remaining = amount
                    for fine in member['fine_history']:
                        if not fine['paid'] and remaining > 0:
                            if remaining >= fine['amount']:
                                fine['paid'] = True
                                remaining -= fine['amount']
                            else:
                                # For simplicity, wait until full payment
                                pass
                                
                    member['fine_balance'] -= amount
                    print(f"Payment of ${amount} processed successfully.")
                    print(f"Remaining balance: ${member['fine_balance']}")
                    
                elif action == 'W':
                    amount = float(input("Enter amount to waive: $"))
                    if amount <= 0:
                        print("Invalid amount.")
                        return
                        
                    if amount > member['fine_balance']:
                        amount = member['fine_balance']
                        
                    reason = input("Enter reason for waiving fine: ")
                    
                    # Process waiver
                    remaining = amount
                    for fine in member['fine_history']:
                        if not fine['paid'] and remaining > 0:
                            if remaining >= fine['amount']:
                                fine['paid'] = True
                                fine['waived'] = True
                                fine['waive_reason'] = reason
                                remaining -= fine['amount']
                            else:
                                # For simplicity, wait until full waiver
                                pass
                                
                    member['fine_balance'] -= amount
                    print(f"Fine of ${amount} waived successfully.")
                    print(f"Remaining balance: ${member['fine_balance']}")
                    
                elif action == 'C':
                    print("Operation cancelled.")
                    
                else:
                    print("Invalid selection.")
                
                break
                
        if not found:
            print("Member not found.")
            
    @staticmethod
    def view_overdue_books():
        print("\n----- OVERDUE BOOKS -----")
        today = datetime.datetime.now()
        
        found = False
        for key, member in Member.members.items():
            if member['borrowed_book']['title'] and member['borrowed_book']['return_date']:
                return_date = member['borrowed_book']['return_date']
                fine = FineSystem.calculate_fine(return_date)
                
                if fine > 0:  # Book is overdue
                    found = True
                    book_title = member['borrowed_book']['title']
                    days_overdue = fine // FineSystem.FINE_RATE  # Calculate days from fine amount
                    
                    print(f"Member: {member['name']} (ID: {member['id_num']})")
                    print(f"Book: {book_title}")
                    print(f"Due Date: {FineSystem.format_date(return_date)}")
                    print(f"Days Overdue: {days_overdue}")
                    print(f"Fine Accrued: ${fine}")
                    print("------------------------")
                    
        if not found:
            print("No overdue books found.")

class MainMenu:
    current_name = ''
    current_id_num = ''
    current_contact_num = ''
    
    def start(self):
        print('''
        ========== LIBRARY MANAGEMENT SYSTEM ==========
        [1] Student
        [2] Librarian
        [3] Exit
        ==============================================
        ''')
        while True:
            try:
                selection = input('[HOME PAGE]---> ')
                if selection == '1':
                    self.member_login()
                    return
                elif selection == '2':
                    self.librarian_login()
                    return
                elif selection == '3':
                    print('Exiting Program. Goodbye!')
                    break
                else: 
                    print("Invalid selection. Please try again.")
            except Exception as e:
                print(f"Error: {e}")
                
    def member_login(self):
        print('''
        ========== MEMBER LOGIN ==========
        [1] Login
        [2] Register
        [3] Return to Main Menu
        ================================
        ''')
        while True:
            try:
                selection = input('[LOGIN]---> ')
                if selection == '1':
                    member_id = input('[ID Number (0 to go back)]--> ')
                    if member_id == '0':
                        self.member_login()
                        return
                        
                    # Search for member by ID
                    found = False
                    for key, member in Member.members.items():
                        if member['id_num'] == member_id:
                            found = True
                            print(f"\nWelcome, {member['name']}!")
                            
                            # Check for fines
                            if member['fine_balance'] > 0:
                                print(f"NOTE: You have an outstanding fine of ${member['fine_balance']}.")
                                
                            MainMenu.current_name = member['name']
                            MainMenu.current_id_num = member['id_num']
                            MainMenu.current_contact_num = member['contact_num']
                            self.member_menu()
                            return
                            
                    if not found:
                        print('Member not found. Please check your ID or register.')
                        
                elif selection == '2':
                    self.member_registration()
                    return
                elif selection == '3':
                    self.start()
                    return
                else:
                    print("Invalid selection. Please try again.")
            except Exception as e:
                print(f'Error: {e}')
        
    def member_registration(self):
        print("\n----- MEMBER REGISTRATION -----")
        name = input('Name: ')
        
        # ID validation
        while True:
            id_num = input("Enter a 9-digit ID: ").strip()
            
            if not id_num.isdigit() or len(id_num) != 9:
                print("Invalid ID. It must be exactly 9 digits.")
                continue
            
            if any(member['id_num'] == id_num for member in Member.members.values()):
                print("ID Number already taken. Try again.")
                continue
            
            break
            
        # Contact number validation
        while True:
            contact_num = input("Contact Number (11 digits starting with 09): ").strip()
            if contact_num.isdigit() and len(contact_num) == 11 and contact_num[:2] == "09":
                break
            else: 
                print("Invalid contact number. Must be 11 digits starting with 09.")
                
        # Confirmation
        while True:
            decision = input('Do you wish to register? [Y/N]: ')
            if decision.lower() == 'y':
                register = Member(name, id_num, contact_num)
                register.add_member()
                print(f"\nWelcome, {name}! You are successfully registered.")
                self.member_login()
                break
            elif decision.lower() == 'n':
                print('Registration cancelled. Returning to login page...')
                self.member_login()
                break
            else:
                print("Please enter Y or N.")
                
    def member_menu(self):
        current_member = CurrentMemberDetails(MainMenu.current_name, MainMenu.current_id_num, MainMenu.current_contact_num)
        
        while True:
            print("""
            ========== MEMBER MENU ==========
            [1] Available Books
            [2] Borrow A Book
            [3] Return A Book
            [4] View My Borrowed Books
            [5] Account Details
            [6] View Fine History
            [7] Pay Fine
            [8] Return to Login
            =================================
            """)
            
            try:
                selection = input('---> ')
                
                if selection == '1':
                    print("\n----- AVAILABLE BOOKS -----")
                    Book.show_available_books()
                
                elif selection == '2':
                    print("\n----- BORROW A BOOK -----")
                    
                    # Check if member has outstanding fines
                    has_fine = False
                    for key, member in Member.members.items():
                        if member['id_num'] == MainMenu.current_id_num and member['fine_balance'] > 0:
                            print(f"You have an outstanding fine of ${member['fine_balance']}.")
                            print("Please pay your fine before borrowing another book.")
                            has_fine = True
                            break
                            
                    if has_fine:
                        continue
                        
                    print('NOTE: A member can only borrow one book at a time.')
                    
                    if Book.show_available_books():
                        try:
                            book_id = int(input('\nEnter the ID of the book you want to borrow (0 to cancel): '))
                            if book_id == 0:
                                print("Borrowing cancelled.")
                                continue
                                
                            # Validate and parse return date
                            while True:
                                return_date = input("Enter return date (YYMMDD): ")
                                if not return_date.isdigit() or len(return_date) != 6:
                                    print("Invalid date format. Please use YYMMDD format.")
                                    continue
                                    
                                try:
                                    year = int("20" + return_date[:2])
                                    month = int(return_date[2:4])
                                    day = int(return_date[4:6])
                                    date_obj = datetime.datetime(year, month, day)
                                    
                                    # Check if date is in the future
                                    if date_obj <= datetime.datetime.now():
                                        print("Return date must be in the future.")
                                        continue
                                        
                                    break
                                except ValueError:
                                    print("Invalid date. Please enter a valid date.")
                                
                            current_member.borrow_book(book_id, return_date)
                            
                        except ValueError:
                            print('Invalid input. Please enter a valid book ID.')
                    
                elif selection == '3':
                    print("\n----- RETURN A BOOK -----")
                    current_member.return_book()
                
                elif selection == '4':
                    current_member.borrowed_books()
                
                elif selection == '5':
                    current_member.account_details()
                    
                elif selection == '6':
                    current_member.view_fine_history()
                    
                elif selection == '7':
                    print("\n----- PAY FINE -----")
                    
                    # Check if member has any fines
                    has_fine = False
                    fine_amount = 0
                    for key, member in Member.members.items():
                        if member['id_num'] == MainMenu.current_id_num:
                            fine_amount = member['fine_balance']
                            if fine_amount > 0:
                                has_fine = True
                            break
                            
                    if not has_fine:
                        print("You don't have any outstanding fines.")
                        continue
                        
                    print(f"Your current fine balance is ${fine_amount}")
                    
                    try:
                        payment = float(input("Enter payment amount: $"))
                        if payment <= 0:
                            print("Invalid amount. Payment must be greater than zero.")
                            continue
                            
                        current_member.pay_fine(payment)
                        
                    except ValueError:
                        print("Invalid input. Please enter a valid amount.")
                
                elif selection == '8':
                    print("Returning to login page...")
                    self.member_login()
                    return
                
                else:
                    print("Invalid selection. Please try again.")
                    
            except Exception as e:
                print(f"Error: {e}")

    def librarian_login(self):
        print('''
        ========== LIBRARIAN LOGIN ==========
        Username: admin
        Password: admin123
        ===================================
        ''')
        
        username = input("Username: ")
        password = input("Password: ")
        
        if username == "admin" and password == "admin123":
            print("\nWelcome, Librarian!")
            self.librarian_menu()
        else:
            print("Invalid credentials.")
            self.start()

    def librarian_menu(self):
        while True:
            print("""
            ========== LIBRARIAN MENU ==========
            [1] Add New Book
            [2] View All Books
            [3] View Available Books
            [4] View All Members
            [5] Search Book
            [6] View Member Details
            [7] View Overdue Books
            [8] Manage Fines
            [9] Return to Main Menu
            ====================================
            """)
            
            try:
                selection = input('---> ')
                
                if selection == '1':
                    LibrarianFunctions.add_new_book()
                elif selection == '2':
                    LibrarianFunctions.view_all_books()
                elif selection == '3':
                    print("\n----- AVAILABLE BOOKS -----")
                    Book.show_available_books()
                elif selection == '4':
                    LibrarianFunctions.view_all_members()
                elif selection == '5':
                    LibrarianFunctions.search_book()
                elif selection == '6':
                    LibrarianFunctions.view_member_details()
                elif selection == '7':
                    LibrarianFunctions.view_overdue_books()
                elif selection == '8':
                    LibrarianFunctions.manage_fines()
                elif selection == '9':
                    print("Returning to main menu...")
                    self.start()
                    return
                else:
                    print("Invalid selection. Please try again.")
                    
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    menu = MainMenu()
    menu.start()
