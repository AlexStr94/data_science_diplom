import string
import xlsxwriter

ALPHABET = list(string.ascii_uppercase)
ALPHABET += [f'A{s}' for s  in string.ascii_uppercase]

def create_form():
    workbook = xlsxwriter.Workbook('form.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.set_default_row(20)
    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 30, 3)

    worksheet.set_portrait()
    worksheet.set_paper(9)
    worksheet.fit_to_pages(1, 1)

    table_format = workbook.add_format(
        {
            'font_name': 'Times New Roman',
            'font_size': 10,
            'valign': 'vcenter',
            'text_wrap': True,
            'border': 1,
        }
    )

    for r in range(1, 35):
        if r < 5:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Необходимо написать цифру "1"',
                table_format
            )
        elif r < 10:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Необходимо написать цифру "2"',
                table_format
            )
        elif r < 14:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Необходимо написать цифру "3"',
                table_format
            )
        elif r < 16:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Оставьте клетку пустой',
                table_format
            )
        elif r < 20:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Необходимо написать цифру "4"',
                table_format
            )
        elif r < 22:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Оставьте клетку пустой',
                table_format
            )
        elif r < 26:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Необходимо написать цифру "5"',
                table_format
            )
        elif r < 30:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Необходимо написать букву "н"',
                table_format
            )
        elif r < 34:
            worksheet.write(
                f'{ALPHABET[0]}{r}',
                'Необходимо написать цифру "0"',
                table_format
            )
        
        for c in range(25):
            worksheet.write(f'{ALPHABET[1+c]}{r-1}', ' ', table_format)
    
    workbook.close()

    print(ALPHABET[0])

if __name__ == '__main__':
    create_form()
        

        
        

