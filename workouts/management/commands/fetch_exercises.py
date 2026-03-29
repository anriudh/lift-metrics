import json
import urllib.request
from django.core.management.base import BaseCommand
from decouple import config
from workouts.models import Exercise


class Command(BaseCommand):
    help = 'Fetches exercises from ExerciseDB API on RapidAPI and saves them to the database'

    def handle(self, *args, **options):
        api_key = config('RAPIDAPI_KEY', default='')
        
        if not api_key:
            self.stdout.write(self.style.ERROR('RAPIDAPI_KEY not found in .env file.'))
            return

        url = 'https://edb-with-videos-and-images-by-ascendapi.p.rapidapi.com/api/v1/exercises?limit=100&offset=0'
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'edb-with-videos-and-images-by-ascendapi.p.rapidapi.com'
        }
        
        try:
            self.stdout.write(self.style.NOTICE(f'Fetching exercises from {url}...'))
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                response_json = json.loads(response.read().decode())
            
            if isinstance(response_json, dict):
                self.stdout.write(self.style.NOTICE(f"Response structure keys: {response_json.keys()}"))
                exercises = response_json.get('data', [])
            else:
                self.stdout.write(self.style.ERROR(f'Unexpected response format: {type(response_json)}'))
                return

            if not isinstance(exercises, list):
                self.stdout.write(self.style.ERROR(f"Expected 'data' to be a list, got {type(exercises)}"))
                return

            if len(exercises) > 0:
                self.stdout.write(self.style.NOTICE(f"Exercise item keys: {exercises[0].keys()}"))

            count = 0
            for item in exercises:
                # Map fields:
                # name -> name
                # target -> muscle_group
                # equipment -> equipment
                # gifUrl -> image_url
                
                exercise, created = Exercise.objects.get_or_create(
                    name=item.get('name'),
                    defaults={
                        'muscle_group': item.get('target', 'unknown'),
                        'equipment': item.get('equipment', 'none'),
                        'image_url': item.get('gifUrl', '')
                    }
                )
                
                if created:
                    count += 1
                
                # Progress logging using manual counter
                current_idx = exercises.index(item) + 1
                if current_idx % 10 == 0:
                    self.stdout.write(f"Processed {current_idx} / {len(exercises)} exercises...")
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} new exercises.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
