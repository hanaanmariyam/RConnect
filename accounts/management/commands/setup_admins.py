from getpass import getpass
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from accounts.models import User
from clubs.models import Club
from events.models import CollegeUnion

ADMINS = [
    ("Aarathi Shankar", "aarathi@gmail.com", "CLUB_ADMIN", "Dance Club"),
    ("Abina Jaleel", "Abina@gmail.com", "CLUB_ADMIN", "Music Club"),
    ("Jesna Jacob", "Jesna@gmail.com", "CLUB_ADMIN", "C-Star"),
    ("Dilna Biju", "Dilna@gmail.com", "CLUB_ADMIN", "Fashion Club"),
    ("Haleema Fahma M C", "haleema@gmail.com", "UNION_ADMIN", "College Union"),
]

class Command(BaseCommand):
    help = "Create/update the five specified RConnect administrator accounts. Passwords are entered securely at the terminal."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("RConnect administrator setup. Passwords will NOT be saved in this command or README.")
        for name,email,role,assignment in ADMINS:
            user, created = User.objects.get_or_create(username=email.lower(), defaults={"email":email.lower()})
            user.email=email.lower()
            user.first_name=name
            user.role=role
            user.is_staff=True
            if created:
                while True:
                    p1=getpass(f"Create password for {name} ({email}): ")
                    p2=getpass("Confirm password: ")
                    if p1 and p1==p2:
                        break
                    self.stderr.write("Passwords were empty or did not match. Try again.")
                user.set_password(p1)
            user.save()
            if role=="CLUB_ADMIN":
                club=Club.objects.get(name=assignment)
                club.assigned_admin=user
                club.save(update_fields=["assigned_admin"])
            else:
                union=CollegeUnion.objects.get(name="College Union")
                union.assigned_admin=user
                union.save(update_fields=["assigned_admin"])
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'} {name} — {email}"))
        self.stdout.write(self.style.SUCCESS("Administrator setup complete."))
