from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .models import Register,Login,Blog,Notification
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile, Login,  ImageUpload,Package,Payment
import re

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('index')

        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('index')

        user = Register(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            dob=dob,
            password=password,
            confirm_password=confirm_password,
            profile_picture=profile_picture
        )
        user.save()
        Login.objects.create(
            reg_id=user,
            email=email,
            password=password  
        )
        messages.success(request, "Registration successful.")
        return redirect('login')

    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from social_django.utils import psa

# The login view
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email is for an admin or a regular user
        if email == 'admin@gmail.com' and password == 'admin123':
            request.session['is_admin'] = True
            return redirect('adminmain_view')  # Redirect to the admin main view

        # Try to authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.blocked:
                messages.error(request, "Your account has been blocked by the administrator.")
                return redirect('login')

            # Log the user in
            auth_login(request, user)

            # Check if the user has completed their profile
            if check_profile_completion(user):
                messages.success(request, "Login successful.")
                return redirect('profile1', reg_id=user.reg_id)  # Redirect to profile1 if complete
            else:
                messages.success(request, "Login successful. Please complete your profile.")
                return redirect('profile')  # Redirect to profile if not complete
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')

# View to handle login via Google
@psa('social:complete')
def google_login(request, backend):
    user = request.user

    # Check if the user has completed their profile
    if check_profile_completion(user):
        messages.success(request, "Login successful.")
        return redirect('profile1', reg_id=user.reg_id)  # Redirect to profile1 if complete
    else:
        messages.success(request, "Login successful. Please complete your profile.")
        return redirect('profile')  # Redirect to profile if not complete







from django.shortcuts import render, redirect, get_object_or_404
from .models import Register  # Your Register model

def profile_view(request, reg_id):
    # Get the currently logged-in user's email from the session
    current_user_email = request.session.get('user_email')

    if not current_user_email:
        # Redirect to login if no user is logged in
        return redirect('login')

    # Fetch the currently logged-in user object
    current_user = Register.objects.filter(email=current_user_email).first()
    
    if not current_user:
        # Redirect to login if the user does not exist
        return redirect('login')

    # Fetch the profile of the user specified by reg_id
    user_profile = get_object_or_404(Register, reg_id=reg_id)

    # Fetch all users of the opposite gender
    if current_user.gender == 'female':
        # Show male profiles to female users
        other_users = Register.objects.exclude(email=current_user_email).filter(gender='male')
    elif current_user.gender == 'male':
        # Show female profiles to male users
        other_users = Register.objects.exclude(email=current_user_email).filter(gender='female')
    else:
        # In case of other gender preferences or no specific gender
        other_users = Register.objects.exclude(email=current_user_email)

    context = {
        'current_user': current_user,
        'user_profile': user_profile,
        'other_users': other_users,
        'search_query': request.GET.get('query', ''),  # Add the search query to context
    }

    return render(request, 'profile1.html', context)




def view_profile1(request, personal_id):
    profile = get_object_or_404(Profile, personal_id=personal_id)
    education = Education.objects.filter(reg_id=profile.reg_id)
    family = Family.objects.filter(reg_id=profile.reg_id)
    images = ImageUpload.objects.filter(reg_id=profile.reg_id)  # Query for uploaded images

    context = {
        'profile': profile,
        'education': education,
        'family': family,
        'images': images,  # Add images to the context
    }

    return render(request, 'profile_detail.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Education, Family

def check_profile_completion(user):
    # Check if the user has completed their profile, education, and family details
    profile_completed = hasattr(user, 'profile') and user.profile is not None
    education_completed = Education.objects.filter(reg_id=user.reg_id).exists()
    family_completed = Family.objects.filter(reg_id=user.reg_id).exists()
    
    return profile_completed and education_completed and family_completed

from django.shortcuts import render

# views.py
from django.shortcuts import render
from .models import Register, Profile

def view_profiles(request):
    current_user = request.user

    # Ensure the user is logged in
    if not current_user.is_authenticated:
        return redirect('login')

    # Fetch the profile of the current user
    try:
        current_user_profile = Profile.objects.get(reg_id=current_user)
    except Profile.DoesNotExist:
        current_user_profile = None
    
    # Determine the opposite gender to filter
    opposite_gender = 'male' if current_user_profile and current_user_profile.gender == 'female' else 'female'

    # Fetch all users of the opposite gender except the currently logged-in user
    other_users = Register.objects.filter(profile__gender=opposite_gender).exclude(reg_id=current_user.reg_id)

    context = {
        'current_user': current_user,
        'other_users': other_users,
        'opposite_gender': opposite_gender,
    }
    return render(request, 'profile1.html', context)



def user_profile(request):
    email = request.session.get('user_email')
    if email:
        user = get_object_or_404(Register, email=email)
        return render(request, 'user_profile.html', {'user': user})
    else:
        return redirect('login')  # Redirect to login if user is not authenticated



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register

def block_user(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)
    user.block_user()
    messages.success(request, f"User {user.email} has been blocked.")
    return redirect('review_users')

def unblock_user(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)
    user.unblock_user()
    messages.success(request, f"User {user.email} has been unblocked.")
    return redirect('review_users')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile

def profile(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()
        
        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Create a new Profile or get the existing one
        profile, created = Profile.objects.get_or_create(reg_id=user)

        # Update the profile with POST data
        profile.address = request.POST.get('address')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.marital_status = request.POST.get('marital_status')
        profile.mother_tongue = request.POST.get('mother_tongue')
        profile.religion = request.POST.get('religion')
        profile.caste = request.POST.get('caste')
        profile.physical_status = request.POST.get('physical_status')
        profile.about = request.POST.get('about')
        profile.spoken_language = request.POST.get('spoken_language')
        profile.age = request.POST.get('age')
        profile.complexion = request.POST.get('complexion')
        profile.hobbies = request.POST.get('hobbies')
        profile.occupation = request.POST.get('occupation')
        profile.annual_income = request.POST.get('annual_income')
        profile.more_about_me = request.POST.get('more_about_me')
        profile.save()

        messages.success(request, "Profile added successfully.")
        return redirect('education')

    return render(request, 'profile.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile

def edit_personal_details(request):
    user_email = request.session.get('user_email')
    user = Register.objects.filter(email=user_email).first()
    
    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    profile, created = Profile.objects.get_or_create(reg_id=user)
    
    if request.method == 'POST':
        # Update the profile with POST data
        profile.address = request.POST.get('address')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.marital_status = request.POST.get('marital_status')
        profile.mother_tongue = request.POST.get('mother_tongue')
        profile.religion = request.POST.get('religion')
        profile.caste = request.POST.get('caste')
        profile.physical_status = request.POST.get('physical_status')
        profile.about = request.POST.get('about')
        profile.spoken_language = request.POST.get('spoken_language')
        profile.age = request.POST.get('age')
        profile.complexion = request.POST.get('complexion')
        profile.hobbies = request.POST.get('hobbies')
        profile.occupation = request.POST.get('occupation')
        profile.annual_income = request.POST.get('annual_income')
        profile.more_about_me = request.POST.get('more_about_me')
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'edit_personal_details.html', {'profile': profile})

def edit_profile(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')

        # Validate input fields
        if not first_name or not last_name or not phone_number or not gender or not dob:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'edit_profile.html', {'user': user})

        # Update the user profile
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.gender = gender
        user.dob = dob

        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user': user})


    
    # Render the profile template with user data
    return render(request, 'view_profile.html', {'user': user})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Education, Register

def education(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()

        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Check if an Education record exists
        education = Education.objects.filter(reg_id=user).first()

        if not education:
            # Create a new Education record if it doesn't exist
            education = Education(reg_id=user)

        # Update the Education record with the provided form data
        education.school_name = request.POST.get('school_name')
        education.school_passout_year = request.POST.get('school_passout_year')
        education.school_percentage = request.POST.get('school_percentage')
        education.plus_two_name = request.POST.get('plus_two_name')
        education.plus_two_passout_year = request.POST.get('plus_two_passout_year')
        education.plus_two_percentage = request.POST.get('plus_two_percentage')
        education.degree_institution_name = request.POST.get('degree_institution_name')
        education.degree_passout_year = request.POST.get('degree_passout_year')
        education.degree_percentage = request.POST.get('degree_percentage')
        education.degree_name = request.POST.get('degree_name')
        education.field_of_study = request.POST.get('field_of_study')
        education.save()

        messages.success(request, "Education details added successfully.")
        return redirect('family')  # Redirect to the next step or wherever you want the user to go next

    return render(request, 'education.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Education


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Education  # Import your models

def edit_education(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()

        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        education = Education.objects.filter(reg_id=user).first()

        if not education:
            education = Education(reg_id=user)

        education.school_name = request.POST.get('school_name')
        education.school_passout_year = request.POST.get('school_passout_year')
        education.school_percentage = request.POST.get('school_percentage')
        education.plus_two_name = request.POST.get('plus_two_name')
        education.plus_two_passout_year = request.POST.get('plus_two_passout_year')
        education.plus_two_percentage = request.POST.get('plus_two_percentage')
        education.degree_institution_name = request.POST.get('degree_institution_name')
        education.degree_passout_year = request.POST.get('degree_passout_year')
        education.degree_percentage = request.POST.get('degree_percentage')
        education.degree_name = request.POST.get('degree_name')
        education.field_of_study = request.POST.get('field_of_study')
        education.save()

        messages.success(request, "Education details updated successfully.")
        return redirect('edit_education')  # Update this to the correct redirect URL

    user_email = request.session.get('user_email')
    user = Register.objects.filter(email=user_email).first()
    education = Education.objects.filter(reg_id=user).first()

    return render(request, 'edit_education.html', {'education': education})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Family, Register


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Family, Register

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Family, Register

def family(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        if not user_email:
            messages.error(request, "User email not found in session.")
            return redirect('login')

        user = Register.objects.filter(email=user_email).first()
        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Extract form data
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation', '')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation', '')
        sibling_count = request.POST.get('sibling_count', '')
        sibling_details = request.POST.get('sibling_details', '')
        family_type = request.POST.get('family_type')
        family_status = request.POST.get('family_status')
        family_values = request.POST.get('family_values')
        native_place = request.POST.get('native_place', '')
        additional = request.POST.get('additional', '')

        # Validate required fields
        if not father_name or not mother_name or not family_type or not family_status or not family_values:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'family.html')

        # Create a new Family record
        Family.objects.create(
            reg_id=user,  # Assuming `reg_id` is a foreign key to the Register model
            father_name=father_name,
            father_occupation=father_occupation,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            sibling_count=int(sibling_count) if sibling_count.isdigit() else None,
            sibling_details=sibling_details,
            family_type=family_type,
            family_status=family_status,
            family_values=family_values,
            native_place=native_place,
            additional=additional
        )

        messages.success(request, "Family details added successfully.")
        return redirect('upload_images', reg_id=user.reg_id)  # Pass reg_id to the URL

    return render(request, 'family.html')

def edit_family(request):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, "User email not found in session.")
        return redirect('login')

    user = Register.objects.filter(email=user_email).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    try:
        family = Family.objects.get(reg_id=user)
    except Family.DoesNotExist:
        family = None

    if request.method == 'POST':
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation', '')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation', '')
        sibling_count = request.POST.get('sibling_count', '')
        sibling_details = request.POST.get('sibling_details', '')
        family_type = request.POST.get('family_type')
        family_status = request.POST.get('family_status')
        family_values = request.POST.get('family_values')
        native_place = request.POST.get('native_place', '')
        additional = request.POST.get('additional', '')

        if not father_name or not mother_name or not family_type or not family_status or not family_values:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'edit_family.html', {'family': family})

        if family:
            # Update existing family details
            family.father_name = father_name
            family.father_occupation = father_occupation
            family.mother_name = mother_name
            family.mother_occupation = mother_occupation
            family.sibling_count = int(sibling_count) if sibling_count.isdigit() else None
            family.sibling_details = sibling_details
            family.family_type = family_type
            family.family_status = family_status
            family.family_values = family_values
            family.nativeplace = native_place
            family.additional = additional
            family.save()
            messages.success(request, "Family details updated successfully.")
        else:
            # Create new family details
            Family.objects.create(
                reg_id=user,
                father_name=father_name,
                father_occupation=father_occupation,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                sibling_count=int(sibling_count) if sibling_count.isdigit() else None,
                sibling_details=sibling_details,
                family_type=family_type,
                family_status=family_status,
                family_values=family_values,
                nativeplace=native_place,
                additional=additional
            )
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .models import Register,Login,Blog,Notification
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Login

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile, Login,  ImageUpload
import re

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('index')

        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('index')

        user = Register(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            dob=dob,
            password=password,
            confirm_password=confirm_password,
            profile_picture=profile_picture
        )
        user.save()
        Login.objects.create(
            reg_id=user,
            email=email,
            password=password  # Store hashed password in practice
        )
        messages.success(request, "Registration successful.")
        return redirect('login')

    return render(request, 'index.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'admin@gmail.com' and password == 'admin123':
            request.session['is_admin'] = True
            return redirect('adminmain_view')

        user = Register.objects.filter(email=email).first()

        if user and user.check_password(password):
            if user.blocked:
                messages.error(request, "Your account has been blocked by the administrator.")
                return redirect('login')

            # Check if the user has completed their profile
            if check_profile_completion(user):
                messages.success(request, "Login successful.")
                request.session['user_email'] = email
                return redirect('profile1', reg_id=user.reg_id)  # Redirect to profile1 if profile is complete
            else:
                messages.success(request, "Login successful. Please complete your profile.")
                request.session['user_email'] = email
                return redirect('profile')  # Redirect to profile if not complete

        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Register

def profile_view(request, reg_id):
    current_user_email = request.session.get('user_email')

    if not current_user_email:
        return redirect('login')

    current_user = Register.objects.filter(email=current_user_email).first()
    
    if not current_user:
        return redirect('login')

    # Fetch the profile of the user specified by reg_id
    user_profile = get_object_or_404(Register, reg_id=reg_id)

    # Fetch other users based on gender and search query
    opposite_gender = 'male' if current_user.gender == 'female' else 'female'
    other_users = Register.objects.filter(gender=opposite_gender).exclude(email=current_user_email)

    # Handle search
    search_query = request.GET.get('query', '')  # Set default to empty string
    if search_query:
        other_users = other_users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    # Add request existence check
    for user in other_users:
        user.profile.request_exists = FriendRequest.objects.filter(sender=current_user, recipient=user).exists()

    context = {
        'current_user': current_user,
        'user_profile': user_profile,
        'other_users': other_users,
        'search_query': search_query,  # Ensure it's passed to the template
    }

    return render(request, 'profile1.html', context)



def view_profile1(request, personal_id):
    profile = get_object_or_404(Profile, personal_id=personal_id)
    education = Education.objects.filter(reg_id=profile.reg_id)
    family = Family.objects.filter(reg_id=profile.reg_id)
    images = ImageUpload.objects.filter(reg_id=profile.reg_id)  # Query for uploaded images

    context = {
        'profile': profile,
        'education': education,
        'family': family,
        'images': images,  # Add images to the context
    }

    return render(request, 'profile_detail.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Education, Family

def check_profile_completion(user):
    # Check if the user has completed their profile, education, and family details
    profile_completed = hasattr(user, 'profile') and user.profile is not None
    education_completed = Education.objects.filter(reg_id=user.reg_id).exists()
    family_completed = Family.objects.filter(reg_id=user.reg_id).exists()
    
    return profile_completed and education_completed and family_completed

from django.shortcuts import render

# views.py
from django.shortcuts import render
from .models import Register, Profile

def view_profiles(request):
    current_user = request.user

    # Ensure the user is logged in
    if not current_user.is_authenticated:
        return redirect('login')

    # Fetch the profile of the current user
    try:
        current_user_profile = Profile.objects.get(reg_id=current_user)
    except Profile.DoesNotExist:
        current_user_profile = None
    
    # Determine the opposite gender to filter
    opposite_gender = 'male' if current_user_profile and current_user_profile.gender == 'female' else 'female'

    # Fetch all users of the opposite gender except the currently logged-in user
    other_users = Register.objects.filter(profile__gender=opposite_gender).exclude(reg_id=current_user.reg_id)

    context = {
        'current_user': current_user,
        'other_users': other_users,
        'opposite_gender': opposite_gender,
    }
    return render(request, 'profile1.html', context)



def user_profile(request):
    email = request.session.get('user_email')
    if email:
        user = get_object_or_404(Register, email=email)
        return render(request, 'user_profile.html', {'user': user})
    else:
        return redirect('login')  # Redirect to login if user is not authenticated



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register

def block_user(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)
    user.block_user()
    messages.success(request, f"User {user.email} has been blocked.")
    return redirect('review_users')

def unblock_user(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)
    user.unblock_user()
    messages.success(request, f"User {user.email} has been unblocked.")
    return redirect('review_users')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile

def profile(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()
        
        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Create a new Profile or get the existing one
        profile, created = Profile.objects.get_or_create(reg_id=user)

        # Update the profile with POST data
        profile.address = request.POST.get('address')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.marital_status = request.POST.get('marital_status')
        profile.mother_tongue = request.POST.get('mother_tongue')
        profile.religion = request.POST.get('religion')
        profile.caste = request.POST.get('caste')
        profile.physical_status = request.POST.get('physical_status')
        profile.about = request.POST.get('about')
        profile.spoken_language = request.POST.get('spoken_language')
        profile.age = request.POST.get('age')
        profile.complexion = request.POST.get('complexion')
        profile.hobbies = request.POST.get('hobbies')
        profile.occupation = request.POST.get('occupation')
        profile.annual_income = request.POST.get('annual_income')
        profile.more_about_me = request.POST.get('more_about_me')
        profile.save()

        messages.success(request, "Profile added successfully.")
        return redirect('education')

    return render(request, 'profile.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Profile

def edit_personal_details(request):
    user_email = request.session.get('user_email')
    user = Register.objects.filter(email=user_email).first()
    
    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    profile, created = Profile.objects.get_or_create(reg_id=user)
    
    if request.method == 'POST':
        # Update the profile with POST data
        profile.address = request.POST.get('address')
        profile.height = request.POST.get('height')
        profile.weight = request.POST.get('weight')
        profile.marital_status = request.POST.get('marital_status')
        profile.mother_tongue = request.POST.get('mother_tongue')
        profile.religion = request.POST.get('religion')
        profile.caste = request.POST.get('caste')
        profile.physical_status = request.POST.get('physical_status')
        profile.about = request.POST.get('about')
        profile.spoken_language = request.POST.get('spoken_language')
        profile.age = request.POST.get('age')
        profile.complexion = request.POST.get('complexion')
        profile.hobbies = request.POST.get('hobbies')
        profile.occupation = request.POST.get('occupation')
        profile.annual_income = request.POST.get('annual_income')
        profile.more_about_me = request.POST.get('more_about_me')
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'edit_personal_details.html', {'profile': profile})

def edit_profile(request, reg_id):
    user = get_object_or_404(Register, reg_id=reg_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')

        # Validate input fields
        if not first_name or not last_name or not phone_number or not gender or not dob:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'edit_profile.html', {'user': user})

        # Update the user profile
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.gender = gender
        user.dob = dob

        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('view_all_details', personal_id=user.reg_id)

    return render(request, 'edit_profile.html', {'user': user})


    
    # Render the profile template with user data
    return render(request, 'view_profile.html', {'user': user})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Education, Register

def education(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()

        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Check if an Education record exists
        education = Education.objects.filter(reg_id=user).first()

        if not education:
            # Create a new Education record if it doesn't exist
            education = Education(reg_id=user)

        # Update the Education record with the provided form data
        education.school_name = request.POST.get('school_name')
        education.school_passout_year = request.POST.get('school_passout_year')
        education.school_percentage = request.POST.get('school_percentage')
        education.plus_two_name = request.POST.get('plus_two_name')
        education.plus_two_passout_year = request.POST.get('plus_two_passout_year')
        education.plus_two_percentage = request.POST.get('plus_two_percentage')
        education.degree_institution_name = request.POST.get('degree_institution_name')
        education.degree_passout_year = request.POST.get('degree_passout_year')
        education.degree_percentage = request.POST.get('degree_percentage')
        education.degree_name = request.POST.get('degree_name')
        education.field_of_study = request.POST.get('field_of_study')
        education.save()

        messages.success(request, "Education details added successfully.")
        return redirect('family')  # Redirect to the next step or wherever you want the user to go next

    return render(request, 'education.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Education


# matrimonypro/matrimonyapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Education

def edit_education(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        user = Register.objects.filter(email=user_email).first()

        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        education = Education.objects.filter(reg_id=user).first()

        if not education:
            education = Education(reg_id=user)

        # Update education fields from the POST request
        education.school_name = request.POST.get('school_name')
        education.school_passout_year = request.POST.get('school_passout_year')
        education.school_percentage = request.POST.get('school_percentage')
        education.plus_two_name = request.POST.get('plus_two_name')
        education.plus_two_passout_year = request.POST.get('plus_two_passout_year')
        education.plus_two_percentage = request.POST.get('plus_two_percentage')
        education.degree_institution_name = request.POST.get('degree_institution_name')
        education.degree_passout_year = request.POST.get('degree_passout_year')
        education.degree_percentage = request.POST.get('degree_percentage')
        education.degree_name = request.POST.get('degree_name')
        education.field_of_study = request.POST.get('field_of_study')
        education.save()

        messages.success(request, "Education details updated successfully.")

        # Use the user's ID or another unique identifier for the redirect
        return redirect('view_all_details', personal_id=user.reg_id)  # Assuming 'id' is the identifier

    user_email = request.session.get('user_email')
    user = Register.objects.filter(email=user_email).first()
    education = Education.objects.filter(reg_id=user).first()

    return render(request, 'edit_education.html', {'education': education})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Family, Register


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Family, Register

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Family, Register

def family(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')
        if not user_email:
            messages.error(request, "User email not found in session.")
            return redirect('login')

        user = Register.objects.filter(email=user_email).first()
        if not user:
            messages.error(request, "User not found.")
            return redirect('login')

        # Extract form data
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation', '')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation', '')
        sibling_count = request.POST.get('sibling_count', '')
        sibling_details = request.POST.get('sibling_details', '')
        family_type = request.POST.get('family_type')
        family_status = request.POST.get('family_status')
        family_values = request.POST.get('family_values')
        native_place = request.POST.get('native_place', '')
        additional = request.POST.get('additional', '')

        # Validate required fields
        if not father_name or not mother_name or not family_type or not family_status or not family_values:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'family.html')

        # Create a new Family record
        Family.objects.create(
            reg_id=user,  # Assuming `reg_id` is a foreign key to the Register model
            father_name=father_name,
            father_occupation=father_occupation,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            sibling_count=int(sibling_count) if sibling_count.isdigit() else None,
            sibling_details=sibling_details,
            family_type=family_type,
            family_status=family_status,
            family_values=family_values,
            native_place=native_place,
            additional=additional
        )

        messages.success(request, "Family details added successfully.")
        return redirect('upload_images', reg_id=user.reg_id)  # Pass reg_id to the URL

    return render(request, 'family.html')

def edit_family(request):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, "User email not found in session.")
        return redirect('login')

    user = Register.objects.filter(email=user_email).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    try:
        family = Family.objects.get(reg_id=user)
    except Family.DoesNotExist:
        family = None

    if request.method == 'POST':
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation', '')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation', '')
        sibling_count = request.POST.get('sibling_count', '')
        sibling_details = request.POST.get('sibling_details', '')
        family_type = request.POST.get('family_type')
        family_status = request.POST.get('family_status')
        family_values = request.POST.get('family_values')
        native_place = request.POST.get('native_place', '')
        additional = request.POST.get('additional', '')

        if not father_name or not mother_name or not family_type or not family_status or not family_values:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'edit_family.html', {'family': family})

        if family:
            # Update existing family details
            family.father_name = father_name
            family.father_occupation = father_occupation
            family.mother_name = mother_name
            family.mother_occupation = mother_occupation
            family.sibling_count = int(sibling_count) if sibling_count.isdigit() else None
            family.sibling_details = sibling_details
            family.family_type = family_type
            family.family_status = family_status
            family.family_values = family_values
            family.nativeplace = native_place
            family.additional = additional
            family.save()
            messages.success(request, "Family details updated successfully.")
        else:
            # Create new family details
            Family.objects.create(
                reg_id=user,
                father_name=father_name,
                father_occupation=father_occupation,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                sibling_count=int(sibling_count) if sibling_count.isdigit() else None,
                sibling_details=sibling_details,
                family_type=family_type,
                family_status=family_status,
                family_values=family_values,
                nativeplace=native_place,
                additional=additional
            )
            messages.success(request, "Family details added successfully.")

        return redirect('view_all_details', personal_id=user.reg_id) # Redirect to the family detail page or another page after saving

    return render(request, 'edit_family.html', {'family': family})

# matrimonypro/matrimonyapp/views.py
from django.shortcuts import render, redirect
# matrimonypro/matrimonyapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Register, Profile, Education, Family,ImageUpload
from django.utils import timezone
from datetime import timedelta

def view_all_details(request, personal_id):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, "User email not found in session.")
        return redirect('login')

    user = Register.objects.filter(email=user_email).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    profile = Profile.objects.filter(reg_id=user).first()
    education = Education.objects.filter(reg_id=user).first()
    family = Family.objects.filter(reg_id=user).first()


    # Fetch the user's uploaded images
    images = ImageUpload.objects.filter(reg_id=user).order_by('-uploaded_at')

    # Separate newly uploaded images and previously uploaded images
    newly_uploaded_images = images.filter(uploaded_at__gte=timezone.now() - timedelta(days=1))
    previously_uploaded_images = images.exclude(uploaded_at__gte=timezone.now() - timedelta(days=1))

    context = {
        'user': user,
        'profile': profile,
        'education': education,
        'family': family,
        'newly_uploaded_images': newly_uploaded_images,
        'previously_uploaded_images': previously_uploaded_images,
    }

    return render(request, 'view_all_details.html', context)
# matrimonypro/matrimonyapp/views.py

# matrimonypro/matrimonyapp/views.py
# matrimonypro/matrimonyapp/views.py

# matrimonypro/matrimonyapp/views.py

# matrimonypro/matrimonyapp/views.py

from django.shortcuts import render, get_object_or_404
from .models import Register, FriendRequest

def view_received_requests(request, personal_id):
    # Get the user by personal_id
    user = get_object_or_404(Register, profile__personal_id=personal_id)  # Assuming you have a relationship with Profile
    
    # Fetch pending friend requests for the user
    received_requests = FriendRequest.objects.filter(recipient=user, status='pending')

    context = {
        'received_requests': received_requests,
        'user': user,
    }
    return render(request, 'view_received_requests.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from .models import Package

# View for listing all packages
def view_packages(request):
    packages = Package.objects.all()
    return render(request, 'view_packages.html', {'packages': packages})

def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == 'POST':
        package.name = request.POST.get('name')
        package.description = request.POST.get('description')
        package.price = request.POST.get('price')
        package.duration_days = request.POST.get('duration_days')
        package.save()
        return redirect('view_packages')
    return render(request, 'edit_package.html', {'package': package})

# View for creating a new package
def package_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration_days = request.POST.get('duration_days')

        # Validate and create the package
        if name and description and price and duration_days:
            Package.objects.create(
                name=name,
                description=description,
                price=price,
                duration_days=duration_days
            )
            return redirect('view_packages')
        else:
            error_message = "All fields are required."
            return render(request, 'package_create.html', {'error_message': error_message})
    
    return render(request, 'package_create.html')

# View for deleting a package
def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == 'POST':
        package.delete()
        return redirect('view_packages')
    return render(request, 'delete_package.html', {'package': package})





def package_view(request):
    packages = Package.objects.all()
    return render(request, 'package.html', {'packages': packages})




def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Register.objects.get(email=email)
            user.generate_reset_token()

            current_site = get_current_site(request)
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.reg_id)),
                'token': user.reset_password_token,
            })
            send_mail(subject, message, 'noreply@yourdomain.com', [user.email])

            return HttpResponse('Password reset link has been sent to your email.')
        except Register.DoesNotExist:
            return HttpResponse('Email not found', status=404)
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Register.objects.get(reg_id=uid, reset_password_token=token, token_expiry__gte=timezone.now())
    except (TypeError, ValueError, OverflowError, Register.DoesNotExist):
        return HttpResponse('Invalid or expired reset link', status=400)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user.password = new_password  # Update plain text password
            user.reset_password_token = ''
            user.token_expiry = None
            user.save()

            try:
                login_record = Login.objects.get(reg_id=user)
                login_record.password = new_password  # Update plain text password
                login_record.save()
            except Login.DoesNotExist:
                return HttpResponse('Login record not found', status=404)

            return redirect('login')
        else:
            return HttpResponse('Passwords do not match', status=400)

    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})





def adminmain_view(request):
    if request.session.get('is_admin'):
        return render(request, 'adminmain.html')
    else:
        return redirect('login')
def logout(request):
    if 'is_admin' in request.session:
        del request.session['is_admin']
    return redirect('login')
def review_users(request):
    
    # Fetch all registered users
    users = Register.objects.all()
    # Pass the users to the template
    return render(request, 'review_users.html', {'users': users})
from django.shortcuts import get_object_or_404, redirect
def delete_user(request, reg_id):
    # Retrieve the user from the Register table
    user = get_object_or_404(Register, reg_id=reg_id)
    
    try:
        # Delete associated Login records
        Login.objects.filter(reg_id=user).delete()
        # Delete the user from the Register table
        user.delete()
        messages.success(request, 'User has been deleted successfully.')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
    
    # Redirect to the review users page
    return redirect('review_users')


from django.shortcuts import render, redirect
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.shortcuts import render, redirect

def blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Ensure that required fields are provided
        if title and content:
            # Create a new Blog instance and save it
            blog = Blog(title=title, content=content, image=image)
            blog.save()  # Save the blog post to the database

            return redirect('blog_create')  # Redirect to the same page to display updated list

    # Fetch existing blogs to display
    blogs = Blog.objects.all()

    return render(request, 'blog_create.html', {'blogs': blogs})

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)  # Ensure you're using the correct model and ID field

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Ensure that required fields are provided
        if title and content:
            blog.title = title
            blog.content = content
            if image:
                blog.image = image
            blog.save()  # Save the updated blog post to the database

            return redirect('blog_create')  # Redirect to the list of blog posts

    # Render the edit form with the current blog details
    return render(request, 'edit_blog.html', {'blog': blog})

def delete_blog(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, blog_id=blog_id)  # Use blog_id instead of id
        blog.delete()
        return redirect('blog_create')
def create_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')

        if title and message:  # Basic validation
            try:
                # Create a notification for all users or use specific logic
                Notification.objects.create(
                    title=title,
                    message=message
                )
                # Redirect to a confirmation page or notification list
                return redirect('create_notification')  # Adjust the redirect as needed
            except Exception as e:
                return HttpResponse(f"Error: {e}", status=400)
        else:
            return HttpResponse("Invalid input", status=400)
    notifications = Notification.objects.all().order_by('-date_created')
    
    return render(request, 'create_notification.html', {'notifications': notifications})

def delete_notification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, notification_id=notification_id)
        try:
            notification.delete()
            return redirect('create_notification')  # Redirect back to the notifications list
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=400)
    else:
        return HttpResponse("Invalid request method", status=405)

def home(request):
    return render(request, 'home.html')






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, ImageUpload
import os
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, ImageUpload
from django.conf import settings

def upload_more_image(request):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, "User email not found in session.")
        return redirect('login')

    user = Register.objects.filter(email=user_email).first()
    
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('images')  # Get list of uploaded files

        for file in uploaded_files:
            # Create an instance of ImageUpload
            image_upload = ImageUpload(reg_id=user)
            # Save the original image directly, bypassing compression
            image_upload.image.save(file.name, file)
            image_upload.save()  # Save the instance to the database

        messages.success(request, "Images uploaded successfully without compression.")
        return redirect('view_all_details', personal_id=user.reg_id)  # Redirect to the details page

    return render(request, 'upload_more_image.html', {'user': user})


# matrimonypro/matrimonyapp/views.py


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Package, Payment, Register  # Ensure Register is imported

def payment_page(request, package_id):
    if request.method == "GET":
        # Retrieve the package and its price
        package = get_object_or_404(Package, id=package_id)
        order_amount = int(package.price * 100)  # Convert to paise (integer)
        order_currency = 'INR'
        order_receipt = f'order_rcptid_{package_id}'
        
        # Setup Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        # Create an order
        order = client.order.create({
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'payment_capture': '1'
        })

        context = {
            'order_id': order['id'],
            'amount': order_amount,
            'currency': order_currency,
            'api_key': settings.RAZORPAY_API_KEY
        }
        return render(request, 'payment_page.html', context)

import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Package, Payment, Register  # Ensure Register is imported

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Check for missing parameters
        if not payment_id or not order_id or not signature:
            return JsonResponse({'status': 'failed', 'message': 'Missing payment parameters'})

        # Setup Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Extract package_id from order_id
            package_id = int(order_id.split('_')[1])
            package = get_object_or_404(Package, id=package_id)

            if request.user.is_authenticated:
                user = get_object_or_404(Register, reg_id=request.user.reg_id)

                # Create and save payment record
                payment = Payment(
                    reg_id=user,
                    amount=package.price,
                    currency='INR',
                    payment_id=payment_id,
                    payment_status='success',
                    order_id=order_id
                )
                payment.save()

                return JsonResponse({'status': 'success', 'message': 'Payment was successful!'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'User not authenticated'})
        except Exception as e:
            print(f"Error occurred during payment processing: {e}")  # Log the error for debugging
            return JsonResponse({'status': 'failed', 'message': 'Payment verification failed.'})

    return JsonResponse({'status': 'failed', 'message': 'Invalid request'})


from django.shortcuts import render
from .models import Notification  # Make sure Notification model is imported

def view_notifications(request):
    notifications = Notification.objects.all().order_by('-date_created')  # Adjust date field if different
    return render(request, 'notifications.html', {'notifications': notifications})

from django.shortcuts import render, redirect
from .models import Blog



def blog_list(request):
    # Fetch all blogs to display
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def search_profiles(request):
    current_user_email = request.session.get('user_email')

    if not current_user_email:
        return redirect('login')

    current_user = Register.objects.filter(email=current_user_email).first()

    if not current_user:
        return redirect('login')

    # Handle search
    search_query = request.GET.get('query', '')
    opposite_gender = 'male' if current_user.gender == 'female' else 'female'
    other_users = Register.objects.filter(gender=opposite_gender).exclude(email=current_user_email)

    if search_query:
        other_users = other_users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    context = {
        'current_user': current_user,
        'other_users': other_users,
        'query': search_query,  # Pass the search query to display in the template
    }

    return render(request, 'search_results.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Register, Profile, FriendRequest

def send_request(request, personal_id):
    if request.method == 'POST':
        sender_email = request.session.get('user_email')
        if not sender_email:
            messages.error(request, "You must be logged in to send a request.")
            return redirect('login')

        sender = Register.objects.filter(email=sender_email).first()
        if not sender:
            messages.error(request, "Sender not found.")
            return redirect('login')

        recipient_profile = get_object_or_404(Profile, personal_id=personal_id)
        recipient = recipient_profile.reg_id

        # Check if a request already exists
        existing_request = FriendRequest.objects.filter(sender=sender, recipient=recipient).first()
        if existing_request:
            messages.info(request, "A request has already been sent to this user.")
        else:
            # Create a new friend request with status set to 'pending'
            FriendRequest.objects.create(sender=sender, recipient=recipient, status='pending')
            messages.success(request, "Friend request sent successfully.")

    return redirect('profile1', reg_id=recipient.reg_id)


def view_sent_requests(request):
    sender_email = request.session.get('user_email')
    if not sender_email:
        messages.error(request, "You must be logged in to view sent requests.")
        return redirect('login')

    sender = Register.objects.filter(email=sender_email).first()
    if not sender:
        messages.error(request, "User not found.")
        return redirect('login')

    sent_requests = FriendRequest.objects.filter(sender=sender)

    context = {
        'sent_requests': sent_requests,
    }

    return render(request, 'view_sent_requests.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, FriendRequest

def view_received_requests(request):
    user_email = request.session.get('user_email')
    if not user_email:
        messages.error(request, "You must be logged in to view received requests.")
        return redirect('login')

    # Get the logged-in user
    user = Register.objects.filter(email=user_email).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('login')

    # Query to get all received friend requests for this user
    received_requests = FriendRequest.objects.filter(recipient=user)

    context = {
        'received_requests': received_requests,
    }

    return render(request, 'view_received_requests.html', context)

from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import FriendRequest

def accept_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.status = 'accepted'
    friend_request.save()
    messages.success(request, "Friend request accepted.")
    return redirect('view_received_requests')

def reject_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.status = 'rejected'
    friend_request.save()
    messages.success(request, "Friend request rejected.")
    return redirect('view_received_requests')

from django.shortcuts import render, redirect
from .models import MatchPreference, Profile

def add_match_preferences(request):
    if request.method == 'POST':
        # Extract match preferences data from POST request
        min_age = int(request.POST.get('min_age'))
        max_age = int(request.POST.get('max_age'))
        preferred_height = request.POST.get('preferred_height')
        preferred_religion = request.POST.get('preferred_religion')
        preferred_caste = request.POST.get('preferred_caste')
        preferred_education = request.POST.get('preferred_education')
        preferred_occupation = request.POST.get('preferred_occupation')
        preferred_location = request.POST.get('preferred_location')
        preferred_income = request.POST.get('preferred_income')
        preferred_family_type = request.POST.get('preferred_family_type')
        preferred_physical_status = request.POST.get('preferred_physical_status')

        # Save or update the user's match preferences
        match_preferences, created = MatchPreference.objects.get_or_create(user=request.user)
        match_preferences.min_age = min_age
        match_preferences.max_age = max_age
        match_preferences.preferred_height = preferred_height
        match_preferences.preferred_religion = preferred_religion
        match_preferences.preferred_caste = preferred_caste
        match_preferences.preferred_education = preferred_education
        match_preferences.preferred_occupation = preferred_occupation
        match_preferences.preferred_location = preferred_location
        match_preferences.preferred_income = preferred_income
        match_preferences.preferred_family_type = preferred_family_type
        match_preferences.preferred_physical_status = preferred_physical_status
        match_preferences.save()

        # Get all profiles and calculate their match score
        profiles = Profile.objects.all()
        matching_profiles = []

        for profile in profiles:
            score = 0

            # Check age match
            if min_age <= profile.age <= max_age:
                score += 20  # Award points for age match

            # Check height match (a simple example; you can adjust this logic)
            if preferred_height and preferred_height in profile.height:
                score += 10  # Award points for height match

            # Check religion match
            if preferred_religion and preferred_religion.lower() == profile.religion.lower():
                score += 10  # Award points for religion match

            # Check caste match
            if preferred_caste and preferred_caste.lower() == profile.caste.lower():
                score += 10  # Award points for caste match

            # Check education match
            if preferred_education and preferred_education.lower() == profile.education.lower():
                score += 10  # Award points for education match

            # Check occupation match
            if preferred_occupation and preferred_occupation.lower() == profile.occupation.lower():
                score += 10  # Award points for occupation match

            # Check location match
            if preferred_location and preferred_location.lower() in profile.location.lower():
                score += 10  # Award points for location match

            # Check income match (assuming it's a number, we can convert it)
            if preferred_income and preferred_income == profile.income:
                score += 10  # Award points for income match

            # Check family type match
            if preferred_family_type and preferred_family_type.lower() == profile.family_type.lower():
                score += 10  # Award points for family type match

            # Check physical status match
            if preferred_physical_status and preferred_physical_status.lower() == profile.physical_status.lower():
                score += 10  # Award points for physical status match

            # Only consider profiles with a score greater than 0
            if score > 0:
                matching_profiles.append((profile, score))

        # Sort profiles based on the score in descending order
        matching_profiles.sort(key=lambda x: x[1], reverse=True)

        # Render the page with the matching profiles
        return render(request, 'matching_profiles.html', {'matching_profiles': matching_profiles})

    return render(request, 'add_match_preferences.html')

