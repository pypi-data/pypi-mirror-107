import random

import pomace

from . import Script


class Salesflare(Script):

    URL = "https://integrations.salesflare.com/s/tortii"
    SKIP = True

    def run(self, page) -> pomace.Page:
        pomace.log.info("Launching form")
        page = page.click_request_this_listing(wait=0)
        page.fill_email(pomace.fake.email)
        page.fill_company(pomace.fake.company)

        pomace.log.info("Submitting form")
        return page.click_submit(wait=1)

    def check(self, page) -> bool:
        success = "Thank you for your request" in page
        page.click_close(wait=0.1)
        return success


class SavannahTaphouse(Script):

    URL = "https://savannahtaphouse.com/contact/"

    MESSAGES = [
        "You should treat your employees better.",
        "You should pay your employees more.",
        "You should protect your customers.",
    ]

    def run(self, page) -> pomace.Page:
        person = pomace.fake.person

        pomace.log.info("Filling form")
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)
        page.fill_message(random.choice(self.MESSAGES))

        pomace.log.info("Submitting form")
        page.browser.execute_script("window.scrollTo(0, 500);")

        return page.click_send_message()

    def check(self, page) -> bool:
        return "sent successfully" in page


class CrownChoice(Script):

    URL = "http://www.mackinawcity.net/contact.php"

    MESSAGES = [
        "Are any of your businesses not owned by hateful Trump cultists?",
        "Crown Choice Inn & Suites has always abused guests. You should shut them down.",
        "Joe and Enzo Lieghio are ruining Mackinaw City. When will you kick them out?",
        "Mackinaw City police are out of control. The Lieghios should be charge with falsifying a report.",
        "I just wanted to let you know that I've cancelled my trip to Mackinaw City because your hotel chains are owned by hateful Trump supporters.",
        "The Lieghio-owned hotels should be removed from your website. That kind of hate doesn't belong in Mackinaw City.",
    ]

    def run(self, page) -> pomace.Page:
        while True:
            person = pomace.fake.person
            if person.state == "Michigan":
                break

        pomace.log.info("Filling form")
        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_email(person.email)
        page.fill_address(person.address)
        page.fill_city(person.city)

        page.browser.execute_script("window.scrollTo(0, 500);")
        page.click_state(wait=0)
        page.browser.find_by_text(person.state).click()

        page.fill_postal_code(person.zip_code)

        page.click_how(wait=0)
        page.browser.find_by_text("Other").click()

        page.fill_message(random.choice(self.MESSAGES))

        pomace.log.info("Submitting form")
        return page.click_submit()

    def check(self, page) -> bool:
        return "Thank you" in page
