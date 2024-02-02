import faker
from playwright.sync_api import sync_playwright

URL = "https://app.bearsoft.ir/user/register"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()

    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto(URL)

    textboxes = page.query_selector_all(".form-control")
    page.wait_for_selector(textboxes)

    fake = faker.Faker()

    data = [
        fake.name().replace(" ", ""),
        fake.name().split()[0] + "@test.com",
        fake.phone_number(),
        fake.name(),
    ]

    for textbox, value in zip(textboxes, data):
        page.fill(textbox, data)

    checkbox_selector = "form-check-input"
    page.check(checkbox_selector)

    context.tracing.stop(path="trace2.zip")

    browser.close()
