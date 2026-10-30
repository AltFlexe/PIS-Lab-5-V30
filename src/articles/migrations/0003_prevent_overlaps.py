from django.db import migrations


def create_triggers(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        raise RuntimeError('Для этой учебной базы требуется SQLite.')
    for operation in ('INSERT', 'UPDATE'):
        name = f'articles_no_rental_overlap_{operation.lower()}'
        schema_editor.execute(f'''
            CREATE TRIGGER {name}
            BEFORE {operation} ON articles_contractspace
            WHEN EXISTS (
                SELECT 1 FROM articles_contractspace AS existing
                WHERE existing.space_id = NEW.space_id
                  AND existing.start_date <= NEW.end_date
                  AND existing.end_date >= NEW.start_date
                  AND existing.id != COALESCE(NEW.id, -1)
            )
            BEGIN
                SELECT RAISE(ABORT, 'Помещение уже занято в этом периоде');
            END
        ''')


def drop_triggers(apps, schema_editor):
    for operation in ('insert', 'update'):
        schema_editor.execute(f'DROP TRIGGER IF EXISTS articles_no_rental_overlap_{operation}')


class Migration(migrations.Migration):
    dependencies = [('articles', '0002_contract_space_tenant_payment_contract_tenant_and_more')]
    operations = [migrations.RunPython(create_triggers, drop_triggers)]
