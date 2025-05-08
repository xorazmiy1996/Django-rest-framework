import time


class LatencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()  # So'rov boshlanish vaqti
        response = self.get_response(request)
        end_time = time.time()  # So'rov tugash vaqti

        # Javobga latency ni qo'shish (headers yoki body ga)
        response["X-Latency"] = f"{end_time - start_time:.3f} seconds"
        return response