import sys

from streamlit import cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "budd.py", "--server.headless", "true"]
    stcli.main()
