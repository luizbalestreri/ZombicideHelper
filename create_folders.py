import os

def create_directories(project_path):
    directories = [
        'app',
        'app/static',
        'app/templates'
    ]

    for directory in directories:
        directory_path = os.path.join(project_path, directory)
        os.makedirs(directory_path, exist_ok=True)

    # Create __init__.py file inside app directory
    with open(os.path.join(project_path, 'app', '__init__.py'), 'a'):
        pass

    # Create routes.py file inside app directory
    with open(os.path.join(project_path, 'app', 'routes.py'), 'a'):
        pass

    print("Directories and files created successfully.")

if __name__ == "__main__":
    project_path = input("Enter the path for your project directory: ")
    create_directories(project_path)