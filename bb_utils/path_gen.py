import os
from django.urls import reverse

def get_url(request, endpoint, params=None):  
    """
    The function `get_url` takes a request and an endpoint as input, and returns the complete URL for
    the given endpoint using the current scheme and host.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information about the request, such as the HTTP method, headers, and body
    :param endpoint: The `endpoint` parameter is a string that represents the name of the URL pattern
    that you want to generate the URL for
    :return: a complete URL by combining the current scheme (e.g., "http" or "https"), the current host
    (e.g., "example.com"), and the URL pattern for the "list_alert" endpoint.
    """
    if params:
        url = reverse(endpoint, args=params)
    else:
        url = reverse(endpoint)
        
    current_scheme = request.scheme
    current_host = "localhost"
    current_port = request.get_port()
    
    return f"{current_scheme}://{current_host}:{current_port}{url}"

    
def gen_root_path(current_directory=None):
    """
    Find Project's root directory path.

    Args:
        current_directory (str): The starting directory. If not provided, the current working directory will be used.

    Returns:
        str or None: The Django project's root directory path if found, otherwise None.
    """
    if current_directory is None:
        current_directory = os.getcwd()

    # Search for the manage.py file in parent directories
    while not os.path.exists(os.path.join(current_directory, '.env')):
        current_directory = os.path.dirname(current_directory)

        # Stop if we reached the root directory
        if current_directory == os.path.dirname(current_directory):
            return None

    return current_directory

def gen_backend_path():
    """
    Find the Django project's backend directory path.

    Returns:
        str or None: The Django project's backend directory path if found, otherwise None.
    """
    root = gen_root_path()
    if root is None:
        return None

    backend = os.path.join(root, 'backend')
    if os.path.exists(backend):
        return backend

    return None

def gen_scraping_path():
    """
    Find the path to the scraping directory.

    Returns:
        str or None: The path to the scraping directory if found, otherwise None.
    """
    backend = gen_backend_path()
    if backend is None:
        return None

    scraping = os.path.join(backend, 'scraping')
    if os.path.exists(scraping):
        return scraping

    return None