def send_data(self, raw_str):
	if self.sockets[self]['new_version']:
		back_str = []
		back_str.append('\x81')
		data_length = len(raw_str)

		if data_length <= 125:
			back_str.append(chr(data_length))
		else:
			back_str.append(chr(126))
			back_str.append(chr(data_length >> 8))
			back_str.append(chr(data_length & 0xFF))

			back_str = "".join(back_str) + raw_str
			#self.transport.write(back_str)
	else:
		back_str = '\x00%s\xFF' % (raw_str)
		#self.transport.write(back_str)
