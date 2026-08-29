import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []  # Список для хранения всех пользователей

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.session_token = None

    @staticmethod
    def hash_password(password):
        """
        Хеширование пароля с использованием SHA-256 и соли.
        """
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @staticmethod
    def check_password(stored_password, provided_password):
        """
        Проверка пароля.
        """
        if ':' not in stored_password:
            return stored_password == provided_password
        
        password_hash, salt = stored_password.split(':')
        return password_hash == hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest()

    def get_details(self):
        return f"Имя пользователя: {self.username} email: {self.email}"

class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)
        self.address = address
        self.user_type = "customer"

    def get_details(self):
        return (f"Имя пользователя: {self.username} email: {self.email}", 
                f"Адрес: {self.address}")

class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)
        self.admin_level = admin_level
        self.user_type = "admin"

    def get_details(self):
        return (f"Имя пользователя: {self.username} email: {self.email}", 
                f"Уровень доступа: {self.admin_level}")

    @staticmethod
    def list_users():
        """
        Выводит список всех пользователей.
        """
        if not User.users:
            print("Список пользователей пуст.")
            return
        
        print("\n=== Список пользователей ===")
        for i, user in enumerate(User.users, 1):
            user_type = getattr(user, 'user_type', 'user')
            print(f"{i}. {user.username} ({user_type}) - {user.email}")
        print("============================\n")

    @staticmethod
    def delete_user(username):
        """
        Удаляет пользователя по имени пользователя.
        """
        for i, user in enumerate(User.users):
            if user.username == username:
                if isinstance(user, Admin) and user.admin_level == 0:
                    print("Нельзя удалить главного администратора!")
                    return False
                User.users.pop(i)
                print(f"Пользователь '{username}' успешно удален.")
                return True
        print(f"Пользователь с именем '{username}' не найден.")
        return False

class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.current_user = None
        # Создаем главного администратора по умолчанию
        main_admin = Admin("admin", "admin@system.com", "admin123", 0)
        User.users.append(main_admin)

    def register(self, user_class, username, email, password, *args):
        """
        Регистрация нового пользователя.
        """
        # Проверка уникальности имени пользователя
        for user in User.users:
            if user.username == username:
                print(f"Ошибка: пользователь с именем '{username}' уже существует.")
                return None
        
        # Проверка уникальности email
        for user in User.users:
            if user.email == email:
                print(f"Ошибка: пользователь с email '{email}' уже зарегистрирован.")
                return None
        
        # Создание нового пользователя
        try:
            if user_class == Customer:
                new_user = Customer(username, email, password, *args)
            elif user_class == Admin:
                if len(args) > 0:
                    new_user = Admin(username, email, password, args[0])
                else:
                    new_user = Admin(username, email, password, 1)
            else:
                print("Ошибка: неизвестный тип пользователя.")
                return None
            
            User.users.append(new_user)
            print(f"Пользователь '{username}' успешно зарегистрирован.")
            return new_user
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            return None

    def login(self, username, password):
        """
        Аутентификация пользователя.
        """
        # Проверка, не авторизован ли уже пользователь
        if self.current_user:
            print(f"Пользователь '{self.current_user.username}' уже авторизован.")
            return self.current_user
        
        # Поиск пользователя
        for user in User.users:
            if user.username == username:
                if User.check_password(user.password, password):
                    self.current_user = user
                    user.session_token = uuid.uuid4().hex
                    print(f"Пользователь '{username}' успешно авторизован.")
                    return user
                else:
                    print("Ошибка: неверный пароль.")
                    return None
        
        print(f"Ошибка: пользователь с именем '{username}' не найден.")
        return None

    def logout(self):
        """
        Выход пользователя из системы.
        """
        if self.current_user:
            username = self.current_user.username
            self.current_user.session_token = None
            self.current_user = None
            print(f"Пользователь '{username}' вышел из системы.")
        else:
            print("Ни один пользователь не авторизован.")

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        if self.current_user:
            return self.current_user
        else:
            print("Пользователь не авторизован.")
            return None


if __name__ == "__main__":
    auth_service = AuthenticationService()
    
    # Регистрация клиента
    print("\n--- Регистрация клиента ---")
    customer = auth_service.register(Customer, "john_doe", "john@mail.com", "pass123", "ул. Ленина, 1")
    
    # Регистрация администратора
    print("\n--- Регистрация администратора ---")
    admin = auth_service.register(Admin, "admin2", "admin2@mail.com", "admin456", 2)
    
    # Попытка регистрации с существующим именем
    print("\n--- Попытка регистрации с существующим именем ---")
    auth_service.register(Customer, "john_doe", "john2@mail.com", "pass456", "ул. Пушкина, 2")
    
    # Авторизация
    print("\n--- Авторизация ---")
    auth_service.login("john_doe", "pass123")
    
    # Попытка повторной авторизации
    print("\n--- Попытка повторной авторизации ---")
    auth_service.login("admin", "admin123")
    
    # Получение текущего пользователя
    print("\n--- Текущий пользователь ---")
    current = auth_service.get_current_user()
    if current:
        print(current.get_details())
    
    # Просмотр списка пользователей (только для админа)
    print("\n--- Список пользователей (администратор) ---")
    auth_service.login("admin", "admin123")
    Admin.list_users()
    
    # Удаление пользователя (только для админа)
    print("\n--- Удаление пользователя ---")
    Admin.delete_user("john_doe")
    
    # Обновленный список пользователей
    Admin.list_users()
    
    # Выход из системы
    print("\n--- Выход из системы ---")
    auth_service.logout()
    auth_service.logout()  # Повторный выход
    
    # Попытка удаления главного администратора
    print("\n--- Попытка удаления главного администратора ---")
    auth_service.login("admin", "admin123")
    Admin.delete_user("admin")