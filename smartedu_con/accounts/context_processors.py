def user_type(request):
    user_type = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'student'):
            user_type = 'student'
        elif hasattr(request.user, 'teacher'):
            user_type = 'teacher'
    return {'user_type': user_type}
