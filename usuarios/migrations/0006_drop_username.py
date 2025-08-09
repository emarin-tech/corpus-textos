from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_alter_usuario_managers'),  # deja la que te haya puesto Django
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE usuarios_usuario
              DROP CONSTRAINT IF EXISTS usuarios_usuario_username_key;
            ALTER TABLE usuarios_usuario
              DROP COLUMN IF EXISTS username;
            """,
            reverse_sql="""
            ALTER TABLE usuarios_usuario
              ADD COLUMN username varchar(150);
            ALTER TABLE usuarios_usuario
              ADD CONSTRAINT usuarios_usuario_username_key UNIQUE (username);
            """
        ),
    ]
