from accounts.models import User


def create_user(email: str, first_name: str, last_name: str, password: str) -> User:
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    return user


def create_superuser(email: str, first_name: str, last_name: str, password: str) -> User:
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user
