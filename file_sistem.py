class FileSistemItem:
    def __init__(self, name, created_at, modified_at, owner):
        self.name = name
        self.crarted_at = created_at
        self.modified_at = modified_at
        self.owner = owner

    def get_size(self):
        return 'Это абстрактный метод'
    
    def search(self, pattern):
        return 'Это абстрактный метод'
    
    def get_path(self):
        return 'Это абстрактный метод'
    
class File(FileSistemItem):
    def __init__(self, content, extension, size):
        self.content = content
        self.extension = extension
        self.size = size

    def read(self):
        return
    
    def wright(self, content):
        return
    
    def append(self, content):
        return
    
    def __len__():
        return
    
class Directory(FileSistemItem):
    def __init__(self):
        self.children = []

    def add(self, item):
        return
    
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