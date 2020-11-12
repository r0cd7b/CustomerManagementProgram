from customer import *
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox


class Management(CustomerManagement):  # 관리자 클래스.
    # tkinter 위젯에 담긴 정보를 관리한다.
    # 고객 객체 관리자를 상속 받아 해당하는 주요 함수를 오버라이딩한다.
    def __init__(self):
        super().__init__()
        self.__add_level = None  # 고객 추가 창.
        self.__modify_level = None  # 고객 수정 창.
        self.__name_entry = None  # 고객 이름 Entry.
        self.__phone_entry = None  # 고객 전화번호 Entry.
        self.__coupon_entry = None  # 고객 쿠폰 수 Entry.
        self.__visit_entry = None  # 고객 방문 횟수 Entry.
        self.__sorting_status = None  # 정렬 상태를 저장하는 변수.
        self.__sorting_reverse = False  # 정렬의 오름차 혹은 내림차순을 토글하기 위한 변수.
        self.__customer_modify = None  # 수정할 고객 정보를 저장하는 변수.

        self.__tk = Tk()
        self.__tk.title("고객 관리 프로그램")
        w, h = 500, 600
        self.__tk.geometry(f"{w}x{h}+{int((self.__tk.winfo_screenwidth() - w) * 0.5)}"  # 현재 모니터의 해상도에 맞추어 창을 중앙에 위치시킨다.
                           f"+{int((self.__tk.winfo_screenheight() - h) * 0.5)}")

        menu = Menu(self.__tk)  # 메뉴 위젯 선언.
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Open...", command=self.load)  # 파일 열기 메뉴.
        file_menu.add_command(label="Save As...", command=self.save)  # 파일 저장 메뉴.
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.__tk.quit)
        menu.add_cascade(label="File", menu=file_menu)
        self.__tk.config(menu=menu)

        frame = Frame(self.__tk)  # 이후 위젯들은 프레임에 넣는다.
        frame.pack(anchor=CENTER, expand=True)

        self.__search_entry = Entry(frame, width=45, relief=SOLID)  # 검색 Entry.
        self.__search_entry.grid(row=0, columnspan=2, sticky=W, ipady=5)
        Button(frame, text="검색", width=12, pady=4, relief=GROOVE, overrelief=SOLID,  # 검색 버튼.
               command=self.search_tree_view).grid(row=0, columnspan=2, sticky=E)

        self.__view = ttk.Treeview(frame, column=["", "", "", ""], height=20)  # 고객 정보를 표현할 표 위젯. ttk 모듈을 활용했다.
        self.__view.column("#0", width=0, minwidth=0, stretch=False)
        self.__view.column("#1", anchor=CENTER, width=100, stretch=False)
        self.__view.column("#2", anchor=CENTER, width=100, stretch=False)
        self.__view.column("#3", anchor=CENTER, width=100, stretch=False)
        self.__view.column("#4", anchor=CENTER, width=100, stretch=False)
        self.__view.heading("#0")
        self.__view.heading("#1", text="이름", command=lambda: self.sort(0))  # 이름 속성. 람다 함수를 활용해 매개 인자를 전달한다.
        self.__view.heading("#2", text="전화번호", command=lambda: self.sort(1))  # 전화번호 속성.
        self.__view.heading("#3", text="쿠폰 수", command=lambda: self.sort(2))  # 쿠폰 수 속성.
        self.__view.heading("#4", text="방문 횟수", command=lambda: self.sort(3))  # 방문 횟수 속성.
        self.__view.grid(row=1, column=0, pady=9)

        scrollbar = Scrollbar(frame, width=20, command=self.__view.yview)  # 표에 스크롤바를 적용한다.
        scrollbar.grid(row=1, column=1, ipady=180)
        self.__view["yscrollcommand"] = scrollbar.set

        Button(frame, text="추가", width=18, pady=5, relief=GROOVE, overrelief=SOLID,  # 고객 추가 버튼.
               command=self.add).grid(row=2, columnspan=2, sticky=W)
        Button(frame, text="수정", width=18, pady=5, relief=GROOVE, overrelief=SOLID,  # 고객 수정 버튼.
               command=self.modify).grid(row=2, columnspan=2)
        Button(frame, text="삭제", width=18, pady=5, relief=GROOVE, overrelief=SOLID,  # 고객 삭제 버튼.
               command=self.delete).grid(row=2, columnspan=2, sticky=E)

        self.__tk.mainloop()

    def load(self):  # 파일 열기 함수. 상위 클래스의 load를 오버라이딩한다.
        file = filedialog.askopenfile(filetypes=(("텍스트 파일(*.txt)", "*.txt"), ("모든 파일(*.*)", "*.*")))
        if file is None:
            return
        super().load(file)
        for customer in super().customer_list:
            self.__view.insert('', END, values=customer.variables, iid=customer.phone)

    def save(self):  # 파일 저장 함수. 상위 클래스의 save를 오버라이딩한다.
        file = filedialog.asksaveasfile(filetypes=(("텍스트 파일(*.txt)", "*.txt"), ("모든 파일(*.*)", "*.*")))
        if file is None:
            return
        super().save(file)

    def search_tree_view(self):  # 표에서 항목을 검색하는 함수. 내부에서 상위 클래스의 search 함수를 이용한다.
        query = self.__search_entry.get()  # 검색 Entry의 내용을 가져온다.
        if query == "":  # 검색 내용이 없을 경우 검색 중단.
            messagebox.showwarning("검색어 경고", f"검색어를 입력해주십시오.")
            return
        for item in self.__view.selection():  # 표에서 이미 선택되어 있던 항목을 선택 취소한다.
            self.__view.selection_remove(item)
        found_customer = super().search(query)  # 상위 클래스의 search를 수행하여 해당 고객 객체를 찾고 반환한다.
        number = len(found_customer)  # 검색 결과의 개수를 저장.
        if number:  # 검색 결과의 개수가 하나 이상 있을 경우 수행.
            self.__view.selection_add([customer.phone for customer in found_customer])  # 표에서 검색된 항목을 자동 선택한다.
            messagebox.showinfo("검색 성공", f"{number}개의 항목을 찾았습니다.")
        else:
            messagebox.showinfo("검색 실패", f"해당하는 항목을 찾을 수 없습니다.")

    def sort(self, key):  # 정렬 함수.
        if self.__sorting_status == key:  # 현재 요구하는 정렬 속성이 현재 정렬 속성과 같을 경우.
            self.__sorting_reverse = not self.__sorting_reverse  # 오름차순 및 내림차순을 결정하는 변수를 토글한다.
        else:
            self.__sorting_status = key  # 요구하는 정렬 속성을 현재 속성으로 저장한다.

        if self.__sorting_status == 0:  # 0은 이름으로 정렬.
            # 람다 함수를 이용해 객체 속에서 정렬할 기준 변수를 선택한다.
            super().customer_list.sort(reverse=self.__sorting_reverse, key=lambda c: c.name)
        elif self.__sorting_status == 1:  # 1은 전화번호로 정렬.
            super().customer_list.sort(reverse=self.__sorting_reverse, key=lambda c: c.phone)
        elif self.__sorting_status == 2:  # 2는 전화번호로 정렬.
            super().customer_list.sort(reverse=self.__sorting_reverse, key=lambda c: c.coupon)
        else:  # 3은 전화번호로 정렬.
            super().customer_list.sort(reverse=self.__sorting_reverse, key=lambda c: c.visit)

        for customer in super().customer_list:  # 정렬된 순서로 항목을 표시하기 위해 표의 모든 항목을 지우고 다시 리스트에서 불러온다.
            self.__view.delete(customer.phone)
            self.__view.insert('', END, values=customer.variables, iid=customer.phone)

    def add(self):  # 고객 추가 함수. 상위 클래스의 add를 오버라이딩한다.
        self.__add_level = Toplevel(self.__tk)  # 새로운 창을 띄운다.
        self.__add_level.title("고객 추가")
        w, h = 220, 110
        self.__add_level.geometry(f"{w}x{h}+{int((self.__tk.winfo_screenwidth() - w) * 0.5)}"
                                  f"+{int((self.__tk.winfo_screenheight() - h) * 0.5)}")
        self.__add_level.focus()  # 띄워진 창에 focus를 맞춘다.

        frame = Frame(self.__add_level)
        frame.pack(anchor=CENTER, expand=True)

        Label(frame, text="이름", anchor=E, width=7).grid(row=0, column=0, padx=10)
        self.__name_entry = Entry(frame, width=15, relief=SOLID)
        self.__name_entry.grid(row=0, column=1, ipady=1)

        Label(frame, text="전화번호", anchor=E, width=7).grid(row=1, column=0, pady=10)
        self.__phone_entry = Entry(frame, width=15, relief=SOLID)
        self.__phone_entry.grid(row=1, column=1, ipady=1, pady=10)

        Button(frame, text="확인", width=11, relief=GROOVE, overrelief=SOLID,
               command=self.confirm_add).grid(row=2, columnspan=2, sticky=W)  # '확인'버튼을 누르면 고객 추가를 확인하는 함수 수행.
        Button(frame, text="취소", width=11, relief=GROOVE, overrelief=SOLID,
               command=self.__add_level.withdraw).grid(row=2, columnspan=2, sticky=E)  # '취소'버튼을 누르면 창을 닫는다.

    def confirm_add(self):  # 고객 추가 확인 함수.
        name = self.__name_entry.get()
        phone = self.__phone_entry.get()
        if name == "" or phone == "":
            messagebox.showwarning("추가 실패", "추가할 고객 정보를 입력하세요.")
            self.__add_level.focus()
            return
        customer = Customer(name, phone)
        if super().add(customer):  # 객체를 전달해 상위 클래스의 add 함수로 고객 리스트에 추가한다.
            messagebox.showinfo("추가 완료", "해당 고객이 추가되었습니다.")
            self.__add_level.focus()
            self.__view.insert('', END, values=customer, iid=customer.phone)  # 표에도 항목을 추가한다.
            self.__view.focus(customer.phone)
            self.__view.selection_set(customer.phone)  # 추가된 항목을 선택한다.
        else:
            messagebox.showwarning("추가 실패", "이미 존재하는 고객입니다.")
            self.__add_level.focus()

    def modify(self):  # 고객 수정 함수. 상위 클래스의 modify 함수를 오버라이딩한다.
        customers = self.__view.selection()  # 표에서 선택된 항목을 가져온다.
        if not customers:  # 표에서 선택한 항목이 없을 경우 수행.
            messagebox.showwarning("수정 경고", "수정할 고객을 선택하세요.")
            return
        if len(customers) > 1:  # 표에서 선택한 항목이 복수일 경우 수행.
            messagebox.showwarning("수정 경고", "하나의 고객만 선택하세요.")
            return
        customer = super().search_phone(customers[0])  # 상위 클래스의 search_phone 함수를 이용하여 전화번호로 고객 객체를 찾는다.
        self.__customer_modify = customer.phone  # 찾은 전화번호를 다른 함수에서 사용하기 위해 저장한다.

        self.__modify_level = Toplevel(self.__tk)  # 고객 수정 창을 띄운다.
        self.__modify_level.title("고객 수정")
        w, h = 220, 170
        self.__modify_level.geometry(f"{w}x{h}+{int((self.__tk.winfo_screenwidth() - w) * 0.5)}"
                                     f"+{int((self.__tk.winfo_screenheight() - h) * 0.5)}")

        frame = Frame(self.__modify_level)
        frame.pack(anchor=CENTER, expand=True)

        Label(frame, text="이름", anchor=E, width=7).grid(row=0, column=0, padx=10)
        self.__name_entry = Entry(frame, width=15, relief=SOLID)
        self.__name_entry.insert(END, customer.name)
        self.__name_entry.grid(row=0, column=1, ipady=1)

        Label(frame, text="전화번호", anchor=E, width=7).grid(row=1, column=0, pady=10)
        self.__phone_entry = Entry(frame, width=15, relief=SOLID)
        self.__phone_entry.insert(END, customer.phone)
        self.__phone_entry.grid(row=1, column=1, ipady=1)

        Label(frame, text="쿠폰 수", anchor=E, width=7).grid(row=2, column=0)
        self.__coupon_entry = Entry(frame, width=15, relief=SOLID)
        self.__coupon_entry.insert(END, customer.coupon)
        self.__coupon_entry.grid(row=2, column=1, ipady=1)

        Label(frame, text="방문 횟수", anchor=E, width=7).grid(row=3, column=0, pady=10)
        self.__visit_entry = Entry(frame, width=15, relief=SOLID)
        self.__visit_entry.insert(END, customer.visit)
        self.__visit_entry.grid(row=3, column=1)

        Button(frame, text="확인", width=11, relief=GROOVE, overrelief=SOLID,
               command=self.confirm_modify).grid(row=4, columnspan=2, sticky=W)  # 확인 버튼을 누르면 confirm 함수 수행.
        Button(frame, text="취소", width=11, relief=GROOVE, overrelief=SOLID,
               command=self.__modify_level.withdraw).grid(row=4, columnspan=2, sticky=E)  # 취소 버튼을 누르면 창을 닫는다.

    def confirm_modify(self):  # 수정에 대한 confirm 함수.
        try:
            name = self.__name_entry.get()
            phone = self.__phone_entry.get()
            coupon = int(self.__coupon_entry.get())
            visit = int(self.__visit_entry.get())
            # 상위 클래스의 modify 함수를 호출하고 수정한 뒤, 정상적으로 수행되었지 검사한다.
            if super().modify(self.__customer_modify, name, phone, coupon, visit):
                self.__view.item(self.__customer_modify, value=(name, phone, coupon, visit))  # 표에서도 항목을 수정한다.
                messagebox.showinfo("수정 성공", "해당 고객이 수정되었습니다.")
                self.__modify_level.focus()
            else:
                messagebox.showerror("수정 실패", "이미 등록된 고객입니다.")
                self.__modify_level.focus()
        except Exception as e:
            messagebox.showerror("수정 실패", e)
            self.__modify_level.focus()

    def delete(self):  # 고객 삭제 함수. 상위 클래스의 delete 함수를 오버라이딩한다.
        customers = self.__view.selection()  # 복수로 선택된 표의 항목을 가져온다.
        if not customers:  # 선택된 항목이 없을 경우 수행.
            messagebox.showwarning("삭제 경고", "삭제할 고객을 선택하세요.")
            return
        if not messagebox.askyesno("삭제 경고", "정말로 삭제하시겠습니까?"):
            return
        for customer_phone in customers:  # 선택된 복수 고객 객체를 순환 반복한다.
            customer = super().search_phone(customer_phone)  # 상위 클래스의 search_phone 함수를 이용해 선택된 고객을 검색하고 객체를 가져온다.
            super().delete(customer)  # 상위 클래스의 delete 함수를 수행하여 고객 객체 리스트에서 제거한다.
            self.__view.delete(customer_phone)  # 표에서도 해당 항목을 제거한다.
