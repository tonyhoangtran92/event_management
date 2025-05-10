import random
import uuid
from datetime import datetime
from datetime import timezone

from faker import Faker
from pynamodb.exceptions import PutError

from app.models import Event
from app.models import User
from app.models import UserEvent

fake = Faker()


# Create a random user
def create_fake_user(index):
    user_id = uuid.uuid4().hex

    return User(
        PK=f"USER#{user_id}",
        SK="PROFILE",
        user_id=user_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone_number=fake.phone_number(),
        email=f"user{index}@example.com",
        avatar=fake.image_url(),
        gender=random.choice(["male", "female", "other"]),
        job_title=random.choice(["Engineer", "Designer", "Manager", "Analyst"]),
        company=random.choice(["Acme Corp", "Globex", "Initech", "Umbrella Corp"]),
        city=random.choice(["New York", "Tokyo", "San Francisco", "Berlin", "Paris"]),
        state=random.choice(["NY", "CA", "TX", "FL", "WA"]),
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat(),
        deleted_at=None,
    )


# Create a random event
def create_fake_event(index):
    event_id = uuid.uuid4().hex

    return Event(
        PK=f"EVENT#{event_id}",
        SK="DETAILS",
        event_id=event_id,
        slug=fake.slug(),
        title=fake.sentence(nb_words=6),
        description=fake.text(),
        start_at=fake.date_this_year().isoformat(),
        end_at=fake.date_this_year().isoformat(),
        venue=fake.city(),
        max_capacity=str(random.randint(50, 500)),
        owner=f"USER#{random.randint(1, 1000)}",
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat(),
        deleted_at=None,
    )


# Create a user-event relationship
def create_user_event(user, event, role):
    user_event_id = uuid.uuid4().hex
    return UserEvent(
        PK=user_event_id,
        SK=f"EVENT#{event.event_id}",
        user_id=user.user_id,
        event_id=event.event_id,
        role=role,
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat(),
        deleted_at=None,
    )


# Bulk create users
def bulk_create_users(count=1000):
    print(f"Creating {count} users...")
    for i in range(count):
        user = create_fake_user(i)
        try:
            user.save()
        except PutError as e:
            print(f"Error saving user {user.PK}: {e}")
        if i % 100 == 0:
            print(f"Created {i} users...")
    print("User creation done.")


# Bulk create events and user-event relationships
def bulk_create_events_and_user_events(num_events=100, num_users=1000):
    print(f"Creating {num_events} events and user-event relationships...")

    # Step 1: Create Events
    events = []
    for i in range(num_events):
        event = create_fake_event(i)
        event.save()
        events.append(event)
        if i % 10 == 0:
            print(f"Created {i} events...")

    # Step 2: Assign Users to Events as Hosts or Attendees
    users = User.scan()
    user_list = list(users)

    # Creating user-event relationships
    for i, event in enumerate(events):
        num_users_in_event = random.randint(10, 50)
        users_in_event = random.sample(user_list, num_users_in_event)

        # Using batch write
        with UserEvent.batch_write() as batch:
            for user in users_in_event:
                role = "host" if random.random() < 0.1 else "attendee"  # 10% chance to be a host
                user_event = create_user_event(user, event, role)
                batch.save(user_event)

        if i % 10 == 0:
            print(f"Assigned users to event {i}...")

    print("Event and UserEvent creation done.")


def create_fixture_data(user_count=1000, event_count=100, user_event_count=1000):
    for model in [Event, User, UserEvent]:
        if not model.exists():
            model.create_table(read_capacity_units=1000, write_capacity_units=1000, wait=True)

    bulk_create_users(user_count)

    bulk_create_events_and_user_events(event_count, user_event_count)
