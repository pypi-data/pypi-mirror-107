# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:40:13 2021

@author: Lino Boehler

"""
def main(args):
    input_file=args.file
    with open (input_file) as file:
    
       data = file.read()
       data=data.rstrip()
    
    hello="Hello World!"
    print(f"{hello}\n{data}")
    return


if __name__ == "__main__":
    import sys
    input_file=sys.argv[1]
    main(input_file)

