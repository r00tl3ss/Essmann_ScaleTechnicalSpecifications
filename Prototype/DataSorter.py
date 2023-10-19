import g4f

def sort_data(data):
    prompt = f"Sortiere folgende Daten und gebe nur die Daten wieder: {data}"
    response = g4f.ChatCompletion.create(model=g4f.models.gpt_4_32k, provider=g4f.Provider.You, messages=[{"role": "user", "content": prompt}])
    if response is not None:
        return response
    else:
        return ""
    return ""