# Author: @v1s1t0r999
# Created ON [28-05-2021 @ 15:02]

"""
import LogError

try:
    (SOME CODES WHICH MAY OR MAY NOT GIVE ERRORS)
    (BUT UN-FORTUNATELY)
    (ERROR HAPPENS)
    ("!!! Why Fear When LogError is Here !!!")

except Exception as TheError:
    LogError.handle(file="FileName.log",error=TheError)

"""

import datetime

now = datetime.datetime.now()

class RequiredArgument(Exception):
	pass
class SmtpException(Exception):
	pass

def handle(file,error):
	try:
		if not file:
			raise RequiredArgument("Missing Required Argument: 'file'")
		if not error:
			raise RequiredArgument("Missing Required Argument: 'error'")
		date = now.strftime(f"[%d-%m-%Y @ %H:%M]->")
		F = open("Error.log","a")
		F.write(f"\n{str(date)}: {str(error)}")
		F.close()
	except Exception as e:
		print(e)

