def bindframe(frame,sequence,func):
    frame.bind(sequence, func)
    for child in frame.winfo_children():
        child.bind(sequence, func)
