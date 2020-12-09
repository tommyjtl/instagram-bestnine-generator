from igramscraper.instagram import Instagram
from datetime import datetime
import time, sys, requests, os

account_input = input("Enter an account username: ")
check_use_password = input("Is is a private account? (Y/N): ")

if check_use_password == "Y" or check_use_password == "y": 
	your_username = input("Enter your username: ")
	your_password = input("Enter your password: ")
else: pass

instagram = Instagram()

try:
	if check_use_password == "Y" or check_use_password == "y": 
		instagram.with_credentials(your_username, your_password, '.')
		instagram.login()

	account = instagram.get_account(account_input)
	print("Fetching total media published…")

	total_published = account.media_count
	division = int(total_published / 4)
	print("Total media counts: ", str(total_published))

	'''
	media.short_code
	media.comments_count
	media.likes_count
	media.image_high_resolution_url
	'''

	all = []

	is_not_2020 = False
	init_count = division
	init_count_times = 1

	while is_not_2020 == False:

		try:
			print("Requesting time: ", str(init_count_times))
			if check_use_password == "Y" or check_use_password == "y": 
				instagram.with_credentials(your_username, your_password, '.')
				instagram.login()

			medias = instagram.get_medias(account_input, init_count)

			for media in medias: 
				ts = int(str(media.created_time))
				new_dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
				all.append([str(media.short_code), str(new_dt[0:10]), str(media.likes_count), str(media.comments_count), str(media.image_high_resolution_url)])
				# print(media.short_code, new_dt[0:10], media.likes_count)
				
				if new_dt[0:4] != '2020': 
					# print(str(media.short_code), str(new_dt[0:10]), str(media.likes_count), str(media.comments_count), str(media.image_high_resolution_url))
					is_not_2020 = True
					all = all[:-1]
					# print(all)

					sort_out = sorted(all, key=lambda x: int(x[2]), reverse=True)
					# print(sort_out)
					sum = 0

					os.mkdir(str(account_input))
					os.chdir("./" + str(account_input))
					count = 1

					if len(sort_out) >= 9:
						for each in sort_out:
							sum = sum + int(each[2])
							print(each[0], each[1], each[2])

							if count < 10:
								img_data = requests.get(each[4]).content
								with open(str(count)+'_'+str(each[1])+'.jpg', 'wb') as handler:
								    handler.write(img_data)
							
							count += 1

						print("Total likes: ", str(sum), "\t Total posts in 2020: ", str(len(sort_out)))
						sys.exit(0)
					else:
						print("Less than 9 photos this year.")

			all = []
			init_count += division
			init_count_times += 1

			print("Hold for 20 seconds…")

			for t in range(0,20,1): 
				print(".",end="")
				time.sleep(1)
		except: pass
except BaseException as e:
	print(str(e))
