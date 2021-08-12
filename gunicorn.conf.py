

def post_worker_init(worker):
    from app import start_check
    start_check()

