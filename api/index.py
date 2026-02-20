import sys
from streamlit.web import cli as stcli

def run_streamlit():
    sys.argv = ["streamlit", "run", "src/dashboard_app.py", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
    sys.exit(stcli.main())

if __name__ == '__main__':
    run_streamlit()
