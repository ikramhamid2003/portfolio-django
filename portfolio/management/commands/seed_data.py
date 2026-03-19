from django.core.management.base import BaseCommand
from portfolio.models import Project, Experience, Certification, Skill


class Command(BaseCommand):
    help = 'Seed portfolio with Ikram resume data'

    def handle(self, *args, **kwargs):
        Project.objects.all().delete()
        Experience.objects.all().delete()
        Certification.objects.all().delete()
        Skill.objects.all().delete()

        projects = [
            dict(title='StudyBuddy — AI Study Assistant', image_emoji='🤖', featured=True, order=1,
                 tech_stack='React, Django REST Framework, PostgreSQL, Groq API, Llama 3.3',
                 github_url='https://github.com/ikramhamid2003',
                 description='Full-stack AI-powered study assistant with 5+ REST APIs, LLM integration via Groq (Llama 3.3), rate limiting, CORS, structured JSON parsing, and secure API key management.'),
            dict(title='Career Navigator', image_emoji='🧭', featured=True, order=2,
                 tech_stack='Django REST Framework, React, Vite, Tailwind CSS, scikit-learn, Groq LLaMA, PostgreSQL (Neon.tech)',
                 github_url='https://github.com/ikramhamid2003',
                 description='AI career counseling app with VotingClassifier ensemble (KNN, RandomForest, GradientBoosting, SVM), 43 RIASEC features, 12K training samples, SSE streaming chat, and skills gap analysis API.'),
            dict(title='AR Robot Assembly Kit', image_emoji='🥽', featured=True, order=3,
                 tech_stack='Unity, AR Foundation, C#',
                 github_url='https://github.com/ikramhamid2003',
                 description='AR-based 3D robot assembly app with drag-and-drop mechanics, physics-based snapping, progress tracking, hints, and scoring — applied in STEM education.'),
            dict(title='Django Portfolio Website', image_emoji='🌐', featured=False, order=4,
                 tech_stack='Django, Tailwind CSS, SQLite, PowerShell',
                 github_url='https://github.com/ikramhamid2003',
                 description='Dark futuristic personal portfolio with 8 DB models, Django admin, and PowerShell automation for Windows setup.'),
            dict(title='Responsive Portfolio v1', image_emoji='📊', featured=False, order=5,
                 tech_stack='HTML, CSS, JavaScript',
                 github_url='https://github.com/ikramhamid2003',
                 description='Fully responsive static website with smooth animations and project showcases.'),
        ]
        for p in projects:
            Project.objects.create(**p)

        Experience.objects.create(
            role='Machine Learning Intern', company='Edunet Foundation (AICTE & IBM SkillsBuild)',
            start_date='Jan 2026', end_date='Feb 2026', order=1,
            description="Developed backend APIs for an AI-powered Study Assistant using Django REST Framework\nImplemented serializer-based validation and structured JSON response handling\nEvaluated LLM outputs and improved response reliability using prompt engineering\nEnhanced consistency and performance of AI-generated responses")

        Experience.objects.create(
            role='Web Development Intern', company='AspiraSys Pvt. Ltd.',
            location='Chennai, India', start_date='Jul 2025', end_date='Aug 2025', order=2,
            description="Assisted in frontend development tasks using modern web technologies\nApplied AI-assisted tools to support development and improve coding efficiency\nGained exposure to deployment processes and application testing workflows\nCollaborated using Git for version control and project management")

        Certification.objects.create(title='AI & Machine Learning Internship Certificate',
            issuer='Edunet Foundation (AICTE · IBM SkillsBuild)', date='Feb 2026', icon_emoji='🤖')
        Certification.objects.create(title='Web Development Internship Certificate',
            issuer='AspiraSys Pvt. Ltd.', date='Aug 2025', icon_emoji='💻')
        Certification.objects.create(title='IBM SkillsBuild — AI Fundamentals',
            issuer='IBM · AICTE', date='2026', icon_emoji='🏆')
        Certification.objects.create(title='Python for Data Science',
            issuer='IBM SkillsBuild', date='2026', icon_emoji='🔬')

        skills = [
            ('Python','languages',95),('JavaScript','languages',80),
            ('Java','languages',70),('C','languages',65),
            ('Django REST Framework','backend',90),('REST APIs','backend',90),('API Design','backend',85),
            ('React','frontend',80),('Vite','frontend',75),('Tailwind CSS','frontend',85),('HTML/CSS','frontend',85),
            ('LLM Integration','ai_ml',88),('Prompt Engineering','ai_ml',85),
            ('Groq API','ai_ml',85),('scikit-learn','ai_ml',75),
            ('PostgreSQL','databases',85),('MySQL','databases',70),('SQLite','databases',80),
            ('Git','tools',90),('GitHub','tools',90),('Postman','tools',85),('VS Code','tools',90),
        ]
        for name, cat, prof in skills:
            Skill.objects.create(name=name, category=cat, proficiency=prof)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded: {Project.objects.count()} projects, '
            f'{Experience.objects.count()} experiences, '
            f'{Certification.objects.count()} certs, '
            f'{Skill.objects.count()} skills'))
