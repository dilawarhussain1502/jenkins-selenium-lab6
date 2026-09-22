import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_test():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://alnafi.com/auth/sign-in")

    try:
        element = driver.find_element(By.NAME, "email1")
        print("Element Found. Test Passed.")
    except Exception as e:
        print("Element not found. Test Failed. Sending SNS alert...")

        # Boto3 will automatically use AWS environment variables or AWS CLI credentials
        sns = boto3.client('sns', region_name='us-east-2')

        sns.publish(
            TopicArn='arn:aws:sns:us-east-2:632404568196:SeleniumTestAlerts',
            Message='Selenium Test Failed on alnafi.com: Element "email1" was not found on sign-in page.',
            Subject='Selenium Test Failure Alert'
        )
        print("SNS Notification Sent Successfully!")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
