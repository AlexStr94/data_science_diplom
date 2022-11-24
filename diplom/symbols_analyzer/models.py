from django.db import models


class Journal(models.Model):
    students = models.PositiveSmallIntegerField(
        'Количество студентов',
    )
    lessons = models.PositiveSmallIntegerField(
        'Количество занятий'
    )

    class Meta:
        verbose_name = 'Журнал',
        verbose_name_plural = 'Журналы'


class CellImage(models.Model):
    SYMBOL_CHOICE = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('н', 'н')
    )
    image = models.ImageField('Изображение')
    image_array = models.JSONField()
    symbol = models.CharField(
        'Символ',
        choices=SYMBOL_CHOICE,
        max_length=1,
        blank=True
    )

    class Meta:
        verbose_name = 'Изображение ячейки (сырые данные)'
        verbose_name_plural = 'Изображения ячеек (сырые данные)'

