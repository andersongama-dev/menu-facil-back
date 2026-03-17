def summarize_history(history):

    summary = []

    for h in history:

        if isinstance(h, dict):
            summary.append(", ".join(f"{k}: {v}" for k, v in h.items()))
        else:
            summary.append(str(h))

    return "\n".join(summary)