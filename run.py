
from high_level_metadata_Done_changes_filename import MetaData


 ################  ENTER FILE NAME ##################################
d = "/home/brian/Music/"
m = "name_me.mp3"
a = "9xdt1PNn"


test = MetaData(d, m, a)

test.fingerprint_func()



dict_list = test.dict_func()
print "Artist:",dict_list['Artist']
print "Album:",dict_list['Album']
print "Old File Name:",dict_list['Old File Name']
print "New File Name:",dict_list['New File Name']
print "Label:",dict_list['Label']
print "Genre:",dict_list['Genre']
print "Length:",dict_list['Length']
print "Song:",dict_list['Song']
print "Track Number:",dict_list['Tracknum']
print "Date of realease:",dict_list['Date']
print "Path:",dict_list['Path']



#os.rename(path, d+new_file_name)


