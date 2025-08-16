#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project.settings")
    try:
        import django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc

    # 🔧 Setup Django before using any models
    django.setup()

    # ✅ Now it's safe to import and clear sessions
    from django.contrib.sessions.models import Session
    Session.objects.all().delete()  # This logs out all users on server start

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
