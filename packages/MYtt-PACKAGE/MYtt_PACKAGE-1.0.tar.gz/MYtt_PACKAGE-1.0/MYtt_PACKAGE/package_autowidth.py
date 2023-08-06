def autowidth(inputfile,sheetname,number,outputfile):
    from openpyxl import load_workbook, workbook
    workbook = load_workbook(inputfile)
    sheet = workbook[sheetname]
    ######对单元格列宽根据字符串长度自动调整的设置######
    #使用：for循环遍历得出每列长度后形成字典数据来自动设置每列列宽
    dims = {}
    for row in sheet.rows:
        for cell in row:
            if cell.value:
                """
                首先获取每个单元格中的长度；如果有换行符则按单行的长度计算，先分割再计算；
                长度计算：(len(line.encode("utf-8"))-len(line))/2+len(line)，line.encode("utf-8")将中文的字节数定义为2；
                字典储存每列的宽度：将每列的列名作为键名，cell长度计算的最大值作为键值
                """
                len_cell = max([(len(line.encode("utf-8"))-len(line))/2+len(line) for line in str(cell.value).split("\n")])
                dims[cell.column_letter] = max(dims.get(cell.column_letter,0),len_cell)#dict.get(key, default=None)
    #通过遍历存储每列的宽度的字典，来设置相关列的宽度
    for col,value in dims.items():
        sheet.column_dimensions[col].width = value+number if value<50 else 50
    workbook.save(outputfile)

if __name__ == "__main__":
    inputfile = "D:\\1AAA\python开发\\Bio_T2Ex\CSV\\CSV.template.xlsx"
    sheetname = "Sheet"
    number = 6
    outputfile = "D:\\1AAA\python开发\\Bio_T2Ex\CSV\\CSV.template111.xlsx"
    autowidth(inputfile,sheetname,number,outputfile)