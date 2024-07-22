import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import get_orders, get_single_order

class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for Kneel Diamonds"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "orders":
            if url["pk"] != 0:
                response_body = get_single_order(url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
            response_body = get_orders()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()