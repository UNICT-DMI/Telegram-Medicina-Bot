import telegram, yaml, logging

from modules.medicina_bot.handlers.jobs.scrape_professors import scrape_professors_job

def schedule_jobs(job_queue):
    job_queue.run_repeating(scrape_professors_job, interval=24*60*60, first=0)
