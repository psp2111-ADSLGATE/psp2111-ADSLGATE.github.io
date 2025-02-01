import ctypes, math, random, time
import requests


class DMMCache:
	availability_check_link = 'https://debridmediamanager.com/api/availability/check'
	params =  '&dmmProblemKey=%s&solution=%s&onlyTrusted=false&maxSize=0&page=%s'
	torrents_link = 'https://debridmediamanager.com/api/torrents'
	movie_link = '/movie?imdbId=%s'
	show_link = '/tv?imdbId=%s&seasonNum=%s'
	timeout = 6.05

	def __init__(self):
		dmmProblemKey, solution = self.get_secret()
		self.params = {'dmmProblemKey': dmmProblemKey, 'solution': solution}

	def check_cache(self, unchecked_hashes_chunk, imdb): # DMM API Allows max 100 hashes per request.
		data = {**self.params, 'imdbId': imdb, 'hashes': [i for i in unchecked_hashes_chunk if len(i) == 40]}
		try:
			results = requests.post(self.availability_check_link, json=data, timeout=self.timeout)
			available_hashes = results.json()['available']
			files = {file['hash']: file['files'] for file in available_hashes if 'hash' in file}
		except: files = {}

		return files

	def get_cached_hashes(self, unchecked_hashes, imdb):
		def _process(_chunk, _id):
			try: cached_hashes.update(self.check_cache(_chunk, _id))
			except: pass

		from threading import Thread

		cached_hashes = {}
		threads = []
		chunk_size = 100
		chunks = (unchecked_hashes[i:i + chunk_size] for i in range(0, len(unchecked_hashes), chunk_size))
		for chunk in chunks:
			thread = Thread(target=_process, args=(chunk, imdb))
			threads.append(thread)
			thread.start()
		[i.join() for i in threads]

		return cached_hashes

	def get_secret(self):

		def calc_value_alg(t, n, const):
			temp = t ^ n
			t = ctypes.c_long((temp * const)).value
			t4 = ctypes.c_long(t << 5).value
			x32 = t & 0xFFFFFFFF  # convert to 32-bit unsigned value
			t5 = ctypes.c_long(x32 >> 27).value
			t6 = t4 | t5

			return t6

		def slice(e, t):
			a = math.floor(len(e) / 2)
			s = e[0:a]
			n = e[a:]
			i = t[0:a]
			o = t[a:]

			l = ""
			for e in range(0, a):
				l += s[e] + i[e]

			temp = l + (o[::-1] + n[::-1])

			return temp

		def generateHash(e):
			t = int(3735928559) ^ int(len(e))
			t = ctypes.c_long(t).value
			a = 1103547991 ^ len(e)

			for s in range(len(e)):
				n = ord(e[s])
				t = calc_value_alg(t, n, 2654435761)
				# a=(a ^ n*1597334677) << 5 | a >> 27
				a = calc_value_alg(a, n, 1597334677)

			t_o = t
			t = ctypes.c_long(t + ctypes.c_long(a * 1566083941).value | 0).value
			a = ctypes.c_long(a + ctypes.c_long(t * 2024237689).value | 0).value

			return (ctypes.c_long(t ^ a).value & 0xFFFFFFFF) >> 0

		ran = random.randrange(10**80)
		myhex = "%064x" % ran

		# limit string to 64 characters
		e = myhex[:8]
		t = int(time.time())
		a = str(e) + '-' + str(t)

		s = generateHash(a)
		s = hex(s).replace('0x', '')

		n = generateHash("debridmediamanager.com%%fe7#td00rA3vHz%VmI-" + e)
		n = hex(n).replace('0x', '')

		i = slice(s, n)
		dmmProblemKey = a
		solution = i
		return dmmProblemKey, solution
