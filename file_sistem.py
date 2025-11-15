class FileSistemItem:
    def __init__(self, name, created_at, modified_at, owner):
        self.name = name
        self.crarted_at = created_at
        self.modified_at = modified_at
        self.owner = owner

    def _get_size(self, content):
        return 'Это абстрактный метод'
    
    def _search(self, pattern):
        return 'Это абстрактный метод'
    
    def _get_path(self):
        return 'Это абстрактный метод'
    
class File(FileSistemItem):
    def __init__(self, name, extension, size=0):
        super().__init__(name, created_at=None, modified_at=None, owner=None)
        self.content = None
        self.extension = extension
        self.size = size

    def read(self):
        return self.content
    
    def wright(self, content):
        self.content = content
        return 'Файл создан'
    
    def append(self, content):
        self.content += content
        return 'Файл был успешно обновлен'
    
    def __len__(self):
        length = len(self.content) * 2
        return f'{length} байт по UTF-16'
    
class Directory(FileSistemItem):
    def __init__(self):
        self.children = {}

    def add(self, item):
        if item.name in self.children:
            raise ValueError(f"Элемент '{item.name}' уже существует в директории")
        
        self.children[item.name] = item
        print(self.children)
        return f"'{item.name}' успешно добавлен"
    
    def remove(self, name):
        return
    
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