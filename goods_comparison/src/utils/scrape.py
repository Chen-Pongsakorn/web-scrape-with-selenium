import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Scrape:
    def __init__(
        self,
        url=None,
        is_incognito=True,
        browser="chrome",
        timeout=60,
    ):
        if url:
            self.url = url
        else:
            raise Exception("Missing target url")
        self.method = {"xpath": By.XPATH}
        self.is_incognito = is_incognito
        self.browser = browser
        self.timeout = timeout  # timeout for each element
        self.is_started_driver = False

    def __get_driver(self):
        print("...Getting driver")
        if self.browser == "chrome":
            option = webdriver.ChromeOptions()
            if self.is_incognito:
                option.add_argument("--incognito")

            self.driver = webdriver.Chrome(options=option)
            self.driver.get(self.url)
            time.sleep(10)

        return True

    def __find_element(
        self, method="xpath", element=None
    ):
        element_value = None
        if element:
            method = self.method.get(method, {})
            if method:
                if self.is_started_driver == False:
                    print("!!!!!!!!no driver...")
                    self.is_started_driver = self.__get_driver()
                element_value = self.driver.find_element(
                    method, element
                )

        return element_value
    
    def __scroll_down(self, scroll_down_by=None, scroll_down_times=None):
        if scroll_down_times:
            for _ in range(scroll_down_times):
                self.driver.execute_script(f"window.scrollBy(0,{str(scroll_down_by)})")
                time.sleep(5)

    def find_element(
        self, find_element_step=None, method="xpath"
    ):
        """
        find_element_step is step to find element
        here are the keys
            - element
            - output
            - key_value
            - scroll_down_by
            - scroll_down_times
        to find the output in current url, you need to set
            element = your target element
            output = text
        to find multiple output in current url, you need to set multiple object with the same as above
        if you need to interact site before getting output, you need to set these before taking first step
            element = your target element
            output = your action (click, search)
            key_value = your search value
            scroll_down_by = scroll pixel
            scroll_down_times = how many times you want to scroll

        result will be list of dict that contain text_result as a key
        """

        result = []
        if find_element_step:
            for item in find_element_step:
                print(item)
                start_time = time.time()
                while True:
                    try:
                        element = item.get("element", None)
                        if element:
                            print("...Start find element")
                            result_element = self.__find_element(
                                method, element
                            )
                            print("...Finish find element")
                        if item.get("output", None) == "text":
                            print("...Start adding result_element")
                            result_element = {"text_result": result_element.text}
                            result.append(result_element)
                            print("...Finish add result_element")
                            break
                        elif item.get("output", None) == "click":
                            print("...Start click")
                            # result_element.click()
                            self.driver.execute_script("arguments[0].click();", result_element)
                            time.sleep(10)
                            result.append(None)
                            print("...Finish click")
                            break
                        elif item.get("output", None) == "search":
                            print("...Start search")
                            result_element.send_keys(item.get("key_value", None))
                            result_element.send_keys(Keys.RETURN)
                            result.append(None)
                            print("...Finish search")
                            break
                        elif item.get("output", None) == "scroll_down":
                            print("...Start scroll_down")
                            scroll_down_by = item.get("scroll_down_by", None)
                            scroll_down_times = item.get("scroll_down_times", None)
                            if self.is_started_driver == False:
                                self.is_started_driver = self.__get_driver()
                            self.__scroll_down(scroll_down_by, scroll_down_times)
                            result.append(None)
                            print("...Finish scroll_down")
                            break

                    except Exception as e:
                        if time.time() - start_time > self.timeout:
                            print("...Timeout reached. No element found.")
                            break  # Exit the loop if the timeout is reached
                        else:
                            print("...Retry find element")
                            time.sleep(1)

        return result
