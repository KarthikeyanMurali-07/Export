import os
import subprocess
import py7zr  # Make sure you have py7zr installed: pip install py7zr

def run_command(command, cwd=None):
    """Run a shell command and return its output."""
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout.strip()

def clone_repository(repo_url, local_dir):
    """Clone a git repository to a local directory."""
    if not os.path.exists(local_dir):
        print(f"Cloning repository from {repo_url} to {local_dir}...")
        run_command(f"git clone {repo_url} {local_dir}")
    else:
        print(f"Repository already cloned to {local_dir}.")

def pull_changes(local_dir):
    """Pull the latest changes from the remote repository."""
    print(f"Pulling latest changes in {local_dir}...")
    run_command("git pull", cwd=local_dir)

def list_files(local_dir):
    """List all files in the local repository directory."""
    print(f"Listing files in {local_dir}...")
    files = run_command("git ls-tree -r HEAD --name-only", cwd=local_dir)
    print("Files in repository:")
    print(files)
    return files.splitlines()

def extract_7z_files(local_dir, files):
    """Extract .7z files found in the repository."""
    for file in files:
        if file.endswith(".7z"):
            file_path = os.path.join(local_dir, file)
            print(f"Extracting {file_path}...")
            with py7zr.SevenZipFile(file_path, mode='r') as archive:
                archive.extractall(path=os.path.dirname(file_path))
            print(f"Extracted {file_path} to {os.path.dirname(file_path)}.")

def main():
    repo_url = "https://github.com/username/repository.git"  # Replace with your repository URL
    local_dir = "repository"  # Local directory where the repo will be cloned
    
    try:
        clone_repository(repo_url, local_dir)
        pull_changes(local_dir)
        files = list_files(local_dir)
        extract_7z_files(local_dir, files)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
