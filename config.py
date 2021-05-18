class uploadr:
	domain = "example.com"
	port = 5000
	uploads = './uploads' # uploaded files will be stored
	qrcodes = './qrcodes' # qr codes will be stored

# gunicorn
bind = "0.0.0.0:" + uploadr.port
