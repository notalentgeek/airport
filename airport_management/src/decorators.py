from ..consts import STRING

"""
This function was meant for view that can only be accessed by certain group.
However, because there is only one kind of `User` in this prototype, this
function is not currently being used.
"""
def airport_manager_login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated() and\
            user.groups.filter(name=STRING.AIRPORT_MANAGER_GROUP).exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponse("you are not allowed to see this web page")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap