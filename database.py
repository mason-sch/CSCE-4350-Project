import os

# database filename
DB_FILE = "data.db"

# KV store class
class KeyValueStore:

	# initialize store
	def __init__(self):
		# initialize list for indexing
		self.store = []

		# load state from db file
		self.load_from_file()

	# load state from db file
	def load_from_file(self):

		# if no db file exists, exit (one will be created)
		if not os.path.exists(DB_FILE):
			return

		# if db file is found
		with open(DB_FILE, "r") as f:

			# strip lines into parts
			for line in f:
				parts = line.strip().split(" ", 2)

				# if SET command is detected, set the value
				if len(parts) == 3 and parts[0] == "SET":
					key = parts[1]
					value = parts[2]
					self.set(key, value, persist=False)

	# find key within the store
	def find_key(self, key):

		# if key matches, return it. otherwise return an error
		for i in range(len(self.store)):
			if self.store[i][0] == key:
				return i
		return -1

	# SET command
	def set(self, key, value, persist=True):

		# find key if it exists
		index = self.find_key(key)

		# if key doesn't exist, create it
		if index == -1:
			self.store.append([key, value])

		# if key does exist, overwrite the value
		else:
			self.store[index][1] = value

		# if command has persistance (commands written by user), write it to the db file
		if persist:
			with open(DB_FILE, "a") as f:
				f.write(f"SET {key} {value}\n")

	# GET command
	def get(self, key):

		# find the key
		index = self.find_key(key)

		# if key doesn't exist, return error
		if index == -1:
			return -1

		# if key does exist, return the value
		return self.store[index][1]



# print welcome message
print("CSCE 4350 Project")

# create store
kv = KeyValueStore()
print("KV Store Created\n")

# infinite loop
while True:

	# strip user input of whitespace
	try:
		command = input().strip()
	except EOFError:
		break

	if not command:
		continue

	# separate command into parts
	parts = command.split(" ", 2)
	cmd = parts[0]

	# if command is SET, run the SET command
	if cmd == "SET" and len(parts) == 3:
		kv.set(parts[1], parts[2])
		print("OK\n")

	# if command is GET, run the GET command
	elif cmd == "GET" and len(parts) == 2:
		print(kv.get(parts[1]), end='\n\n')

	# if command is EXIT, break the loop
	elif cmd == "EXIT":
		break

	# otherwise, print an error
	else:
		print("ERROR, INVALID COMMAND\n")
