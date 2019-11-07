# This allow the app to save temporary files
# to send via the `send_file` flask function
# See this thread for some better ways to this:
# https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask
# None of those seemed as reliable, so this is a stopgap solution

import os, time, random, glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(CURRENT_DIR, "..", "tmp")

def ensure_temp_directory_exists():
	if not os.path.exists(TEMP_DIR):
		os.makedirs(TEMP_DIR)


# Files will be delete on server start OR on each requests
# As long as they are at least 30 seconds old
SECONDS_TILL_DELETION = 30

def delete_expired_temp_files():
	now = int(time.time())
	for filepath in glob.glob("%s/*" % TEMP_DIR):
		filename = os.path.basename(filepath)
		try:
			timepart = int(filename.split("-")[0])
			if (timepart + SECONDS_TILL_DELETION) < now:
				os.remove(filepath)

		except ValueError:
			pass

# File name is the time it was created
# and a random int to avoid collisions
def get_file_path(ext="txt"):
	now = int(time.time())
	filename = "%i-%i.%s" % (now, random.randint(0, 10000000), ext)
	return "%s/%s" % (TEMP_DIR, filename)