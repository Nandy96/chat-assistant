import getopt
import httplib
import os
import sys
import urllib

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '665a1157fa944f86a7adfe61e58a9489',
}

params = urllib.urlencode({
})


# appId = '594deced-2f12-44f3-9a90-db5f0c7c75ec'
# versionId = '0.1'


def main(argv):
    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        print conn
        help_str = ("Usage: \n"
                    "python string_parser.py "
                    "--file_name <file name>")
        try:
            opts, args = getopt.getopt(argv, "h",
                                       ["file_name="])
            print opts, args
        except getopt.GetoptError as ex:
            print help_str
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print help_str
                sys.exit()
            elif opt in "--file_name":
                file_name = str(arg)

        if os.path.isfile(file_name):
            with open(file_name, 'r+') as f:
                for line in f:
                    word = """ {"name": "%s"} """ % line
                    conn.request("POST",
                                 "/luis/api/v2.0/apps/10c26ec5-11c4-4854-a7f8-2bb32a6e469a/versions/0.1/entities?%s"
                                 % params, word, headers)
                    response = conn.getresponse()
                    print response
                    data = response.read()
                    print(data)

    except Exception as e:
        print("[Errno {}".format(e))


if __name__ == "__main__":
    main(sys.argv[1:])
