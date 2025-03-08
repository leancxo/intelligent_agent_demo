# main.py
import streamlit as st
import subprocess
import sys


def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'langchain', 'openai', 'python-dotenv', 'requests',
        'pydantic', 'tiktoken', 'matplotlib', 'pandas', 'streamlit'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("All packages installed successfully!")


def main():
    """Main function to run the application."""
    # Check dependencies
    check_dependencies()

    # Run the Streamlit app
    subprocess.run(["streamlit", "run", "ui.py"])


if __name__ == "__main__":
    main()