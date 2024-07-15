from pyautocad import Autocad, APoint
import pandas as pd
import os
from collections import defaultdict

#Auaaaaa üç yıl sonra yeniden makine öğrenmesi zamanı.
#İTÜ de bir arkadaş vardı makine öğrenmesi değil yapay öğrenme diyeceksiniz diye bizi darlayıp duruyordu.
#Noldu acaba tdk da işe girebildi mi?

def extract_table_from_autocad(selection):
    lines = []
    texts = []

    
    for entity in selection:
        if entity.EntityName in ['AcDbText', 'AcDbMText']:
            texts.append(entity)
        elif entity.EntityName == 'AcDbLine':
            start_point = APoint(entity.StartPoint)
            end_point = APoint(entity.EndPoint)
            lines.append((start_point, end_point))

    if not lines:
        print("Seçimde Tablo Bulunamadı.")
        return []


    x_coords = set()
    y_coords = set()
    for start, end in lines:
        x_coords.update([start.x, end.x])
        y_coords.update([start.y, end.y])

    x_coords = sorted(x_coords)
    y_coords = sorted(y_coords, reverse=True) 

    #print(f"x_coords: {x_coords}")
    #print(f"y_coords: {y_coords}")

    cells = defaultdict(str)
    for text in texts:
        pos = APoint(text.InsertionPoint)
        try:
            row = next(i for i, y in enumerate(y_coords[:-1]) if y > pos.y >= y_coords[i+1])
            col = next(i for i, x in enumerate(x_coords[:-1]) if x <= pos.x < x_coords[i+1])
            cells[(row, col)] = text.TextString
        except StopIteration:
            print(f"{pos} pozisyonunda ki yazı hiçbir hücreye uymadığı için es geçiliyor.")
            continue

    if not cells:
        return []

    max_row = max(cells.keys(), key=lambda x: x[0])[0]
    max_col = max(cells.keys(), key=lambda x: x[1])[1]
    table_data = [[cells.get((r, c), '') for c in range(max_col + 1)] for r in range(max_row + 1)]

    return table_data











def save_table_to_excel(table_data, excel_file):
    df = pd.DataFrame(table_data)
    df.to_excel(excel_file, index=False)



def main():
    acad = Autocad(create_if_not_exists=True)
    
    # Seçim yapılmadıysa kullanıcıdan seçim yapmasını iste
    try:
        selection = acad.get_selection()
    except Exception as e:
        print("Lütfen tabloyu seçiniz.")
        return
    
    if selection.Count == 0:
        print("Lütfen tabloyu seçiniz.")
        return

    table_data = extract_table_from_autocad(selection)
    doc = acad.ActiveDocument
    doc_konum = doc.FullName
    doc_name = doc.Name
    doc_name = doc_name.replace(".dwg", "")
    output_name = doc_konum + ".xlsx"
    doc_konum = doc_konum.replace(".dwg", "")
    output_name = doc_konum + ".xlsx"
    
    if table_data:
        save_table_to_excel(table_data, output_name)
        print("Seçim ' output_table.xlsx' adıyla elektronik tabloya döüştürüldü.")
        acad.prompt("Seçim " + doc_name + ".xlsx" + " adıyla elektronik tabloya döüştürüldü.")
    else:
        print("No tables found in the selected objects.")

if __name__ == '__main__':
    main()
