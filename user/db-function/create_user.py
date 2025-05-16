import time
from django.contrib.auth.models import User
from django.db import IntegrityError, DatabaseError


def create_users(num_users):
    start_time = time.time()  # Vaqtni yozish
    with open('errors.log', 'a') as error_file:
        for i in range(1, num_users + 1):
            username = f'user_{i}'
            password = f'password_{i}'
            try:
                User.objects.create_user(username=username, password=password)
            except IntegrityError as e:
                error_file.write(f"IntegrityError: {e} for username {username}\n")
            except DatabaseError as e:
                error_file.write(f"DatabaseError: {e}\n")
            except Exception as e:
                error_file.write(f"Unexpected error: {e}\n")

    end_time = time.time()  # Tugash vaqtini yozish
    duration = end_time - start_time  # Umumiy vaqtni hisoblash

    # Vaqtni yangi faylga yozish
    with open('execution_time.log', 'a') as time_file:
        time_file.write(f"User creation completed in {duration:.2f} seconds.\n")


