# -*- coding: utf-8 -*-
import traceback


def sig_handler(signum, frame):
	print("---\n")
	print("---\n")
	print("---\nsignal: " + str(signum))
	traceback.print_stack(frame)
	print("local vars")
	for key, value in frame.f_locals.iteritems():
		print("{0}:{1}".format(key, value))
	print("---\n")
	print("---\n")
	print("---\n")
	raise Exception('signal: ' + str(signum))
	# sys.exit(signum)
