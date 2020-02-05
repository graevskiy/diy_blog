import os
import json

from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from blog.models import BlogPost, BlogCategory


class Command(BaseCommand):
    help = 'registers blog posts from output.json file in DB'

    def add_arguments(self, parser):
        parser.add_argument(
            'files',
            nargs='+'
        )

    def handle(self, *args, **options):

        self.data = []
        for _file in options['files']:
            
            _file = os.path.join(os.path.dirname(__file__), _file)
            self.stdout.write(f"{_file}")
            if os.path.exists(_file):
                # do json only for now
                with open(_file, mode='r', encoding='utf-8') as f:
                    try:
                        self.data = json.load(f)
                    except JSONDecodeError:
                        self.stdout.write(f"'{_file}' is not a valid JSON")
            else:
                self.stdout.write(f"file '{_file}' was not found")
                return

            # self.data is a list of dicts. each dict has only one key = category name like stocks, bonds etc
            # value is a list of posts where each post is a dict.
            for dict_item in self.data:
                for category, blogs in dict_item.items():
                    cat = BlogCategory.objects.filter(name=category).first()
                    if not cat:
                        cat = BlogCategory(
                            name = category
                        )
                        cat.save()
                    for post in blogs:
                        p_date = datetime.strptime(post['pub_date'], r"%m/%d/%Y %I:%M:%S %p %Z%z").date()
                        p = BlogPost(
                                name=post['title'],
                                body=post['body'],
                                pub_date=p_date, #11/13/2019 11:45:36 AM UTC+0300
                                category=cat
                            )
                        p.save()






