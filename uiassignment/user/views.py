from django.views import View
from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseForbidden,
)
from .models import UserModel
from uiassignment.db import session_factory
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from contextlib import ExitStack
import jwt
from pathlib import Path


# TODO - we should load these key in global config scope
private_key = Path("private.pem").read_text()
public_key = Path("public.pem").read_text()


def user_list():
    with ExitStack() as stack:
        # TODO - There may be better way to make sure session is always closed even error occur
        session = session_factory()
        stack.callback(session.close)

        user_query = session.query(UserModel)

        return JsonResponse({"d": [user.json() for user in user_query.all()]})


def user_info(request: HttpRequest, acct: str):
    with ExitStack() as stack:
        session = session_factory()
        stack.callback(session.close)

        user_query = session.query(UserModel).filter_by(acct=acct)

        user = user_query.one_or_none()
        if user:
            return JsonResponse({"d": user.json()})
        else:
            return HttpResponseNotFound()


def user_create(request: HttpRequest, acct: str):
    with ExitStack() as stack:
        session = session_factory()
        stack.callback(session.close)

        # TODO - we should validate this POST body
        body = json.loads(request.body)
        now = datetime.now()

        # TODO - we shouldn't store password directly in database, at least
        # we should do some hashing.
        user = UserModel(acct, body["pwd"], body["fullname"], now, now)

        session.add(user)
        session.commit()
        session.close()

        # TODO - we should return the object created. I didn't just
        # run another query to get the object here because the result
        # might be influenced by another request, so we have to think
        # futher way to achive this.
        return JsonResponse({"d": "ok"})


def user_update(request: HttpRequest, acct: str):
    with ExitStack() as stack:
        session = session_factory()
        stack.callback(session.close)

        # TODO - we should validate this POST body
        body = json.loads(request.body)
        now = datetime.now()

        # TODO - we should check if target user is exist and give appropriate response
        session.query(UserModel).filter_by(acct=acct).update(
            {"fullname": body["fullname"], "updated_at": now}
        )

        session.commit()

        return JsonResponse({"d": "ok"})


def user_delete(request: HttpRequest, acct: str):
    with ExitStack() as stack:
        session = session_factory()
        stack.callback(session.close)

        # TODO - we should check if target user is exist and give appropriate response
        session.query(UserModel).filter_by(acct=acct).delete()
        session.commit()

        return JsonResponse({"d": "ok"})


def auth_api(request: HttpRequest):
    token = request.headers.get("Authorization")
    if not token:
        return None, False

    # TODO - we should return False when decoded fail
    token = jwt.decode(token, public_key, algorithms=["RS256"])
    return token, True


def users_view(request: HttpRequest):
    ctx, authed = auth_api(request)
    if not authed:
        return HttpResponseForbidden

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    return user_list()


# TODO - Finish CSRF
@csrf_exempt
def user_view(request: HttpRequest, acct: str):
    # TODO - we should validate the input from api to prevent from injection

    # TODO - we should improve how api was routed. In my previous experience,
    # we use Node.js, so we can routed different method to different function
    # easily. However, Django seems to be MVT framework, so it routing logic is
    # not design for RESTful api. There seems to be some extension to achieve
    # this, however, it take some time to study that library and add more complexity.
    # I think this project can be finished by Flask with much more cleaner code
    # for someone not working with Django ecosystem previously.

    if request.method == "POST":
        return user_create(request, acct)

    ctx, authed = auth_api(request)
    if not authed:
        return HttpResponseForbidden

    if request.method == "GET":
        return user_info(request, acct)
    elif request.method == "DELETE":
        return user_delete(request, acct)
    elif request.method == "PUT":
        return user_update(request, acct)

    return HttpResponseNotAllowed(["GET", "POST", "DELETE", "PUT"])


def search_user_view(request: HttpRequest, fullname: str):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    with ExitStack() as stack:
        session = session_factory()
        stack.callback(session.close)

        # TODO - As the same, we should avoid injection
        user_query = session.query(UserModel).filter(
            UserModel.fullname.ilike(f"%{fullname}%")
        )

        return JsonResponse({"d": [user.json() for user in user_query.all()]})


def token_view(request: HttpRequest, acct: str):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    with ExitStack() as stack:
        session = session_factory()
        stack.callback(session.close)

        # TODO - we should validate this POST body
        body = json.loads(request.body)

        user_query = session.query(UserModel).filter_by(acct=acct)

        user = user_query.one_or_none()
        if user:
            # TODO - we shouldn't store password directly in database, at least
            # we should do some hashing.
            if user.pwd == body["pwd"]:
                token = jwt.encode({"acct": acct}, private_key, algorithm="RS256")

                return JsonResponse({"d": token})
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseNotFound()
