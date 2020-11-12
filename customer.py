class Customer:  # 고객 정보 클래스.
    def __init__(self, name, phone, coupon=0, visit=0):
        self.__name = name  # 이름.
        self.__phone = phone  # 전화번호.
        self.__coupon = coupon  # 쿠폰 수.
        self.__visit = visit  # 방문 횟수.

    # 접근자와 설정자(파이썬 최신 문법 반영).
    @property
    def name(self):
        return self.__name

    @property
    def phone(self):
        return self.__phone

    @property
    def coupon(self):
        return self.__coupon

    @property
    def visit(self):
        return self.__visit

    @name.setter
    def name(self, name):
        self.__name = name

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @coupon.setter
    def coupon(self, coupon):
        self.__coupon = coupon

    @visit.setter
    def visit(self, visit):
        self.__visit = visit

    @property
    def variables(self):  # 객체의 모든 변수를 튜플로 반환하는 접근자.
        return self.__name, self.__phone, self.__coupon, self.__visit

    def __eq__(self, other):  # 비교 함수 정의. 객체를 비교할 때, 기본 키인 전화번호를 비교한다.
        return self.__phone == other.__phone

    def __str__(self):  # 문자열 반환 함수 정의. 객체를 문자열로 표현할 때, 자동으로 형식을 지정한다.
        return f"{self.__name} {self.__phone} {self.__coupon} {self.__visit}"


class CustomerManagement:  # 고객 객체를 관리할 클래스.
    def __init__(self):
        self.__customer_list = []  # 고객 객체를 리스트에 담는다.

    def __str__(self):  # 문자열을 반환해야할 때, 고객 객체를 모두 모아 문자열로 출력한다.
        string = ""
        for customer in self.__customer_list:
            string += f"{customer}\n"
        return string

    @property  # 고객 리스트 접근자.
    def customer_list(self):
        return self.__customer_list

    def save(self, file):  # 파일 저장 함수.
        with file as file:
            file.write(self.__str__())

    def load(self, file):  # 파일 불러오기 함수.
        with file:
            self.__customer_list = []
            for line in file:  # 한 줄씩 읽어 반복한다.
                item = line.split()  # 자료를 띄어쓰기로 구분.
                self.__customer_list.append(Customer(item[0], item[1], int(item[2]), int(item[3])))  # 객체로 만든 후 리스트에 저장.

    def search(self, query):  # 검색 함수.
        found_customer = []  # 검색되는 여러 객체를 반환하기 위해 리스트 선언.
        for customer in self.__customer_list:
            for variables in customer.variables:  # 튜플로 반환된 변수순으로 반복한다.
                if query == variables:  # 같은 변수를 발견할 경우 수행.
                    found_customer.append(customer)  # 고객 추가.
                    break
        return found_customer  # 리스트 반환.

    def search_phone(self, phone):  # 기본 키인 전화번호로 검색하는 함수.
        for customer in self.__customer_list:
            if customer.phone == phone:
                return customer
        return None  # 검색된 객체가 없을 경우 None 반환.

    def add(self, customer):  # 고객 객체 추가 함수.
        if self.search_phone(customer.phone):  # 기본 키인 전화번호를 중복 검사.
            return False
        self.__customer_list.append(customer)
        return True

    def modify(self, customer_phone, name, phone, coupon, visit):  # 고객 객체 수정 함수.
        if customer_phone != phone:  # 만약 해당되는 고객 정보가 없으면 수행하지 않는다.
            for customer in self.__customer_list:
                if customer.phone == phone:
                    return False
        customer = self.search_phone(customer_phone)
        customer.name = name
        customer.phone = phone
        customer.coupon = coupon
        customer.visit = visit
        return True  # 정상적으로 수정되면 True 반환.

    def delete(self, customer):  # 고객 객체 삭제 함수.
        if self.search_phone(customer.phone):  # 해당 고객이 존재할 경우 수행.
            self.__customer_list.remove(customer)
            return True
        return False
