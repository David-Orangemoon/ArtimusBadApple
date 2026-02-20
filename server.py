from http.server import HTTPServer, SimpleHTTPRequestHandler, test;
import sys, getopt, math, os;

#One thing I have never understood about python is uppercase booleans
hasCors = False;
allowUrls = "*";

#Create the custom handler for the HTTP server, mostly managing the CORS stuff
class CustomHandler (SimpleHTTPRequestHandler):
    def end_headers(self):
        if (hasCors):
            self.send_header('Access-Control-Allow-Origin', allowUrls);
        SimpleHTTPRequestHandler.end_headers(self);

if __name__ == '__main__':
    try:
        port = 8000;
        directory = os.getcwd();

        args, values = getopt.getopt(sys.argv[1:], "p:ca:d:", ["cors", "allow=", "port=", "directory"]);
        for cArg, cVal in args:
            match cArg:
                case "-c" | "--cors":
                    hasCors = True;
                
                case "-p" | "--port":
                    if(cVal):
                        port = max(min(65535, int(cVal)), 0);
                
                case "-a" | "--allow":
                    if(cVal):
                        allowUrls = str(cVal);

                case "-d" | "--directory":
                    if(cVal):
                        directory = str(cVal);


        if (hasCors):
            print("Serving with CORS headers!");
            print("This CORS server allows \"" + allowUrls + "\"");

        print("You are serving at \"" + directory + "\"")

        class mixin:
            def finish_request(self, request, client_address):
                self.RequestHandlerClass(request, client_address, self, directory=directory);

        class server(mixin, HTTPServer):
            pass;

        test(CustomHandler, server, port=port);
    except getopt.error as err:
        print("An error has occurred");
        print(err);