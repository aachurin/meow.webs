from meow.webs import Route, Include

extra_routes = [
    Route("/path_params/{p1}/{p2}/{p3}/", "GET", "views.get_extra_path_params")
]

extra_routes2 = [
    Route("/path_params/{p1}/{p2}/{p3}/", "GET", "views.get_extra_path_params")
]

routes = [
    Route("/request/", "GET", "views.get_request"),
    Route("/method/", "GET", "views.get_method"),
    Route("/method/", "POST", "views.get_method", name="post_method"),
    Route("/scheme/", "GET", "views.get_scheme"),
    Route("/host/", "GET", "views.get_host"),
    Route("/port/", "GET", "views.get_port"),
    Route("/path/", "GET", "views.get_path"),
    Route("/query_string/", "GET", "views.get_query_string"),
    Route("/query_params/", "GET", "views.get_query_params"),
    Route("/page_query_param/", "GET", "views.get_page_query_param"),
    Route("/url/", "GET", "views.get_url"),
    Route("/body/", "POST", "views.get_body"),
    Route("/headers/", "GET", "views.get_headers"),
    Route("/headers/", "POST", "views.get_headers", name="post_headers"),
    Route("/accept_header/", "GET", "views.get_accept_header"),
    Route("/missing_header/", "GET", "views.get_missing_header"),
    Route("/path_params/{example}/", "GET", "views.get_path_params"),
    Route(
        "/full_path_params/{+example}",
        "GET",
        "tests.views.get_path_params",
        name="full_path_params",
    ),
    Route("/request_data/", "POST", "views.get_request_data"),
    Route("/multikey_request_data/", "POST", "views.get_multikey_request_data"),
    Route("/return_string/", "GET", "views.return_string"),
    Route("/return_bytes/", "GET", "views.return_bytes"),
    Route("/return_data/", "GET", "views.return_data"),
    Route("/return_template/", "GET", "views.return_template"),
    Route("/return_none/", "GET", "views.return_none"),
    Route("/return_response/", "GET", "views.return_response"),
    Route("/return_own_status_code/", "GET", "views.return_own_status_code"),
    Route("/return_unserializable_json/", "GET", "views.return_unserializable_json"),
    Route("/return_302/", "GET", "views.return_302"),
    Route("/return_bad_response/", "GET", "views.return_bad_response"),
    Route("/return_default_query_param/", "GET", "views.return_default_query_param"),
    Route("/return_required_query_param/", "GET", "views.return_required_query_param"),
    Route(
        "/return_input_data_get/",
        "GET",
        "views.return_input_data",
        name="return_input_data_get",
    ),
    Route(
        "/return_input_data_post/",
        "POST",
        "views.return_input_data",
        name="return_input_data_post",
    ),
    Route(
        "/return_wrapped_response/",
        "GET",
        ["views.return_string", "views.wrap_result"],
        name="return_wrapped_response",
    ),
    Include("/extra", "extra", extra_routes),
    Include("/extra2", "extra2", "routes.extra_routes2"),
]
