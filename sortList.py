#Input: string (Liste, getrennt durch Kommas) : Sortiere die Liste alphabetisch und gib sie als string zurück
def sort_list(input_list: str) -> str:
    items = [item.strip() for item in input_list.split(',')]
    items.sort()
    return ', '.join(items)
#--------------------------------------------------------------------------------

liste = "Edge, Pulse width, Glitch, Runt, Timeout, Pattern/State, Setup/hold, Window, Protocol, Generic Protocol, Burst, Nth Edge, OR'd Edges, InfiniiScan Zone, Measurement limit, Non-monotonic edge"


sorted_liste = sort_list(liste)
print(sorted_liste)