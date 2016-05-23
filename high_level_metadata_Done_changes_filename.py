# Metadata script for Nukebox 2000
# modules
import acoustid
import json
import urllib2
import os
from mutagen.mp3 import MP3

# Main Class
class MetaData:
	'''
	B{NukeBox 2000 Metadata Class}
	  - Finds Metadata for .mp3 files that do not contain ID3 Tag info
	  - Uses the acoustid and musicbrainz database for metadata
	  - Metadata is used as default, if no metadata is found original file data is used
	'''
	def __init__(self, directory, music, api_key):
		
		"""
		Information needed for metadata retrieval
		
		  directory - The directory the music is contained in
		  music - The name of the music file
		  api_key - The api_key got when registering with acoustid
		  
		  All other variables are made equal to null
		
		"""
		
		self.directory = directory
		self.old_file_name = music
		self.path = directory+music
		self.api_key = api_key
		
		self.artist = "null"
		self.album = "null"
		self.user_album = "null"
		self.user_artist = "null"
		self.user_song = "null"
		self.file_name = "null"
		self.label = "null"
		self.genre = "null"
		self.length = "null" 
		self.song = "null"
		self.tracknum = "null"
		self.date = "null"
		
	def User_data_func(self):
		
		"""
		User data method
		
		  - Finds the existing song, artist, album and duration, contained in the ID3 Tag and prints to sceen. 
		  
		  - If the information is not found an appropriate message is displayed
		  
		  - Finds the duration of the song and prints it
		  
		  - Executes the fingerprint_func method
		
		"""
		
		
		try:
			self.path = song
			self.user_song = self.song["TIT2"]
			print(self.user_song)
		except:
			print ("Sorry Cannot find song title")
			
		try:
			self.user_artist = self.song["TPE1"]
			print(self.user_artist)
		except:
			print ("Sorry cannot find Artist")
		try:
			self.user_album = self.song["TALB"]
			print(self.user_album)
		except:
			print ("Sorry cannnot find Album name")
			
		#get the length of the track, divide by 60 to get minutes
		self.user_duration = path.info.length
		print(self.user_duration)
		self.fingerprint_func()
		
		
	# variables for the strip for the Audio Fingerprint out of the acoustid.fingerprint API
	def fingerprint_func(self):
		"""
		Fingerprint retrieval Method
		
		  - Strips the audio fingerprint out of the acoustid.fingerprint API
		  
		  - Executes the lines_func and duration_func methods
		
		"""
		
		fingerprint = acoustid.fingerprint_file(self.path)
		self.line = fingerprint
		
		self.line = str(self.line)
		self.line_word = ""
		self.after_word = "')"
		self.before_word = ", '"
		self.num = 1
		
		self.lines_func()
		self.duration_func()
		
	# variables for the strip for the duration out of the acoustid.fingerprint API
	# creates variables = null
	# runs line func
	def duration_func(self):
		"""
		Duration retrieval method
		
		  - Strips the duration out of the acoustid.fingerprint API
		  
		  - Executes the lines_func method
		
		"""
		self.line_word = ""
		self.after_word = "."
		self.before_word = "("
		self.num = 2
		
		
		self.lines_func()
		
		
		###############################   id_func  ##########################
		
	# uses key and duration to access the JSON metadata from the acoustid website
	# variables to isolate the song id, runs line func
	def id_func(self):
		"""
		Song ID retrieval method
		
		  - Finds the song id using the acoustid URL, inputing the duration of the song and fingerprint gathered above and 
		  also the acoustid API Key where necessary
		  
		  - Executes the lines_func method
		"""
		key = self.api_key
		duration = self.duration
		fingerprint = self.fingerprint
		
		website = "http://api.acoustid.org/v2/lookup?client="+key+"&duration="+duration+"&fingerprint="+fingerprint+"&meta=recordingids"
		response = urllib2.urlopen(website)
		
		data = json.load(response)
		self.line = str(data)
		
		self.line_word = "[{u'recordings': [{u'id': u'"
		self.after_word = "'}"
		self.before_word = "[{u'recordings': [{u'id': u'"
		self.num = 3
		
		self.lines_func()
		
		
	################ MetaData ###############################
	
	# Error check to see if the ID works on acousticbrainz website (JSON metadata)
	# If it does not it uses the acoustid API (XML metadata)
	def error_check_func(self):
		
		"""
		Error check for acousticbrainz URL method
		
		  - Uses the song ID got from above to test if the acoustbrainz website responds correctly
		  - The song ID is entered into the acoustbrainz.org URL for high-level metadata retrieval
		  - If for any reason this fails the acoustid API is used for metadata retrieval
		  - If the acoustid API is used the results are stored and edit_filename_func method is executed
		  - If the acousticbrainz.org website works successfully the artist_func method is executed
		  
		"""
		ID = self.ID
		website = "http://acousticbrainz.org/"+ID+"/high-level"
		
		try:
			response = urllib2.urlopen(website)
		except urllib2.HTTPError, e:
			if e.code:
				print "Using API\n"
				apikey = self.api_key
				fingerprint = self.fingerprint
				duration = self.duration
				
				
				data = acoustid.lookup(apikey, fingerprint, duration)
				
				result = acoustid.parse_lookup_result(data)
				
				for line in result:
					self.song = line[2]
					self.artist = line[3]
				self.edit_filename_func()
				
				return None
				
		except urllib2.URLError, e:
			print e.args,"tr"
		self.artist_func()
	
	# Isolates artist if possible, otherwise skips on to file_name
	def artist_func(self):
		"""
		Artist retrieval method
		
		  - The song ID is used to retrieve the song metadata from acousticbrainz
		  - This JSON file is parsed for the Artist name and stored in self.artist
		  - The JSON response is saved in self.data for easy parsing later
		  - Executes the album_func method
		  - A null value is used for artist is no artist information is found
		  
		"""
		
		ID = self.ID
		website = "http://acousticbrainz.org/"+ID+"/high-level"
	
		responce = urllib2.urlopen(website)
		#URL = "https://musicbrainz.org/ws/2/recording/"+ID+"?inc=aliases%2Bartist-credits%2Breleases"
		#response = urllib2.urlopen(URL)
		
		
		response = urllib2.urlopen(website)
		self.data = json.load(response)   
		#print self.data
		
		#print data
		try:
			self.artist = (self.data['metadata']['tags']['artist'][0])
			metadata = (self.data['metadata'])
			tags = (self.data['metadata']['tags'])
			self.album_func()
		except:
			self.album_func()
		#print metadata
		#print self.artist
	
	def album_func(self):
		''' 
		Album retrieval method
		
		  - Trys to retrieve the Artist information and execute the album_func method
		  - If this fails the album_func method is executed and self.album = null
		'''
		try:
			self.album = (self.data['metadata']['tags']['album'][0])
			self.file_name_func()
		except:
			self.file_name_func()
		
		
	# isolate file_name if possible, otherwise skips to label
	def file_name_func(self):
		''' 
		File name retrieval method
		
		  - Trys to retrieve the file name information and execute the label_func method
		  - If this fails the label_func method is executed and self.filename = null
		'''
		try:
			self.file_name = (self.data['metadata']['tags']['file_name'])
			self.label_func()
		except :
			self.label_func()
		#print self.file_name
		
	# isolate label if possible, otherwise skips to genre
	def label_func(self):
		''' 
		Label retrieval method
		
		  - Trys to retrieve the Label information and execute the genre_func method
		  - If this fails the genre_func method is executed and self.label = null
		'''
		try:
			self.label = (self.data['metadata']['tags']['label'][0])
			genre_func()
		except:
		#print self.label
			self.genre_func()
	
	# isolate genre if possible, otherwise skips to title
	def genre_func(self):
		''' 
		Genre retrieval method
		
		  - Trys to retrieve the genre information and execute the title_func method
		  - If this fails the title_func method is executed and self.genre = null
		'''
		try:
			self.genre = (self.data['metadata']['tags']['length'][0])
			self.title_func()
		except:
		#print self.genre
			self.title_func()
		
	# isolate  if possible, otherwise skips to label
	def title_func(self):
		''' 
		Title retrieval method
		
		  - Trys to retrieve the Title information and execute the tracknum_func method
		  - If this fails the tracknum_func method is executed and self.title = null
		'''
		try:
			self.song = (self.data['metadata']['tags']['title'][0])
			self.tracknum_func()
		except:
		#print self.song
			self.tracknum_func()
		
	# isolate Track Number if possible, otherwise skips to date of song release
	def tracknum_func(self):
		''' 
		Track Number retrieval method
		
		  - Trys to retrieve the Track Number information and exicute the date_func method
		  - If this fails the date_func method is exicuted and self.tracknum = null
		'''
		try:
			self.tracknum = (self.data['metadata']['tags']['tracknumber'][0])
			self.date_func()
		except:
		#print self.tracknum
			self.date_func()
			
	# isolate date of song release if possible, otherwise skips to edit_filename
	def date_func(self):
		''' 
		Song release date retrieval method
		
		  - Trys to retrieve the Song Release Date information and exicute the edit_filename_func method
		  - If this fails the edit_filename_func method is exicuted and self.date = null
		'''
		try:
			self.date = (self.data['metadata']['tags']['date'][0])
			self.edit_filename_func()
		except:
			self.edit_filename_func()
			
	############## Filename Validation ########################		


	# default is to use metadata if metadata returns null it uses the users filename 
	def edit_filename_func(self):
		''' 
		Edit file name method
		
		  - Checks if the artist, song or album returned null
		  - If any return null the original user data is used
		  - Edits music to the correct state for database storage
		  - If all values are null the old filename is used for storage
		  - Executes dict_func method
		'''
		
		#checks if self.file_name is a string or not
		if self.artist == "null":
			self.artist = self.user_artist
		if self.song == "null":
			self.song = self.user_song
		if self.album == "null":
			self.album = self.user_album
		
		self.song=self.song.split("(",1)[0]
		self.song=self.song.strip()
		self.new_file_name = self.artist+" - "+self.song+".mp3"
		
		if self.new_file_name == "null - null.mp3":
			self.new_file_name = self.old_file_name
			self.dict_func()
		else:
			self.dict_func()
		
		
			
		#else:
		#	self.dict_func()
		
		
		
	###############################   dic_func  #######################################
	
	
	def dict_func(self):
		'''
		Dictonary method
		
		  - Places all retrieved values into a key value pair dictionary and returns the dictonary value
		'''
		##renames file
		#os.rename(self.path, self.directory+self.file_name)
		self.send_path = self.directory+self.new_file_name
		self.dict_list = {'Artist': self.artist, 'Album': self.album, 'Old File Name': self.old_file_name, 'New File Name': self.new_file_name, 'Label': self.label, 'Genre': self.genre, 'Length': self.duration, 'Song': self.song, 'Tracknum' : self.tracknum, 'Date' : self.date, 'Path' : self.send_path}
		
		return self.dict_list
		# print "Artist:",dict_list['Artist']
		# print "Old File Name:",dict_list['Old File Name']
		# print "New File Name:",dict_list['New File Name']
		# print "Label:",dict_list['Label']
		# print "Genre:",dict_list['Genre']
		# print "Length:",dict_list['Length']
		# print "Song:",dict_list['Song']
		# print "Track Number:",dict_list['Tracknum']
		# print "Date of realease:",dict_list['Date']
		# print "Path:",dict_list['Path']


	################ LineFunc #####################
	
	#ueses variables from above to isolate certain strings from outputs
	def lines_func(self):
		'''
		Lines method
		
		  - used for string isolation for song fingerprint, duration and song ID
		'''
		line = str(self.line)

		if self.line_word in line:
			#deletes everything before and including selected string
			line=line.split(self.before_word ,-1)[-1] 
			#deletes everything after and including selected string
			line=line.split(self.after_word,1)[0]
			
			#gets rid of whitespaces
			line=line.strip()
			
		# used for fingerprint, duration and song ID isolation
		if self.num == 1:
			self.fingerprint = line
			##>>>print line
		elif self.num == 2:
			self.duration = line
			self.id_func()
			#print line
		elif self.num == 3:
			self.ID = line
			#print self.ID
			self.error_check_func()

# Main funtion to test script
def main():
	'''
	Main function to test code
	
	  - Not used in this script as values are brought in from run.py
	'''
	# a = API Key
	# d = directory of song
	# m = songs file name
	 ################  ENTER FILE NAME ##################################
	d = "/home/brian/Music/"
	m = "04 Give It All.mp3"
	a = "9xdt1PNn"
	
	
	test = MetaData(d, m, a)

	test.User_data_func()

#checks if script is run 
if __name__ == '__main__':
	main()
