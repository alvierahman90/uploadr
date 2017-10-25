# uploadr
Upload files to a server on your local network for faster and simpler file transfers across a network.

## config
The config file for uploadr is very simple. It should be in a class called  `uploadr` in a file called `config.py`. It should be valid python and the two options needed are `domain` and `port` which are both used for the creation of QR code links. The file can also be used as the config file for 
gunicorn. Here is an example below:
```python
class uploadr:
	domain = "example.com"
	port = 8005

# gunicorn
bind = "0.0.0.0:" + uploadr.port
```

You also need to create the directories `qrcodes` and `uploads` (in your working directory).
## dependencies
uploadr uses the following modules:
 - `flask`
 - `qrcode`
 - `werkzeug`

