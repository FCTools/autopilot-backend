from web.backend.celery import app
from bot_manager.services.helpers.condition_parser import ConditionParser
from bot_manager.models import Bot


@app.task
def check_bots():
    with open('something.txt', 'w', encoding='utf-8') as file:
        bots = Bot.objects.filter(status="enabled")

        for bot in bots:
            if bot.type == 1:
                for campaign in bot.campaigns_list.all():
                    sites = ConditionParser.check_sites(bot.condition, campaign.id)
                    file.write(f"bot: {bot.id}, action: {bot.action}, campaign: {campaign.id}, sites: {str(sites)}\n")

