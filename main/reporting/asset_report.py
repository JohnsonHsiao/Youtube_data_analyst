import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd
from googleapiclient.http import MediaIoBaseDownload
from io import FileIO
from datetime import date, timedelta

class Auth():

    def get_authenticated_service(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
        credentials = flow.run_console()
        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials = credentials)

    def auth(self):
        self.youtube_reporting = self.get_authenticated_service()

class Check_Jobs(Auth):

    def check_jobs(self):
        results = self.youtube_reporting.jobs().list().execute()
        if not results:
            self.queued_jobs = []
        else:
            if len(results["jobs"]) != 0:
                self.queued_jobs = [[job["id"], job["reportTypeId"], job["name"], job["createTime"]] for job in results["jobs"]]

class Convert_Csv_To_Excel():

    def convert_csv_to_excel(self, day, job):

        csv_file = pd.read_csv(os.path.join(os.getcwd(), f"{self.channel_name}_data", f"{day}", "csv", f"{job[1]}", f"{job[2].lower().replace(' ', '_')}.csv"))
        csv_file.to_excel(os.path.join(os.getcwd(), f"{self.channel_name}_data", f"{day}", "excel", f"{job[1]}", f"{job[2].lower().replace(' ', '_')}.xlsx"), index=False)

class Create_Jobs(Auth):

    def create_jobs(self, to_create):
        if len(to_create) == 0:
            return
        else:
            for job in to_create:
                reporting_job = self.youtube_reporting.jobs().create(
                    body=dict(
                      reportTypeId=job[0],
                      name=job[1]
                    )
                  ).execute()

class Delete_Jobs(Auth):

    def delete_jobs(self):
        for job_id in self.job_ids:
            self.youtube_reporting.jobs().delete(
                jobId=f"{job_id}"
                    ).execute()

class Download_Reports(Auth):

    def download_reports(self, day, job):
        
        local_file = os.path.join(os.getcwd(), f"{self.channel_name}_data", f"{day}", "csv", f"{job[1]}",  f"{job[2].lower().replace(' ', '_')}.csv")
        
        for report_url in self.report_urls:
            request = self.youtube_reporting.media().download(
                        resourceName=' '
                          )
            request.uri = report_url
            fh = FileIO(local_file, mode='wb')
            downloader = MediaIoBaseDownload(fh, request, chunksize=-1)

            done = False
            while done is False:
                status, done = downloader.next_chunk()

class Get_Reports(Auth):

    def get_reports(self, job, date_dir):
        
        year, month, day = [int (i) for i in date_dir.split("-")]
        date_dir = date(year, month, day)
        
        start_time_at_or_after = str(date_dir) + "T00:00:00.000000Z"
        end_time = str(date_dir + timedelta(days=1)) + "T00:00:00.0000001Z"
        
        results = self.youtube_reporting.jobs().reports().list(
                    jobId=f"{job[0]}",
                    startTimeAtOrAfter=f"{start_time_at_or_after}",
                    startTimeBefore=f"{end_time}"
                        ).execute()
        reports_per_day = []
        if results:
            for report in results["reports"]:
                reports_per_day.append(report)
            self.report_urls = [job_url["downloadUrl"] for job_url in reports_per_day]






