import os

def empty_directory(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(project_root, '..', '..', 'data')
    empty_directory(data_directory)
    print("Data directory cleaned up.")

if __name__ == "__main__":
    main()