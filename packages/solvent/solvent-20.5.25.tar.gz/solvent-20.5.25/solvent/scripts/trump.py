import log
import pomace

from . import Script


class Trump(Script):

    URL = "https://www.donaldjtrump.com/desk"

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person

        log.info(f"Beginning iteration as {person}")
        page.click_close(wait=0.5)
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)
        page.fill_phone(person.phone)
        return page.click_save()

    def check(self, page) -> bool:
        return "membership" in page.url
