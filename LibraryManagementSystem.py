class Book:
    def __init__(self, title, author, isbn, available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available
        self.books = {
            1 : {
                'title':'The Hobbit',
                'author':'J.R.R. Tolkien',
                'isbn':'9780345339683',
                'available':False
            },
            2 : {
                'title':'1984',
                'author':'George Orwell',
                'isbn':'9780451524935',
                'available':False
            }
        }
        
    def book_record(self):
        return {
            'title':self.title,
            'author':self.author,
            'isbn':self.isbn,
            'available':self.available
        }
        
    def show_available_books(self):
        for book in self.books:
            if self.books[book]['available']:
                print(self.books[book]['title'])
            else: continue
        
class Member:
    members = {
        1:{
            'name':'John James',
            'id_num':'202356789',
            'contact_num':'09123456789',
            'borrowed_book':{
                'title':'The Hobbit',
                'return_date':'111314'
            }
         },
        2:{
            'name':'James John',
            'id_num':'202309876',
            'contact_num':'09876543219',
            'borrowed_book':{
                'title':'1984',
                'return_date':'111414'
            }
        }
    }
    
    def __init__(self, name, id_num, contact_num):
        self.name = name
        self.id_num = id_num
        self.contact_num = contact_num
        
    def add_member(self):
        Member.members.update(
            {
                len(self.members)+1:{
                    'name':self.name,
                    'id_num':self.id_num,
                    'contact_num':self.contact_num,
                    'borrowed_book':{
                        'title':None,
                        'return_date':None
                    }
                }
            }
            )
            
    def show_all_members(self):
        print(self.members)

class CurrentMemberDetails(Member):
    def account_details(self):
        for key in Member.members:
            if Member.members[key]['id_num'] == self.id_num:
                print(f"""
                Name: {Member.members[key]['name']}
                ID Number: {Member.members[key]['id_num']}
                Contact Number: {Member.members[key]['contact_num']}
                Borrowed Book: {Member.members[key]['borrowed_book']['title']}
                Return Date: {Member.members[key]['borrowed_book']['return_date']}
                """)
                MainMenu.account_menu()
                
                
    def borrowed_books(self):
        for key in Member.members:
            if Member.members[key]['id_num'] == self.id_num:
                print(f"""
                Book: {Member.members[key]['borrowed_book']['title']}
                Return Date: {Member.members[key]['borrowed_book']['return_date']}
                """)
                MainMenu.account_menu()
                
    # def borrow_book(self):
    #     for key in Member.members:
    #         # check the eligibility for borrowing a book
            

class MainMenu:
    current_name = ''
    current_id_num = ''
    current_contact_num = ''
    
    def start(self):
        print('''
        ---------- HOME PAGE ----------
        [1] Student
        [2] Librarian
        [3] Exit
        -------------------------------
        ''')
        while True:
            try:
                selection = int(input('[HOME PAGE]---> '))
                if selection == 1:
                    self.member_login()
                    return
                elif selection == 2:
                    self.librarian_login()
                    return
                elif selection == 3:
                    print('Exiting Program.')
                    break
                else: continue
            except Exception as e:
                continue
                
    def member_login(self):
        member_instance = Member('temp','0000','0000')
        print('''
        ---------- LOGIN ----------
        [1] Login
        [2] Register
        [3] Return
        ---------------------------
        ''')
        while True:
            try:
                selection = int(input('[LOGIN]---> '))
                if selection == 1:
                    while True:
                        try:
                            member_id = int(input('[ID (0 to go back)]--> '))
                            if member_id == 0:
                                self.member_login()
                                return
                            #This will track the datas
                            for member in member_instance.members.values():
                                if member['id_num'] == str(member_id):
                                    print(f"Welcome, {member['name']}!")
                                    # self.member_menu()
                                    member_instance = Member(member['name'],member['id_num'],member['contact_num'])
                                    MainMenu.current_name = member['name']
                                    MainMenu.current_id_num = member['id_num']
                                    MainMenu.current_contact_num = member['contact_num']
                                    self.member_menu()
                                    return
                                else: continue
                            print('Not Found.')
                        except Exception as e:
                            print(f'')
                elif selection == 2:
                    self.member_registration()
                    return
                elif selection == 3:
                    self.start()
                    return
            except Exception as e:
                continue
        
    def member_registration(self):
        name = str(input('Name: '))
        while True:
            try:
                id_num = input("Enter a 9-digit ID: ").strip()
        
                # Ensure it's exactly 9 digits
                if not id_num.isdigit() or len(id_num) != 9:
                    print("Invalid ID. It must be exactly 9 digits.")
                    continue
        
                # Check if ID already exists
                if any(member['id_num'] == id_num for member in Member.members.values()):
                    print("ID Number already taken. Try again.")
                    continue
        
                print("ID is available!")
                break  # Exit loop if ID is valid and unique
        
            except Exception as e:
                print(f"Error: {e}")  # Debugging message
        while True:
            try:
                contact_num = input("Contact Number: ").strip()
                if contact_num.isdigit() and len(contact_num) == 11 and contact_num[:2] == "09":
                    break
                else: continue
            except Exception as e:
                continue
        while True:
            decision = input('Do you wish to register? [Y/N]: ')
            if decision.lower() == 'y':
                register = Member(name,str(id_num),str(contact_num))
                register.add_member()
                print(f"Welcome, {name}!. You are succesfully registered. Going back to login page.")
                self.member_login()
                break
            elif decision.lower() == 'n':
                print('Returning...')
                self.member_login()
                break
            else:
                continue
                
    def member_menu(self):
        current_details = CurrentMemberDetails(MainMenu.current_name,MainMenu.current_id_num,MainMenu.current_contact_num)
        print("""
        ---------- MEMBER MENU ----------
        [1] Borrow A Book
        [2] Return A Book
        [3] Borrowed Books
        [4] Account Details
        [5] Exit
        ---------------------------------
        """)
        selection = int(input('---> '))
        if selection == 3:
            current_details.borrowed_books()
        elif selection == 4: 
            current_details.account_details()
            
    def librarian_login(self):
        print('Librarian Menu')
        
        
MainMenu().start()



# books = Book(1,2,3,True)
# books.show_available_books()      