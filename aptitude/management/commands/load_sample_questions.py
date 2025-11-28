from django.core.management.base import BaseCommand
from aptitude.models import Question

class Command(BaseCommand):
    help = 'Load 25 sample aptitude questions'

    def handle(self, *args, **options):
        # Sample questions data
        sample_questions = [
            {
                'question_text': 'What is the capital of France?',
                'option_a': 'London',
                'option_b': 'Berlin',
                'option_c': 'Paris',
                'option_d': 'Madrid',
                'correct_option': 'C'
            },
            {
                'question_text': 'Which planet is known as the Red Planet?',
                'option_a': 'Venus',
                'option_b': 'Mars',
                'option_c': 'Jupiter',
                'option_d': 'Saturn',
                'correct_option': 'B'
            },
            {
                'question_text': 'What is 15 + 27?',
                'option_a': '42',
                'option_b': '32',
                'option_c': '52',
                'option_d': '47',
                'correct_option': 'A'
            },
            {
                'question_text': 'Who wrote "Romeo and Juliet"?',
                'option_a': 'Charles Dickens',
                'option_b': 'William Shakespeare',
                'option_c': 'Jane Austen',
                'option_d': 'Mark Twain',
                'correct_option': 'B'
            },
            {
                'question_text': 'What is the largest mammal?',
                'option_a': 'Elephant',
                'option_b': 'Blue Whale',
                'option_c': 'Giraffe',
                'option_d': 'Hippopotamus',
                'correct_option': 'B'
            },
            {
                'question_text': 'Which element has the chemical symbol "O"?',
                'option_a': 'Gold',
                'option_b': 'Oxygen',
                'option_c': 'Osmium',
                'option_d': 'Oganesson',
                'correct_option': 'B'
            },
            {
                'question_text': 'What is the square root of 64?',
                'option_a': '6',
                'option_b': '7',
                'option_c': '8',
                'option_d': '9',
                'correct_option': 'C'
            },
            {
                'question_text': 'Which country is known as the Land of the Rising Sun?',
                'option_a': 'China',
                'option_b': 'Thailand',
                'option_c': 'South Korea',
                'option_d': 'Japan',
                'correct_option': 'D'
            },
            {
                'question_text': 'What is the hardest natural substance on Earth?',
                'option_a': 'Gold',
                'option_b': 'Iron',
                'option_c': 'Diamond',
                'option_d': 'Platinum',
                'correct_option': 'C'
            },
            {
                'question_text': 'How many continents are there?',
                'option_a': '5',
                'option_b': '6',
                'option_c': '7',
                'option_d': '8',
                'correct_option': 'C'
            },
            {
                'question_text': 'Which gas do plants absorb from the atmosphere?',
                'option_a': 'Oxygen',
                'option_b': 'Nitrogen',
                'option_c': 'Carbon Dioxide',
                'option_d': 'Hydrogen',
                'correct_option': 'C'
            },
            {
                'question_text': 'What is the currency of Japan?',
                'option_a': 'Yuan',
                'option_b': 'Won',
                'option_c': 'Yen',
                'option_d': 'Ringgit',
                'correct_option': 'C'
            },
            {
                'question_text': 'Which ocean is the largest?',
                'option_a': 'Atlantic Ocean',
                'option_b': 'Indian Ocean',
                'option_c': 'Arctic Ocean',
                'option_d': 'Pacific Ocean',
                'correct_option': 'D'
            },
            {
                'question_text': 'How many sides does a hexagon have?',
                'option_a': '5',
                'option_b': '6',
                'option_c': '7',
                'option_d': '8',
                'correct_option': 'B'
            },
            {
                'question_text': 'Who painted the Mona Lisa?',
                'option_a': 'Vincent van Gogh',
                'option_b': 'Pablo Picasso',
                'option_c': 'Leonardo da Vinci',
                'option_d': 'Michelangelo',
                'correct_option': 'C'
            },
            {
                'question_text': 'What is the boiling point of water in Celsius?',
                'option_a': '90°C',
                'option_b': '100°C',
                'option_c': '110°C',
                'option_d': '120°C',
                'correct_option': 'B'
            },
            {
                'question_text': 'Which animal is known as the King of the Jungle?',
                'option_a': 'Tiger',
                'option_b': 'Elephant',
                'option_c': 'Lion',
                'option_d': 'Bear',
                'correct_option': 'C'
            },
            {
                'question_text': 'What is the smallest prime number?',
                'option_a': '0',
                'option_b': '1',
                'option_c': '2',
                'option_d': '3',
                'correct_option': 'C'
            },
            {
                'question_text': 'Which planet is closest to the Sun?',
                'option_a': 'Venus',
                'option_b': 'Mercury',
                'option_c': 'Mars',
                'option_d': 'Earth',
                'correct_option': 'B'
            },
            {
                'question_text': 'How many bones are in the human body?',
                'option_a': '206',
                'option_b': '250',
                'option_c': '300',
                'option_d': '180',
                'correct_option': 'A'
            },
            {
                'question_text': 'What is the main ingredient in guacamole?',
                'option_a': 'Tomato',
                'option_b': 'Avocado',
                'option_c': 'Onion',
                'option_d': 'Pepper',
                'correct_option': 'B'
            },
            {
                'question_text': 'Which is the longest river in the world?',
                'option_a': 'Amazon River',
                'option_b': 'Mississippi River',
                'option_c': 'Nile River',
                'option_d': 'Yangtze River',
                'correct_option': 'C'
            },
            {
                'question_text': 'What does CPU stand for?',
                'option_a': 'Central Processing Unit',
                'option_b': 'Computer Personal Unit',
                'option_c': 'Central Processor Unit',
                'option_d': 'Central Program Unit',
                'correct_option': 'A'
            },
            {
                'question_text': 'Which gas is most abundant in the Earth\'s atmosphere?',
                'option_a': 'Oxygen',
                'option_b': 'Carbon Dioxide',
                'option_c': 'Nitrogen',
                'option_d': 'Hydrogen',
                'correct_option': 'C'
            },
            {
                'question_text': 'How many degrees are in a circle?',
                'option_a': '180',
                'option_b': '270',
                'option_c': '360',
                'option_d': '90',
                'correct_option': 'C'
            }
        ]

        # Create questions
        for question_data in sample_questions:
            question, created = Question.objects.get_or_create(
                question_text=question_data['question_text'],
                defaults={
                    'option_a': question_data['option_a'],
                    'option_b': question_data['option_b'],
                    'option_c': question_data['option_c'],
                    'option_d': question_data['option_d'],
                    'correct_option': question_data['correct_option']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created question: {question.question_text}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Question already exists: {question.question_text}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {len(sample_questions)} sample questions')
        )