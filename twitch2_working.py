import random
import os
import asyncio
from twitchio.ext import commands
import serial

class Bot(commands.Bot):
    def __init__(self):
        serial_port = os.getenv('SERIAL_PORT')  # Get the serial port from environment variable
        self.SerialObj = serial.Serial(serial_port)
        self.SerialObj.baudrate = 9600  # set Baud rate to 9600
        self.SerialObj.bytesize = 8   # Number of data bits = 8
        self.SerialObj.parity  ='N'   # No parity
        self.SerialObj.stopbits = 1   # Number of Stop bits = 1
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'], initial_channels=[os.environ['CHANNEL']])
        self.water_count = 0  # Counter to keep track of the number of times the plant has been watered
        
        # Plant trivia questions and answers
        self.plant_trivia = [
{
    'question': 'What is the world’s tallest tree species?',
    'options': ['A) Coast Redwood', 'B) Giant Sequoia', 'C) Douglas Fir', 'D) Sitka Spruce'],
    'answer': 'A'
},
{
    'question': 'Which flower is often associated with love and Valentine’s Day?',
    'options': ['A) Daisy', 'B) Rose', 'C) Lily', 'D) Orchid'],
    'answer': 'B'
},
{
    'question': 'Which plant is the national flower of Japan?',
    'options': ['A) Sakura (Cherry Blossom)', 'B) Lotus', 'C) Chrysanthemum', 'D) Bamboo'],
    'answer': 'A'
},
{
    'question': 'Which plant is used to make tequila?',
    'options': ['A) Agave', 'B) Cactus', 'C) Yucca', 'D) Aloe Vera'],
    'answer': 'A'
},
{
    'question': 'Which plant is also known as the “corpse flower” due to its foul smell?',
    'options': ['A) Rafflesia', 'B) Titan Arum', 'C) Venus Flytrap', 'D) Pitcher Plant'],
    'answer': 'B'
},
{
    'question': 'Which plant is known for its ability to trap and digest insects?',
    'options': ['A) Sundew', 'B) Pitcher Plant', 'C) Venus Flytrap', 'D) All of the above'],
    'answer': 'D'
},
{
    'question': 'Which plant is often used as a natural insect repellent?',
    'options': ['A) Lavender', 'B) Citronella', 'C) Basil', 'D) Mint'],
    'answer': 'B'
},
{
    'question': 'Which plant is believed to bring good luck according to Feng Shui?',
    'options': ['A) Bamboo', 'B) Money Plant', 'C) Snake Plant', 'D) Jade Plant'],
    'answer': 'D'
},
{
    'question': 'Which plant is a symbol of purity and is often used in religious ceremonies?',
    'options': ['A) Jasmine', 'B) Lotus', 'C) Tulip', 'D) Daisy'],
    'answer': 'B'
},
            # Add more trivia questions here...
        ]

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def water(self, ctx: commands.Context):
        # Choose a random trivia question
        trivia_question = random.choice(self.plant_trivia)
        await ctx.send(trivia_question['question'])
        await ctx.send('\n'.join(trivia_question['options']))
        await asyncio.sleep(0.2)
        try:
            msg = await self.wait_for('message', timeout=30)                
            user_answer = msg[0].content.strip().upper()  # Convert the answer to uppercase
            print(user_answer)
                # Check if the user's answer is correct
            if user_answer == trivia_question['answer']:
                    self.water_count += 1  # Increment the water count
                    await ctx.send(f'Correct answer, watering the plant! Thanks {ctx.author.name}! This is the {self.water_count}th time!')
                    self.SerialObj.write(b'A') 
            else:
                    await ctx.send('Incorrect answer! Better luck next time!')
        except asyncio.TimeoutError:
                    await ctx.send("Time's up! You didn't answer in time.")
        except Exception as error:
              print("uncaught error", error)

bot = Bot()
bot.run()
