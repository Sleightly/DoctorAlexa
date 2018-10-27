from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import random
import pandas as pd

app = Flask(__name__)
ask = Ask(app, "/health")

list_of_challenges = [
	['Complete 20 push-ups!', 'https://previews.123rf.com/images/logo3in1/logo3in11609/logo3in1160900004/62275155-step-instruction-for-push-up-of-woman-cartoon-illustration-about-work-out-.jpg'],
	['Complete 10 squats!', 'http://www.parallelcodemotifs.org/file/2018/05/quick_online_demo_of_the_squat_position.jpg'],
	['Go for a quick walk!', 'https://s3.envato.com/files/246953810/1920x1080.jpg'],
	['Get up and stretch with some leg lunges', 'https://cdn-img.health.com/sites/default/files/styles/large_16_9/public/1512670961/carrie-underwood-hot-moves-illustration.jpg?itok=iDs-LOX2&1512671216'],
	['Complete 3 neck rolls, both ways', 'https://cdn1.dailyhealthpost.com/wp-content/uploads/2017/09/04-NeckRoll.jpg'],
	['How are your wrists feeling? Do 10 wrist rolls both hands', 'http://www.pt-helper.com/images/wrist%20flexion%20extension%202_300.jpg?crc=187343839'],
	['Up and ready! Do 15 jumping jacks', 'https://img.clipartxtras.com/6f32167532a39488781dd0ea9eddc37e_jumping-jack-clipart-clipground-jumping-jack-clipart_909-1024.jpeg'],
	['Do a barrel roll!', 'https://i.stack.imgur.com/ZcHgS.png'],
	['Complete a 30 second wall sit!', 'https://img.clipartxtras.com/3c60e4db1c7a5701de2d6226f79549ef_10-great-exercises-to-do-outdoors-this-summer-wall-sit-drawing_537-821.jpeg'],
	['Breathe deeply for 15 seconds, in ...  out ... in ... out ...', 'https://img.clipartxtras.com/594655456ff1c5ff99dbfe0c831c19ce_3-easy-ways-to-breathe-deeply-wikihow-deep-breathing-drawing_728-546.jpeg']
]

list_of_tips = [
	['Get up and active every hour', 'https://c.tadst.com/gfx/750x500/dst-illustration.png?1'],
	['Try and reach 10,000 steps a day', 'https://www.ishn.com/ext/resources/Issues/2017/02-February/ISHN0217_C1_pic.jpg?1486065988'],
	['Drink 8 cups of water a day', 'https://waterandhealth.org/wp-content/uploads/2017/05/acc_pouring_water.jpg'],
	['Exercise daily, try it with \n -ask doctor to give me a challenge-', 'https://static0.fitbit.com/simple.b-cssdisabled-jpg.h2366b7ba34958d57b0e6cfbbd42686a3.pack?items=%2Fcontent%2Fassets%2Fadventures%2Fimages%2Fgallery%2Fyosemite4.jpg'],
	['Exercise daily, try it with \n -ask doctor to give me a challenge-', 'https://static1.squarespace.com/static/551954dfe4b0cc9152288892/569f67c8ab2810c1c4ef8d05/569f67c8df40f33e1071ea36/1453462882928/01_DSC4648.jpg?format=2500w'],
	['Reduce salt and sugar intake', 'https://www.belmarrahealth.com/wp-content/uploads/2017/08/eblast-salt-intake-500x339.jpg'],
	['Enjoy plenty of fruits and vegetables', 'https://www.heart.org/-/media/aha/h4gm/article-images/how-to-eat-more-fruits-and-veg.jpg?h=800&la=en&w=1200&hash=F662753067CDEBD879359EB35869072B4F1CCFA3'],
	['Get enough sleep and rest', 'https://healthblog.uofmhealth.org/sites/consumer/files/2017-01/UMH_C_SLEEPHACK%401x.jpg'],
	['Avoid bright lights before you sleep', 'https://www.telegraph.co.uk/content/dam/women/2016/09/26/phonenight_trans_NvBQzQNjv4BqpJliwavx4coWFCaEkEsb3kvxIt-lGGWCWqwLa_RXJU8.JPG?imwidth=450'],
	['Have fun and be happy!', 'https://imgc.allpostersimages.com/img/print/posters/brett-wilson-be-happy-and-smile_a-G-13062055-0.jpg']
]



@app.route('/')
def home():
	return 'Substitute homepage'

@ask.launch
@ask.intent('question')
def command(command):
	output = parse_command(command)
	return output

@ask.intent('details')
def details():
	instructs = [
		"show me my medications",
		"show me my reminders",
		"tell me a tip",
		"give me a challenge",
		"when should I take my next medication"
	]
	list_of_in = "Here are some sample commands . . . "
	for i in range(len(instructs)):
		list_of_in = list_of_in + instructs[i] + " . . . "

	text = list_of_in.replace(". . .", "\n  -	").split('\n')
	text_file = ""
	for i in range(len(text)-1):
		text_file = text_file + "\n" + text[i]
	return statement(list_of_in).standard_card(
					title='Helpful Commands',
                    text=text_file,
                    small_image_url='https://cdn.shopify.com/s/files/1/0194/3447/products/refer_to_instructions_label_c7a08cc5-bfd0-4268-8c7e-6f0e0935be95.png?v=1507145698',
                    large_image_url='https://cdn.shopify.com/s/files/1/0194/3447/products/refer_to_instructions_label_c7a08cc5-bfd0-4268-8c7e-6f0e0935be95.png?v=1507145698')


def parse_command(command):
	print(command)
	if "challenge" in command:
		choice = random_choice()
		text_file = list_of_challenges[choice][0] #database call
		respond = "Let see if you can complete this challenge. . . " + text_file
		return statement(respond).standard_card(
					title='Challenge',
                    text=text_file,
                    small_image_url= list_of_challenges[choice][1],
                    large_image_url= list_of_challenges[choice][1])
	if "advice" in command:
		choice = random_choice()
		print(choice)
		text_file = list_of_tips[choice][0]#database call
		respond = "The more you know!" + text_file
		return statement(respond).standard_card(
					title='Advice',
                    text=text_file,
                    small_image_url=list_of_tips[choice][1],
                    large_image_url=list_of_tips[choice][1])
	if "reminders" or "reminder" or "schedule" or "schedules" in command:
		text_file = "test"#database call
		respond = "Here are your next medications. . . " + text_file
		return statement(respond).standard_card(
					title='reminders',
                    text=text_file,
                    small_image_url='https://example.com/small.png',
                    large_image_url='https://example.com/large.png')
	elif "medication" or "medications" in command:
		text_file = "test"#database call
		respond = "These are your medications. . . " + text_file
		return statement(respond).standard_card(title='CATS says...',
                       text=text_file,
                       small_image_url='https://example.com/small.png',
                       large_image_url='https://example.com/large.png')
	else:
		return statement("Sorry, I did not catch that . . . " + details())

def random_choice():
	return random.randint(0, 9);

'''
@ask.intent("YesIntent")
def read_subreddits():
	print('here')
	subreddits = get_subreddits('')
	sub_reddit_msg = 'The found subreddits are {}'.format(subreddits)
	return statement(sub_reddit_msg)
@ask.intent("NoIntent")
def stop_action():
	bye = "Okay... bye"
	return statement(bye)
'''

if __name__ == '__main__':
	app.run(debug=True)
