from django.db import migrations


def seed_services(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    Service.objects.bulk_create([
        Service(
            name='Lavage interne et externe',
            description='Nettoyage complet de l\'intérieur (sièges, tapis, tableau de bord) et de l\'extérieur (carrosserie, vitres, jantes).',
            price=25.00,
            duration_minutes=45,
        ),
        Service(
            name='Lavage externe',
            description='Lavage extérieur complet : carrosserie, vitres, jantes et pneus.',
            price=15.00,
            duration_minutes=30,
        ),
        Service(
            name='Lavage rapide',
            description='Lavage extérieur rapide pour un entretien régulier à petit prix.',
            price=10.00,
            duration_minutes=15,
        ),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_translate_services_to_french'),
    ]

    operations = [
        migrations.RunPython(seed_services),
    ]
