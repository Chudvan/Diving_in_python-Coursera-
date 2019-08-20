import os
import tempfile


class File:
    def __init__(self, path):
        if os.path.isdir(path):
            raise FileNotFoundError(f'{path} is a directory.')
        self.path = path
        file_name = path.split(os.sep)[-1]
        self.name = os.path.splitext(file_name)[0]
        self.ext = os.path.splitext(file_name)[1]
        with open(self.path, 'a'):
            pass

    def write(self, string):
        with open(self.path, 'a') as f:
            f.write(string)

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def __add__(self, other):
        new_path = os.path.join(tempfile.gettempdir(), self.name + '_' + other.name)
        cur_path = new_path
        i = 1
        while os.path.isdir(cur_path + self.ext) or os.path.isfile(cur_path + self.ext):
            cur_path = new_path + '_' + str(i)
            i += 1
        new_path = cur_path + self.ext
        with open(new_path, 'w') as f:
            f.write(self.read())
            f.write(other.read())
        return File(new_path)

    def __iter__(self):
        self.iter = open(self.path, 'r')
        return self

    def __next__(self):
        result = self.iter.readline()
        if not result:
            self.iter.close()
            del self.iter
            raise StopIteration
        return result

    def __str__(self):
        return self.path
