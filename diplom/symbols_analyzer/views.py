import cv2
import numpy as np
import io

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView

from .documents import create_paper_gradebook
from .exceptions import BadResolution
from .forms import CreateJournalForm, SymbolAnalyzerForm, UploadBlankImageForm, UploadJournalForm
from .models import CellImage, Journal
from .utils import analyze_image, get_grades, get_row_data

ROTATION = {
    'rotationMinus90': 'cv2.ROTATE_90_COUNTERCLOCKWISE',
    'rotationPlus90': 'cv2.ROTATE_90_CLOCKWISE',
    'rotation180': 'cv2.ROTATE_180'
}

class CreateJournalView(CreateView):
    form_class = CreateJournalForm
    template_name = 'symbols_analyzer/index.html'
    
    def get_success_url(self):
        return reverse('symbols_analyzer:journal', args=(self.object.id,))


class JournalDetailView(View):

    def get_object(self):
        pk = self.kwargs['pk']
        journal = get_object_or_404(Journal, pk=pk)

        return journal

    def get_context(self):
        journal = self.get_object()
        lessons_num = range(1, journal.lessons+1)
        table = []
        for student in range(journal.students):
            name = f'Студент{student}'

            row = [
                name,
                {lesson: '' for lesson in lessons_num}
            ]
            table.append(row)
        
        context = {
            'journal': journal,
            'table': table,
            'lessons_num': lessons_num
        }

        return context

    def get(self, request, pk):
        context = self.get_context()

        return render(request, 'symbols_analyzer/journal.html', context)

    def post(self, request, pk):
        context = self.get_context()
        journal = self.get_object()
        form = UploadJournalForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            image = io.BytesIO(request.FILES['file'].read())
            nparr = np.frombuffer(image.getvalue(), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            rotation = form.cleaned_data['rotation']
            if rotation != 'rotationNone':
                image = cv2.rotate(image, eval(ROTATION[rotation]))
            need_shape = (journal.students+1, journal.lessons+2)
            try:
                result, image = analyze_image(image, need_shape)
                result = get_grades(image, result)
            except BadResolution as error:
                context['error'] = error.message
                return render(request, 'symbols_analyzer/journal.html', context) 


            table = []
            for student in range(journal.students):
                name = f'Студент{student}'

                row = [
                    name,
                    {tup[0]: tup[1] for tup in zip(range(1, journal.lessons+1), result[student])}
                ]
                table.append(row)
            context['table'] = table
        return render(request, 'symbols_analyzer/journal.html', context)


class UploadBlankImageView(View):
    def get(self, request):
        form = UploadBlankImageForm()
        return render(
            request,
            'symbols_analyzer/uploadblank.html', 
            {'form': form}
        )
    
    def post(self, request):
        form = UploadBlankImageForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            image = io.BytesIO(request.FILES['file'].read())
            nparr = np.frombuffer(image.getvalue(), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            rotation = form.cleaned_data['rotation']
            if rotation != 'rotationNone':
                image = cv2.rotate(image, eval(ROTATION[rotation]))
            result, image = analyze_image(image)
            get_row_data(image, result)

        form = UploadBlankImageForm()
        return render(
            request,
            'symbols_analyzer/uploadblank.html', 
            {'form': form}
        )


class SymbolAnalyzerView(View):
    def get(self, request):
        images = CellImage.objects.filter(
            symbol=''
        )
        if images.count() > 0:
            form = SymbolAnalyzerForm(initial={'image_pk': images[0].pk})
            content = {
                'form': form,
                'image': images[0]
            }

            return render(
                request,
                'symbols_analyzer/symbolanalyzer.html', 
                content
            )

    def post(self, request):
        form = SymbolAnalyzerForm(request.POST)
        if form.is_valid():
            image_pk = form.cleaned_data['image_pk']
            image = CellImage.objects.get(pk=image_pk)

            symbol = form.cleaned_data['symbol']

            if symbol in ('empty', 'error'):
                image.delete()
            else:
                image.symbol = symbol
                image.save()
        
        return HttpResponseRedirect(reverse('symbols_analyzer:symbolanalyzer'))


class GetPaperGradebookView(View):
    def get(self, request, pk):
        journal = get_object_or_404(Journal, pk=pk)
        filename = 'Журнал оценок.xlsx'
        paper_gradebook = create_paper_gradebook(journal)
        response = HttpResponse(
            paper_gradebook,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
