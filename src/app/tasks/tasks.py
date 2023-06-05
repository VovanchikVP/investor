import asyncio

from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin

from src.app.configs.db import DATABASE_URL
from src.app.services.asset_verification import AssetVerificationServices

site = AdminSite(settings=Settings(database_url_async=DATABASE_URL))
scheduler = SchedulerAdmin.bind(site)


@scheduler.scheduled_job("interval", seconds=1800)
def interval_task_test():
    asyncio.run(AssetVerificationServices.create())


# @scheduler.scheduled_job('cron', hour=3, minute=30)
# def cron_task_test():
#     print('cron task is run...')
#
#
# @scheduler.scheduled_job('date', run_date=date(2023, 6, 2))
# def date_task_test():
#     print('date task is run...')
