from django.contrib import admin
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook

from .models import Richiesta, Componente, UfficioCompetente, Prestazione, StatoPrestazione, ListaPrestazioni

from django_object_actions import DjangoObjectActions
from openpyxl import Workbook
from openpyxl.worksheet.table import Table
from openpyxl.utils import get_column_letter
import datetime


# Register your models here.
#admin.site.register(Richiesta)
admin.site.register(Componente)
admin.site.register(UfficioCompetente)
admin.site.register(Prestazione)
admin.site.register(StatoPrestazione)
admin.site.register(ListaPrestazioni)


class ComponenteInline(admin.StackedInline):
    model = Componente
    fields = [('cognome', 'nome'), ('luogo_nascita', 'data_nascita'), 'note']
    extra = 0


class PrestazioneInline(admin.StackedInline):
    model = Prestazione
    fields = ['descrizione', 'nota', 'stato']
    extra = 0


class RichiestaAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('get_componenti', 'id', 'data_colloquio', 'telefono_1', 'telefono_1_note', 'telefono_2', 'telefono_2_note', 'collocazione_attuale', 'ufficio_competente')
    fields = [('id', 'data_colloquio'), ('telefono_1', 'telefono_1_note'), ('telefono_2', 'telefono_2_note'), 'collocazione_attuale', 'ufficio_competente']
    inlines = [ComponenteInline, PrestazioneInline]

    def export_excel(modeladmin, request, queryset):
        print("PREMUTO EXPORT")
        """Esportare dati in formato Excel con Datatable"""
        print("ESTRAI TUTTI I DATI")
        report = ''
        wb = Workbook()
        sheet = wb.active
        row = 1
        """AGGIUNGERE INTESTAZIONE FILE"""
        sheet.cell(row=row, column=1).value = "ID RICHIESTA"
        sheet.cell(row=row, column=2).value = "COMPONENTI NUCLEO"
        sheet.cell(row=row, column=3).value = "PRESTAZIONI"

        richieste = Richiesta.objects.all()
        for rich in richieste:
            row = row + 1
            print("RICHIESTA")
            print(rich)
            sheet.cell(row=row, column=1).value = str(rich)
            id_rich = rich.id
            lista_comp = ''
            componenti = Componente.objects.filter(richiesta_id = id_rich)
            for comp in componenti:
                lista_comp += comp.cognome + ' ' + comp.nome + ', '
            lista_comp = lista_comp[:-2]
            sheet.cell(row=row, column=2).value = lista_comp
            print("COMPONENTI")
            print(lista_comp)
            lista_prest = ''
            prestazioni = Prestazione.objects.filter(richiesta_id=id_rich)
            for prest in prestazioni:
                lista_prest += str(prest.descrizione) + ' (' + str(prest.stato.descrizione) + '), '
            lista_prest = lista_prest[:-2]
            sheet.cell(row=row, column=3).value = lista_prest
            print("PRESTAZIONI")
            print(lista_prest)
            print("--------")

        table = Table(displayName="Table1", ref="A1:" + get_column_letter(sheet.max_column) + str(sheet.max_row))

        sheet.add_table(table)

        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/ms-excel', )
        response[
            'Content-Disposition'] = f'attachment; filename=ExportedExcel-{datetime.datetime.now().strftime("%Y%m%d%H%M")}.xlsx'
        return response


    changelist_actions = ("export_excel",)

    def get_componenti(self, instance):
        componenti = Componente.objects.filter(richiesta__id=instance.id)
        result = ''
        for comp in componenti:
            result += comp.cognome + ' ' + comp.nome + ', '
        return result[:-2]

admin.site.register(Richiesta, RichiestaAdmin)
