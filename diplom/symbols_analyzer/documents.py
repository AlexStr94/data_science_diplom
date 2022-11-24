import io
import string
import xlsxwriter


ALPHABET= list(string.ascii_uppercase)

def create_paper_gradebook(journal):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    worksheet.set_default_row(20)
    worksheet.set_column(0, 0, 3)
    worksheet.set_column(1, 1, 35)
    worksheet.set_column(2, 26, 3)

    worksheet.set_portrait()
    worksheet.set_paper(9)
    worksheet.fit_to_pages(1, 1)

    title_bold_format = workbook.add_format(
        {
            'font_name': 'Times New Roman',
            'font_size': 12,
            'align': 'center',
            'bold': True
        }
    )

    table_format = workbook.add_format(
        {
            'font_name': 'Times New Roman',
            'font_size': 10,
            'valign': 'vcenter',
            'text_wrap': True,
            'border': 1,
        }
    )

    worksheet.write('A4', '№', table_format)
    worksheet.write('B4', 'ФИО/Номер занятия', table_format)
    for lesson in range(journal.lessons):
        worksheet.write(f'{ALPHABET[2+lesson]}4', '', table_format)
    for index in range(journal.students):
        worksheet.write(f'A{5+index}', f'{1+index}', table_format)
        worksheet.write(f'B{5+index}', f'Студент{index}', table_format)
        
        for lesson in range(journal.lessons):
            worksheet.write(f'{ALPHABET[2+lesson]}{5+index}', '', table_format)
    

    workbook.close()
    output.seek(0)

    return output        