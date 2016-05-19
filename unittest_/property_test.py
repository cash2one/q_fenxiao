__author__ = 'binpo'

func = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default


fal = property(lambda a,b:a > a or b)
print fal