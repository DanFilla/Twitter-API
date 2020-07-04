import threading

def democrat_stream():
    import Democrats.DemStream.initDemStream

def republican_stream():
    import Republicans.RepStream.initRepStream

def start_schedule():
    import Schedule.status_updater

if __name__ == "__main__":
    dem = threading.Thread(target=democrat_stream)
    rep = threading.Thread(target=republican_stream)
    sched = threading.Thread(target=start_schedule)

    dem.start()
    rep.start()
    sched.start()
