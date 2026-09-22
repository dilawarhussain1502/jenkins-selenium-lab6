import time
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_performance_test():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    url = "https://example.com"

    start_time = time.time()
    driver.get(url)
    end_time = time.time()

    load_time = round(end_time - start_time, 4)
    print(f"Page Load Time for {url}: {load_time} seconds")

    driver.quit()

    cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')

    cloudwatch.put_metric_data(
        Namespace='WebPerformance',
        MetricData=[
            {
                'MetricName': 'PageLoadTime',
                'Value': load_time,
                'Unit': 'Seconds',
                'Dimensions': [
                    {
                        'Name': 'WebPage',
                        'Value': 'example.com'
                    },
                ]
            },
        ]
    )
    print("Metric successfully pushed to AWS CloudWatch!")

if __name__ == "__main__":
    run_performance_test()
