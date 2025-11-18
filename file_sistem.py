from datetime import datetime


class FileSistemItem:
    def __init__(self, name, owner, created_at=None, modified_at=None):
        self.name = name
        self.created_at = created_at or datetime.now()
        self.modified_at = modified_at or datetime.now()
        self.owner = owner
        self.parent = None  # ИСПРАВЛЕНО

    def get_size(self):
        raise NotImplementedError()

    def search(self, pattern):
        raise NotImplementedError()

    def get_path(self):
        if self.parent is None:
            return f"/{self.name}"
        return f"{self.parent.get_path()}/{self.name}"

    def _update_modified(self):
        self.modified_at = datetime.now()


class File(FileSistemItem):
    def __init__(self, name, owner, content='', extension='txt'):
        super().__init__(name, owner)
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

    def append(self, user, content):
        if user not in self.allowed_users:
            raise PermissionError("Доступ запрещен")

        self.content += content
        self.size = len(self.content.encode("utf-8"))
        self._update_modified()

    def get_size(self):
        return self.size  # ИСПРАВЛЕНО

    def search(self, pattern):
        import fnmatch
        return [self] if fnmatch.fnmatch(self.name, pattern) else []

    def __len__(self):
        return self.size  # ИСПРАВЛЕНО


class Directory(FileSistemItem):
    def __init__(self, name, owner):
        super().__init__(name, owner)  # ИСПРАВЛЕНО
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
        for i, child in enumerate(self.children):
            if child.name == name:
                del self.children[i]
                self._update_modified()
                return
        raise FileNotFoundError(f"Нет элемента: {name}")

    def get_size(self):
        return sum(child.get_size() for child in self.children)

    def search(self, pattern):
        result = []
        for child in self.children:
            result.extend(child.search(pattern))
        return result

    def list_all(self, indent=0):
        print("  " * indent + f"[DIR] {self.name}/")
        for child in self.children:
            if isinstance(child, Directory):
                child.list_all(indent + 1)
            else:
                print("  " * (indent + 1) +
                      f"[FILE] {child.name}.{child.extension} ({child.get_size()} bytes)")

    def __getitem__(self, name):
        for child in self.children:
            if child.name == name:
                return child
        raise KeyError(name)

    def __contains__(self, name):
        return any(child.name == name for child in self.children)

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)


# ТЕСТ
root = Directory("root", owner="admin")
docs = Directory("docs", owner="admin")
file1 = File("info", "admin", "Hello world")
file2 = File("notes", "admin", "Some text", "md")

root.add(docs)
docs.add(file1)
docs.add(file2)

root.list_all()
print(file1.read("admin"))
print("Размер docs:", docs.get_size())
print("Путь к file2:", file2.get_path())
