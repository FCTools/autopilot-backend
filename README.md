# Autopilot Backend

<p align="center">
<a href="https://t.me/alcatraz_rm"><img src="https://img.shields.io/badge/Telegram Chat-@alcatraz_rm-2CA5E0.svg?logo=telegram&style=for-the-badge" alt="Chat on Telegram"/></a>
<img src="https://img.shields.io/badge/version-v.0.0.1-green?style=for-the-badge" alt="Last Release"/>
</p>

## Autopilot backend (python/django-based bot managing service)
Project name for copyright: autopilot.autopilot-backend

Supported functions:
* Create/view/update/delete bots:
    * set name for bot
    * write flexible conditions for traffic optimizations 
    * set schedule and period for conditions checking
    * select traffic source and campaigns list for checking
    
Frontend part now implemented using default Django Admin module.

Supported traffic sources:
* Propeller Ads ([api documentation](https://ssp-api.propellerads.com/v5/docs/#/))

Stack:
* [Django](https://www.djangoproject.com/) and [DRF](https://www.django-rest-framework.org/) frameworks for REST-API and admin site
* [requests](https://requests.readthedocs.io/en/master/) for http-requests
* [PostgreSQL](https://www.postgresql.org/) for bots and other data storing
* [python-crontab](https://pypi.org/project/python-crontab/) and crontab for bots conditions checking depending on schedule

<br>
<br>
<p align="center">
Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
</p>
