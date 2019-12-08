import os

class dir_class:
    def __init__(self):
        pass

    def clearFiles(self):
        # self.del_file('/home/mmap/vsa_server/camera/')
        self.del_file('/home/mmap/vsa_server/camera/txt_results/')
        # self.del_file('/home/mmap/vsa_server/camera/imgs/')
        # self.del_file('/home/mmap/mmap/VSA_Server/test')
        print("Dirs have been clear!")

    def del_file(self, path):
        if os.path.exists(path):
            for i in os.listdir(path):
                path_file = os.path.join(path, i)
                if os.path.isfile(path_file):
                    os.remove(path_file)
                    print(path_file + ' ' + 'has been deleted!')
                else:
                    self.del_file(path_file)
        else:
            print("Check your Path!")


if __name__ == '__main__':
    operator = dir_class()
    operator.clearFiles()
    # operator.mkdir()
