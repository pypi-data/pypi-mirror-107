from Email import SendMail, FetchMail, MarkMailFlags

if __name__ == '__main__':
    x = MarkMailFlags()
    x.MarkOtherFlag([1, 2], "answered", True)
