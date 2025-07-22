from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'vault':
        Category = apps.get_model('vault', 'Category')

        default_categories = [
            {'name': 'Social Media', 'icon': 'people', 'color': '#1DA1F2'},
            {'name': 'Email', 'icon': 'envelope', 'color': '#EA4335'},
            {'name': 'Banking', 'icon': 'bank', 'color': '#00A86B'},
            {'name': 'Shopping', 'icon': 'bag', 'color': '#FF9500'},
            {'name': 'Work', 'icon': 'briefcase', 'color': '#6B73FF'},
            {'name': 'Entertainment', 'icon': 'play-circle', 'color': '#E50914'},
            {'name': 'Games', 'icon': 'controller', 'color': '#9146FF'},
            {'name': 'Travel', 'icon': 'airplane', 'color': '#FF6B35'},
            {'name': 'Education', 'icon': 'mortarboard', 'color': '#6A4C93'},
        ]

        for cat_data in default_categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color']
                }
            )