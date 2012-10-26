from controller import app
from model import Archive
from tasks import RescrapeTask
import logging

def main():
    logging.basicConfig(level=logging.DEBUG,
        format='[%(asctime)s] [%(levelname)s] %(message)s')

    Archive.reload()
    RescrapeTask().start()
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    main()
