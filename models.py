from django.db import models
import random
from datetime import date

class UserProfile(models.Model):
    # Gender choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not', 'Prefer not to say'),
    ]
    
    # Blood group choices
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('unknown', 'Unknown'),
    ]

    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='prefer_not'
    )
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    connect_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    weight = models.PositiveSmallIntegerField(
        null=True, 
        blank=True, 
        help_text="Weight in kg"
    )
    mother_tongue = models.CharField(max_length=50, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=7,
        choices=BLOOD_GROUP_CHOICES,
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.connect_id:
            random_num = random.randint(10000, 99999)
            self.connect_id = f"CONNECTID{random_num}"
        super().save(*args, **kwargs)
        
    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

# Keep your existing Profile model as is

class Profile(models.Model):
    # Profile fields
    HEIGHT_CHOICES = [
        (140, '140 cm'), (145, '145 cm'), (150, '150 cm'), (155, '155 cm'),
        (160, '160 cm'), (165, '165 cm'), (170, '170 cm'), (175, '175 cm'),
        (180, '180 cm'), (185, '185 cm'), (190, '190 cm'), (195, '195 cm'),
        (200, '200 cm'),
    ]
    
    COMPLEXION_CHOICES = [
        ('very_fair', 'Very Fair'), ('fair', 'Fair'), 
        ('moderate_fair', 'Moderate Fair'), ('medium', 'Medium'),
        ('dark', 'Dark'), ('prefer_not', 'Prefer not to say'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('slim', 'Slim'), ('average', 'Average'), ('heavy', 'Heavy'),
    ]
    
    PHYSICAL_STATUS_CHOICES = [
        ('normal', 'Normal'), ('differently_abled', 'Differently Abled'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('unmarried', 'Unmarried'), ('widowed', 'Widowed'), 
        ('divorcee', 'Divorcee'),
    ]
    
    FAMILY_STATUS_CHOICES = [
        ('lower_middle', 'Lower Middle Class'), ('middle', 'Middle Class'),
        ('upper_middle', 'Upper Middle Class'), ('rich', 'Rich'),
    ]
    
    DENOMINATION_CHOICES = [
        ('syrian', 'Syrian Catholic'), ('latin', 'Latin Catholic'),
        ('malankara', 'Malankara'), ('orthodox', 'Orthodox'),
        ('jacobite', 'Jacobite'), ('marthoma', 'Marthoma'), ('csi', 'CSI'),
    ]
    
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile')
    height = models.PositiveSmallIntegerField(choices=HEIGHT_CHOICES, null=True, blank=True)
    complexion = models.CharField(max_length=20, choices=COMPLEXION_CHOICES, null=True, blank=True)
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, null=True, blank=True)
    physical_status = models.CharField(max_length=20, choices=PHYSICAL_STATUS_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    family_status = models.CharField(max_length=15, choices=FAMILY_STATUS_CHOICES, null=True, blank=True)
    denomination = models.CharField(max_length=20, choices=DENOMINATION_CHOICES, null=True, blank=True)
    parish_name = models.CharField(max_length=100, null=True, blank=True)
    parish_place = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Profile for {self.user.full_name}"
    
class EducationProfessional(models.Model):
    # Education Level Choices
    EDUCATION_LEVELS = [
        ('high_school', 'High School'),
        ('diploma', 'Diploma'),
        ('bachelors', "Bachelor's Degree"),
        ('masters', "Master's Degree"),
        ('phd', 'PhD/Doctorate'),
        ('other', 'Other'),
    ]
    
    # Bachelor's Degree Choices
    BACHELORS_DEGREES = [
        ('ba', 'BA (Bachelor of Arts)'),
        ('bsc', 'BSc (Bachelor of Science)'),
        ('bcom', 'BCom (Bachelor of Commerce)'),
        ('btech', 'BTech (Bachelor of Technology)'),
        ('bca', 'BCA (Bachelor of Computer Applications)'),
    ]
    
    # Master's Degree Choices
    MASTERS_DEGREES = [
        ('ma', 'MA (Master of Arts)'),
        ('msc', 'MSc (Master of Science)'),
        ('mcom', 'MCom (Master of Commerce)'),
        ('mtech', 'MTech (Master of Technology)'),
        ('mba', 'MBA (Master of Business Administration)'),
    ]
    
    # Occupation Choices
    OCCUPATION_CHOICES = [
        ('business', 'Business'),
        ('professional', 'Professional'),
        ('government', 'Government Service'),
        ('private', 'Private Sector'),
        ('self_employed', 'Self Employed'),
        ('retired', 'Retired'),
        ('student', 'Student'),
        ('not_working', 'Not Working'),
    ]
    
    # Employment Type Choices
    EMPLOYMENT_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('unemployed', 'Unemployed'),
    ]
    
    # Income Range Choices
    INCOME_CHOICES = [
        ('0-25000', '0 - 25,000'),
        ('25001-50000', '25,001 - 50,000'),
        ('50001-75000', '50,001 - 75,000'),
        ('75001-100000', '75,001 - 100,000'),
        ('100001-150000', '100,001 - 150,000'),
        ('150001+', '150,001+'),
        ('not_disclosed', 'Prefer not to disclose'),
    ]
    
    # Main Fields
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='education_professional')
    
    # Education Information
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    bachelors_degree = models.CharField(max_length=20, choices=BACHELORS_DEGREES, blank=True, null=True)
    bachelors_specialization = models.CharField(max_length=100, blank=True, null=True)
    bachelors_institution = models.CharField(max_length=150, blank=True, null=True)
    masters_degree = models.CharField(max_length=20, choices=MASTERS_DEGREES, blank=True, null=True)
    masters_specialization = models.CharField(max_length=100, blank=True, null=True)
    masters_institution = models.CharField(max_length=150, blank=True, null=True)
    phd_field = models.CharField(max_length=100, blank=True, null=True)
    phd_institution = models.CharField(max_length=150, blank=True, null=True)
    other_education = models.CharField(max_length=200, blank=True, null=True)
    
    # Professional Information
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    working_country = models.CharField(max_length=50)
    working_state = models.CharField(max_length=50)
    working_district = models.CharField(max_length=50)
    working_city = models.CharField(max_length=50)
    annual_income = models.CharField(max_length=20, choices=INCOME_CHOICES)
    
    def __str__(self):
        return f"Education & Professional Info - {self.user.full_name}"
    
class AdditionalProfile(models.Model):
    # Native Location Choices
    COUNTRY_CHOICES = [
        ('IN', 'India'),
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('AE', 'United Arab Emirates'),
        ('SA', 'Saudi Arabia'),
        ('SG', 'Singapore'),
        ('MY', 'Malaysia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('JP', 'Japan'),
        ('other', 'Other'),
    ]
    
    # Phone Code Choices
    PHONE_CODE_CHOICES = [
        ('+91', 'India (+91)'),
        ('+1', 'USA/Canada (+1)'),
        ('+44', 'UK (+44)'),
        ('+61', 'Australia (+61)'),
        ('+971', 'UAE (+971)'),
        ('+966', 'Saudi (+966)'),
        ('+65', 'Singapore (+65)'),
        ('+60', 'Malaysia (+60)'),
        ('+49', 'Germany (+49)'),
        ('+33', 'France (+33)'),
        ('+81', 'Japan (+81)'),
    ]
    
    ADDRESS_TYPE_CHOICES = [
        ('same', 'Same as Communication Address'),
        ('different', 'Different Address'),
    ]
    
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='additional_profile')
    
    # Native Location Information
    native_country = models.CharField(max_length=5, choices=COUNTRY_CHOICES)
    native_state = models.CharField(max_length=100, blank=True, null=True)
    native_city = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact Information
    whatsapp_code = models.CharField(max_length=5, choices=PHONE_CODE_CHOICES, default='+91')
    whatsapp_number = models.CharField(max_length=15)
    mobile_code = models.CharField(max_length=5, choices=PHONE_CODE_CHOICES, default='+91')
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=20)
    secondary_mobile_code = models.CharField(max_length=5, choices=PHONE_CODE_CHOICES, default='+91')

    secondary_mobile = models.CharField(max_length=15, blank=True, null=True)
    landline_number = models.CharField(max_length=15, blank=True, null=True)
    alternate_email = models.EmailField(blank=True, null=True)
    preferred_contact_time = models.CharField(max_length=50, blank=True, null=True)
    
    # Present address fields
    present_address_type = models.CharField(
        max_length=10, 
        choices=ADDRESS_TYPE_CHOICES, 
        default='same'
    )
    present_address = models.TextField(blank=True)
    present_pincode = models.CharField(max_length=10, blank=True)
    
    # Permanent address fields
    permanent_address_type = models.CharField(
        max_length=10, 
        choices=ADDRESS_TYPE_CHOICES, 
        default='same'
    )
    permanent_address = models.TextField(blank=True)
    permanent_pincode = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return f"Additional Profile - {self.user.full_name}"
from django.db import models
from .models import UserProfile  # Assuming UserProfile is in the same app

class ProfileCreationDetails(models.Model):
    CREATED_BY_CHOICES = [
        ('brother', 'Brother'),
        ('candidate', 'Candidate'),
        ('father', 'Father'),
        ('friend', 'Friend'),
        ('mother', 'Mother'),
        ('relative', 'Relative'),
        ('sister', 'Sister'),
    ]
    
    HEAR_ABOUT_CHOICES = [
        ('friend', 'Friend/Family'),
        ('social-media', 'Social Media'),
        ('newspaper', 'Newspaper'),
        ('tv', 'TV Advertisement'),
        ('search-engine', 'Search Engine'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='creation_details')
    created_by = models.CharField(max_length=20, choices=CREATED_BY_CHOICES)
    creator_name = models.CharField(max_length=100)
    hear_about = models.CharField(max_length=20, choices=HEAR_ABOUT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Creation details for {self.user.full_name}"


from django.db import models
from django.utils import timezone

class SuccessStory(models.Model):
    brides_name = models.CharField(max_length=100)
    grooms_name = models.CharField(max_length=100)
    wedding_date = models.DateField()
    contact_number = models.CharField(max_length=20)
    story = models.TextField()
    cover_photo = models.ImageField(upload_to='uploads/')  # Changed to single folder
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.brides_name} & {self.grooms_name}'s Wedding Story"

class AdditionalPhoto(models.Model):
    success_story = models.ForeignKey(SuccessStory, related_name='additional_photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads/')  # Changed to same folder
    uploaded_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from .models import UserProfile  # Assuming UserProfile is in the same app

class Family(models.Model):
    # Family Status Choices
    FAMILY_STATUS_CHOICES = [
        ('lower_middle', 'Lower Middle Class'),
        ('middle', 'Middle Class'),
        ('upper_middle', 'Upper Middle Class'),
        ('rich', 'Rich'),
        ('affluent', 'Affluent'),
    ]
    
    # Occupation Choices (can be shared with other models)
    OCCUPATION_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('business', 'Business'),
        ('professional', 'Professional'),
        ('government', 'Government Service'),
        ('private', 'Private Sector'),
        ('retired', 'Retired'),
        ('homemaker', 'Homemaker'),
        ('expired', 'Expired'),
    ]
    
    # Religious Status Choices
    RELIGIOUS_STATUS_CHOICES = [
        ('married', 'Married'),
        ('unmarried', 'Unmarried'),
        ('priest', 'Priest'),
        ('nun', 'Nun'),
        ('candidate', 'Religious Candidate'),
    ]

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='family')
    
    # Family Status
    family_status = models.CharField(
        max_length=20, 
        choices=FAMILY_STATUS_CHOICES,
        blank=True,
        null=True
    )
    
    # Father's Information
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_housename = models.CharField(max_length=100, blank=True, null=True)
    father_native_place = models.CharField(max_length=100, blank=True, null=True)
    father_occupation = models.CharField(
        max_length=20, 
        choices=OCCUPATION_CHOICES,
        blank=True,
        null=True
    )
    
    # Mother's Information
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_housename = models.CharField(max_length=100, blank=True, null=True)
    mother_native_place = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(
        max_length=20, 
        choices=OCCUPATION_CHOICES,
        blank=True,
        null=True
    )
    
    # Brothers Information
    no_of_brothers = models.PositiveIntegerField(default=0)
    no_of_brothers_married = models.PositiveIntegerField(default=0)
    no_of_brothers_unmarried = models.PositiveIntegerField(default=0)
    no_of_brothers_priest = models.PositiveIntegerField(default=0)
    
    # Sisters Information
    no_of_sisters = models.PositiveIntegerField(default=0)
    no_of_sisters_married = models.PositiveIntegerField(default=0)
    no_of_sisters_unmarried = models.PositiveIntegerField(default=0)
    no_of_sisters_nun = models.PositiveIntegerField(default=0)
    no_of_sisters_candidate = models.PositiveIntegerField(default=0)
    
    # Family Assets
    asset_details = models.TextField(blank=True, null=True)
    
    # About Candidate's Family
    about_family = models.TextField(blank=True, null=True)
    
    # Additional Family Information
    family_contact_number = models.CharField(max_length=15, blank=True, null=True)
    family_email = models.EmailField(blank=True, null=True)
    family_address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Family Details - {self.user.full_name}"
    
    def get_total_siblings(self):
        return self.no_of_brothers + self.no_of_sisters
    
    def get_family_summary(self):
        return (
            f"{self.no_of_brothers} brothers ({self.no_of_brothers_married} married, "
            f"{self.no_of_brothers_unmarried} unmarried, {self.no_of_brothers_priest} priests), "
            f"{self.no_of_sisters} sisters ({self.no_of_sisters_married} married, "
            f"{self.no_of_sisters_unmarried} unmarried, {self.no_of_sisters_nun} nuns)"
        )
class HobbiesAndLifestyle(models.Model):
    # Habit Choices
    HABIT_CHOICES = [
        ('never', 'Never'),
        ('occasionally', 'Occasionally'),
        ('regularly', 'Regularly'),
    ]
    
    EATING_HABITS_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('eggetarian', 'Eggetarian'),
        ('non-vegetarian', 'Non-Vegetarian'),
        ('vegan', 'Vegan'),
        ('jain', 'Jain'),
    ]
    
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='hobbies')
    
    # Hobbies and Interests
    hobbies = models.TextField(blank=True, null=True)
    favorite_music = models.TextField(blank=True, null=True)
    preferred_books = models.TextField(blank=True, null=True)
    preferred_movies = models.TextField(blank=True, null=True)
    sports_games = models.TextField(blank=True, null=True)
    favorite_cuisine = models.TextField(blank=True, null=True)
    spoken_languages = models.TextField(blank=True, null=True)
    cultural_background = models.TextField(blank=True, null=True)
    
    # Lifestyle Habits
    eating_habits = models.CharField(max_length=20, choices=EATING_HABITS_CHOICES, blank=True, null=True)
    drinking_habits = models.CharField(max_length=20, choices=HABIT_CHOICES, blank=True, null=True)
    smoking_habits = models.CharField(max_length=20, choices=HABIT_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"Hobbies & Lifestyle - {self.user.full_name}"

from django.db import models
import os
import random
from datetime import date

def user_profile_picture_path(instance, filename):
    return f'profile_pictures/{instance.user.connect_id}/{filename}'

from django.db import models
from .models import UserProfile

class ProfilePicture(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pictures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Profile picture for {self.user.username}"
    
    class Meta:
        ordering = ['-uploaded_at']
    
    
# models.py
from django.db import models
from django.contrib.auth.models import User
from .models import UserProfile  # Assuming you have a UserProfile model

class Interest(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_interests')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_interests')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')  # Prevent duplicate interests
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
        
# models.py
from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)
    duration_months = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.duration_months} months) - ₹{self.price}"
    
from django.conf import settings
from django.db import models

class Payment(models.Model):
    # Option 1: If you want to use UserProfile (recommended if you have extra profile data)
    user_profile = models.ForeignKey(  # Changed to ForeignKey for multiple payments
        'UserProfile', 
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    # Option 2: If you prefer direct User reference
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     related_name='payments'
    # )
    
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        default='Pending',
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed'),
            ('Refunded', 'Refunded'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        # Access user through user_profile
        return f"{self.user_profile.user.username} - {self.plan.name} - ₹{self.amount}"
    
from django.db import models
from django.conf import settings
from matrimonyapp.models import UserProfile  # Make sure to import your UserProfile model

class Block(models.Model):
    blocker = models.ForeignKey(UserProfile, related_name='blocked_users', on_delete=models.CASCADE)
    blocked = models.ForeignKey(UserProfile, related_name='blocked_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')
        verbose_name = 'Blocked Profile'
        verbose_name_plural = 'Blocked Profiles'

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
    
from django.db import models
from matrimonyapp.models import UserProfile

class ShortlistedProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shortlister')
    shortlisted_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shortlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'shortlisted_user')
        verbose_name = 'Shortlisted Profile'
        verbose_name_plural = 'Shortlisted Profiles'

    def __str__(self):
        return f"{self.user} shortlisted {self.shortlisted_user}"