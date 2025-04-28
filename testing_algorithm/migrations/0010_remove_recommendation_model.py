from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('testing_algorithm', '0009_remove_choice_score_choice_cold_score_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Recommendation',
        ),
    ]