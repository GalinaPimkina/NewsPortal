from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        category = Category.objects.get(name=options['category_name'])
        Post.objects.filter(category=category).delete()
        self.stdout.write(self.style.SUCCESS(f'Успешно удалены все записи из категории {category.name}'))
