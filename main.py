import threading

def democrat_stream():
    import Democrats.DemStream.initDemStream

def republican_stream():
    import Republicans.RepStream.initRepStream

if __name__ == "__main__":
    dem = threading.Thread(target=democrat_stream)
    rep = threading.Thread(target=republican_stream)

    dem.start()
    rep.start()
