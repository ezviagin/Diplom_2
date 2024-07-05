from faker import Faker
import random
import string

fake = Faker()


def generate_username():
    return fake.user_name() + str(random.randint(1, 100))


def generate_email():
    return fake.email()


def generate_password(min_length=8):
    # Generate password with at least min_length characters
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for _ in range(min_length))
