from datetime import datetime

class FileSistemItem:
    def __init__(self, name, created_at, modified_at, owner):
        self.name = name
        self.crarted_at = datetime.now()
        self.modified_at = datetime.now()
        self.owner = owner
        self.pattern = None

    def get_size(self, content):
        return 'Это абстрактный метод'
    
    def search(self, pattern):
        return 'Это абстрактный метод'
    
    def get_path(self):
        if self.pattern is None:
            return f"/{self.name}"
        return f"{self.parent.get_path()}/{self.name}"
    
    def _update_modified(self):
        self.modified_at = datetime.now()
    
class File(FileSistemItem):
    def __init__(self, name, owner, content='', extension='txt'):
        super().__init__(name, created_at=None, modified_at=None, owner=None)
        self.content = content
        self.extension = extension
        self.size = len(content.encode("utf-8"))
        self.allowed_users = set([owner])

    def read(self, user):
        if user not in self.allowed_users:
            raise PermissionError("Доступ запрещен")
        return self.content
    
    def wright(self, user, content):
        if user not in self.allowed_users:
            raise PermissionError("Доступ запрещен")
        
        self.content = content
        self.size = len(content.encode("utf-8"))
        self._update_modified()
        return 'Файл создан'
    
    def append(self, user, content):
        if user not in self.allowed_users:
            raise PermissionError("Доступ запрещен")
        
        self.content += content
        self.size = len(self.content.encode("utf-8"))
        self._update_modified()
        return 'Файл был успешно обновлен'
    
    def __len__(self):
        return f'{self.size} байт по UTF-8'
    
class Directory(FileSistemItem):
    def __init__(self, name, owner):
        super().__init__(name, owner)
        self.children = []

    def add(self, item):
        current = self
        while current is not None:
            if current is item:
                raise ValueError("Нельзя добавить директорию саму в себя")
            current = current.parent

        item.parent = self
        self.children.append(item)
        self._update_modified()
    
    def remove(self, name):
        
    
    def get_size(self):
        return
    
    def search(self, pattern):
        return
    
    def list_all(self):
        return
    
    def __getitem__(self, name):
        return
    
    def __contains__(self, name):
        return
    
    def __iter__(self):
        return
    
    def __len__(self):
        return
    
file = File('first', '.py')
directory = Directory()
print(file.wright('Hello'))
print(file.read())
print(file.append(''))
print(file.read())
print(file.__len__())

print(directory.add(file))