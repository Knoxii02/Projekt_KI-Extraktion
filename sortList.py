#Input: string (Liste, getrennt durch Kommas) : Sortiere die Liste alphabetisch und gib sie als string zurück
def sort_list(input_list: str) -> str:
    items = [item.strip() for item in input_list.split(',')]
    items.sort()
    return ', '.join(items)
#--------------------------------------------------------------------------------

liste = "I²C, UART, RS-232, SPI, CAN, LIN"
sorted_liste = sort_list(liste)
print(sorted_liste)