import os
from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def load_exam_data(sender, **kwargs):
    if sender.name == 'polls':  # Only run when the polls app is migrated
        fixture_path = os.path.join(apps.get_app_config('polls').path, 'fixtures', 'exam_questions.json')
        if os.path.exists(fixture_path):
            try:
                call_command('loaddata', fixture_path, verbosity=0)
                print("✅ Exam questions loaded from fixture.")
            except Exception as e:
                print(f"Could not load exam questions: {e}")
        else:
            print("exam_questions.json not found at expected location.")
