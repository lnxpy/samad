from dataclasses import dataclass
from time import sleep

from playwright.sync_api import sync_playwright

from consts import URL


@dataclass
class Web:
    ...


def connector(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()

        cdp_session = page.context.new_cdp_session(page)
        cdp_session.send("Network.setCacheDisabled", {"cacheDisabled": True})

        page.goto(URL)

        print("1 ]]")

        # Wait for the div with class name "input-btn-edit" to be visible
        div_selector = "div.input-btn-edit"
        page.wait_for_selector(div_selector)
        # Click the div element
        div_element = page.query_selector(div_selector)
        div_element.click()

        print("2 ]]")

        # Wait for the 21st li to be visible
        li_selector = "li:nth-child(21)"
        page.wait_for_selector(li_selector)
        # Click the 21st li element
        li_element = page.query_selector(li_selector)
        li_element.click()

        print("3 ]]")

        # Wait for the input with the name attribute 'username' to be visible
        username_selector = 'input[name="username"]'
        page.wait_for_selector(username_selector)
        # Type a value into the username field
        username_element = page.query_selector(username_selector)
        username_element.fill(username)

        print("4 ]]")

        # Wait for the input with the name attribute 'username' to be visible
        username_selector = 'input[name="password"]'
        page.wait_for_selector(username_selector)
        # Type a value into the username field
        username_element = page.query_selector(username_selector)
        username_element.fill(password)

        print("5 ]]")

        # Wait for the button with class name 'ant-btn' to be visible
        button_selector = "button.ant-btn"
        page.wait_for_selector(button_selector)
        # Click the button
        button_element = page.query_selector(button_selector)
        button_element.click()

        sleep(3)

        print("6 ]]")

        context.tracing.stop(path="trace.zip")
        # Wait for the button with class name 'ant-btn' to be visible
        panel = "div.app-food-slide-content"
        page.wait_for_selector(panel)

        button_selector = (
            page.query_selector(panel).query_selector("button").as_element()
        )

        # Click the button
        button_selector.click()

        context.tracing.start(screenshots=True, snapshots=True)

        print("7 ]]")

        forget_card_modal_text = page.wait_for_selector("div.forgetCard-modal-text")

        parent_div_handle = forget_card_modal_text.evaluate_handle(
            "(element) => element.parentElement"
        ).as_element()

        qrcode = parent_div_handle.query_selector("svg").inner_html()
        # qrcode = qrcode.evaluate_handle("(element) => element.outerHTML")

        print("8 ]]")

        data = {
            "primary": parent_div_handle.query_selector_all("div")[4].inner_text(),
            "secondary": parent_div_handle.query_selector_all("div")[5].inner_text(),
            "qrcode": str(qrcode).replace('"', "'"),
            "ncode": parent_div_handle.query_selector_all("div")[7].inner_text(),
        }

        browser.close()

        return data
