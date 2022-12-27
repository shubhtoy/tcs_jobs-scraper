# Purpose: To scrape all the jobs from TCS website
# Author: @shubhtoy
# Python Version: 3.10.1


# Importing the required libraries
import requests
from requests.structures import CaseInsensitiveDict
from threading import Thread
import math
import json

# Defining the URL's
url_base = "https://ibegin.tcs.com/iBegin/api/v1/jobs/searchJ?at=1672163172964"

url_job = "https://ibegin.tcs.com/iBegin/api/v1/job/desc?at=1672165520462"

# Defining global variables
all_jobs = []
page_numbers = 0
OUTPUT_FILE = "jobs.json"

# Defining the headers
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json, text/plain, */*"
headers["Accept-Language"] = "en-US,en;q=0.7"
headers["Connection"] = "keep-alive"
headers["Content-Type"] = "application/json;charset=UTF-8"
headers[
    "Cookie"
] = 'JSESSIONID="FMHNldxETaGABg2Rjvs3yLR0A3ZslDTDd-cGv3U2.master:server-three"; ROUTEID=.3; TS013b808c=0199acb0de4f1e02da4d00351754b87bb7efbe720f099a63ba577f6a29d78f9078fac71cca01137dd5a8e3bf35b13465665880f904078f3701636fe5f3b99179a519a2229d07c05ab0b7ba8574649e2eb63cedd8c4; TS01ab71c3=0199acb0dea90242f4d48a4b895e6f6d7e7030a3e687561cc8a9a8a81bca2d38a00014cc3db27e9e2b653eb82f9206111b7cf3ec1e'
headers["Origin"] = "https://ibegin.tcs.com"
headers["Referer"] = "https://ibegin.tcs.com/iBegin/jobs/search"
headers["Sec-Fetch-Dest"] = "empty"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Site"] = "same-origin"
headers["Sec-GPC"] = "1"
headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

data_base = {"pageNumber": "", "regular": "true", "walkin": "true"}
data_job = {"jobId": ""}

# Get the base data
def get_base(page_number):
    data_base["pageNumber"] = page_number
    resp = requests.post(url_base, headers=headers, data=str(data_base))
    resp = resp.json()["data"]
    return resp


# Get the job description
def get_job(job_id):
    data_job["jobId"] = job_id
    resp = requests.post(url_job, headers=headers, data=str(data_job))
    resp = resp.json()["data"]
    return resp


# Get the total number of jobs
def get_total_jobs():
    global page_numbers
    page_numbers = math.ceil(get_base(1)["totalJobs"] / 10)


# Get all the jobs using threads
def get_all_jobs():
    threads = []
    for i in range(1, page_numbers + 1):
        threads.append(Thread(target=lambda: all_jobs.extend(get_base(i)["jobs"])))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


# Update the job description
def update_job(job):
    job.update(get_job(job["id"][:-1]))
    # print(job)


# get all job descriptions using threads
def get_all_job_desc():
    threads = []
    for job in all_jobs:
        threads.append(Thread(target=update_job, args=(job,)))
        # break
    for thread in threads:
        thread.start()
        # break
    for thread in threads:
        thread.join()
        # break


# Write to json
def to_json():

    new_dict = {}
    new_dict["Company"] = "TCS"
    new_dict["Carrer Page"] = "https://ibegin.tcs.com/iBegin/jobs/search"
    new_dict["Jobs"] = all_jobs

    with open(OUTPUT_FILE, "w") as f:
        json.dump(new_dict, f, indent=4)


# Main function
def main():
    print("Starting")
    # print("Getting all jobs")
    get_total_jobs()
    print("Total Jobs: ", get_base(1)["totalJobs"])
    print("Scraping all jobs")
    get_all_jobs()
    print("Scraping all job descriptions")
    get_all_job_desc()
    print("Writing to json")
    to_json()
    print("Done")


if __name__ == "__main__":
    main()
