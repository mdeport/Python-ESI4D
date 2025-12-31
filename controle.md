# Controle
## Questions 1
### partie A

```python
import django.db import models

class Course(models.Model):
    choix_statut = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    dure_heure = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField()
    statut = models.CharField(max_length=10, choices=choix_statut)
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.titre

    def is_published(self):
        return self.statut == 'publie'
```

```python
class Instructor(models.Model):
    nom_complet = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    biographie = models.TextField()
    photo_profil = models.ImageField(blank=True, null=True)
    date_inscription = models.DateTimeField()

    def __str__(self):
        return self.nom_complet

    def total_courses(self):
        return self.courses.count()
```

```python
from .models import User

class Enrollment(models.Model):
    choix_statut = [
        ('en_cours', 'En cours'),
        ('complete', 'Complété'),
        ('abandonne', 'Abandonné'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    etudiant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_completion = models.DateTimeField(null=True, blank=True)
    note_finale = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    statut = models.CharField(max_length=15, choices=choix_statut, default='en_cours')
    def __str__(self):
        return f"{self.etudiant.username} - {self.course.titre}"

    def is_completed(self):
        return self.statut == 'complete'
```

### partie B

```python
1.Course.objects.filter(statut='publie').order_by('prix')
```
```python
2.Enrollment.objects.filter(course_id=5).select_related('etudiant')
```
```python
3.Enrollment.objects.filter(course__instructor_id=1,statut='complete').count()
```
```python
4.
``` 

### partie C

1. django implémente le design pattern active record avec son orm. cela nous permet que chaque modele soit indepentant et qu'il puisse gerer ses relations a la base de données.

2. la difference entre le pattern mvt et mvc c'est que le mvt utilise les templates pour gerer le visuelle et que le controleur est gerer dans la view alors que dans le mvc chaque partie est bien distinct avec chaque partie qui gere son role.

3. 

## Question 2
### Partie A

```python
from django import forms
from .models import Course, Enrollment
from django.core.exceptions import ValidationError
from ..models import User

class Enrollments(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course', 'etudiant', 'motivation', 'accept_terms']


    motivation = forms.CharField(widget=forms.Textarea, required=False)
    accept_terms = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(statut='publie')

    def clean_etudiant(self):
        email = self.cleaned_data.get('etudiant').email
        if not email.endswith('@student.edu'):
            raise ValidationError("L'email doit appartenir au domaine autorisé @student.edu")
        return self.cleaned_data.get('etudiant')

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if course.enrollments.count() >= 30:
            raise ValidationError("Ce cours n'a plus de places disponibles.")
        return course

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        etudiant = cleaned_data.get('etudiant')

        if Enrollment.objects.filter(course=course, etudiant=etudiant).exists():
            raise ValidationError("Vous êtes déjà inscrit à ce cours.")
```

### Partie B
#### 1
```python
from django.shortcuts import redirect, render
from .forms import Enrollments
from django.contrib import messages

def enroll_student(request):
    if request.method == 'POST':
        form = Enrollments(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie")
            return redirect('course_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs")
    else:
        form = Enrollments()
    return render(request, 'enroll.html', {'form': form})
```

#### 2
```html
{% extends 'base.html' %}

{% block content %}
  <h2>Inscription à un cours</h2>
  {% if messages %}
    {% for message in messages %}
      <div class="alert">
        {{ message }}
      </div>
    {% endfor %}
  {% endif %}

  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">S'inscrire</button>
  </form>
{% endblock %}
```

### Partie C

1. le pattern Post-Redirect-Get permet de rediriger l'utilisateur vers une nouvelle page après l'envoie d'un formulaire en post.

2. le token csrf dans django sert a géréné un jeton a l'ouverture de la session qui permet de verifier que la reponse provient bien de la bonne personne et evite toutes attaque.


## Question 3 
### Partie A

#### 1
```python
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    CHOIX_NIVEAU = [
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_etudiant = models.CharField(unique=True)
    date_naissance = models.DateField()
    niveau_etudes = models.CharField(max_length=10, choices=CHOIX_NIVEAU)

    def __str__(self):
        return self.user.username
```

#### 2

```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')
```

### Partie B
#### 1
```python
# Ajouter la class Meta dans le modele Course
class Meta :
    permissions = [
        ("can_publish_course", "Can publish course"),
        ("can_view_statistics", "Can view statistics"),
    ]
```

#### 2
```python
```

### Partie C

```python
{% if perms.app_name.can_publish_course %}
    <button>Publier</button>
{% endif %}

{% if perms.app_name.can_view_statistics %}
    <a href="{% url 'statistics' %}">Statistiques</a>
{% endif %}
<p>Bienvenue, {{ user.username }}!</p>
<a href="{% url 'logout' %}">Déconnexion</a>
```