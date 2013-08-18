import optparse

class Args:
    
    def __init__(self, args):
        self.args = args
        usageList = ["usage %prog"]
        for arg, val in args.items():
            usageList.append("%s <%s>"%(arg, val))
        self.parser = optparse.OptionParser(' '.join(usageList))

        for arg, val in args.items():
            self.parser.add_option(arg, dest=val, type='string', help='No')

    def getArgs(self):
        (options, args) = self.parser.parse_args()
        for  attr, value in options.__dict__.iteritems():
            if value == None:
                print self.parser.usage
                exit(0)
        return options

def main():
    args = Args({'-H': 'alpha', '-p': 'omega' })
    argsResult = args.getArgs()
    print argsResult.alpha
        
if __name__ == "__main__":
    main()
