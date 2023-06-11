from django.http.request import HttpRequest
from django.http import HttpResponse
from django.http.response import ResponseHeaders

from holder.models import User


def create_user() -> User:
    user = User()
    user.save()
    return user


def user_identifier(get_response):
    def middleware(request: HttpRequest):
        user_uuid = request.COOKIES.get('user_uuid')
        print(user_uuid)
        if user_uuid is None:
            print("User not found!")
            user = create_user()
        else:
            user = User.objects.filter(uniq_uuid=user_uuid).first()
            if user is None:
                user = create_user()

        response: HttpResponse = get_response(request)
        response.set_cookie('user_uuid', user.uniq_uuid)
        return response

    return middleware
