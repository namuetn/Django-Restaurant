

def detect_user(user):
    if user.role == 1:
        return 'vendorDashboard'
    elif user.role == 2:
        return 'customerDashboard'
    elif user.role == None and user.is_superadmin:
        return '/admin'
