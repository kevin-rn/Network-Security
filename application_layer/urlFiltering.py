from urllib.parse import urlparse
from os.path import splitext
import sys

if __name__ == "__main__":
    restrictions = str(sys.argv[1])
    websites = str(sys.argv[2])

    restrict_list = restrictions.split(",")
    websites_list = websites.split(",")

    for website in websites_list:
        _, filetype = splitext(urlparse(website).path)
        if filetype in restrict_list:
            print("{}: Access Denied".format(website))
        else:
            print("{}: Access Accepted".format(website))