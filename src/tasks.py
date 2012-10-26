import time
from threading import Thread
from model import Archive
from scraper import KnessetScraper
import logging

SECONDS_PER_MINUTE = 60

class Task(Thread):
    WAIT_DURATION = 60 # minutes

    def run(self):
        minutes_passed = 0

        while True:
            if minutes_passed == 0:
                self.do_task()

            time.sleep(SECONDS_PER_MINUTE)
            minutes_passed += 1
            minutes_passed %= self.WAIT_DURATION

    def do_task(self):
        raise NotImplementedError()

class RescrapeTask(Task):
    def do_task(self):
        try:
            logging.info("Scraping knesset website...")
            members = KnessetScraper.scrape()
            if Archive.is_empty() or members != Archive.latest().members:
                logging.info("Got new government members! Saving them.")
                Archive.save_new(members)
            else:
                logging.info("Already got latest government members.")

        except Exception:
            logging.error("Error in rescrape task!", exc_info = True)
