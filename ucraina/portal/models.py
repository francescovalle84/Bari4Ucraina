from django.db import models
from django.utils.timezone import now
import uuid


# Create your models here.
class UfficioCompetente(models.Model):

    nome = models.CharField(max_length=100, help_text="Nome dell'ufficio competente")

    def __str__(self):
        return self.nome


class StatoPrestazione(models.Model):

    descrizione = models.CharField(max_length=30)

    def __str__(self):
        return str(self.descrizione)


class ListaPrestazioni(models.Model):
    descrizione = models.CharField(max_length=100)

    def __str__(self):
        return str(self.descrizione)


class Prestazione(models.Model):

    richiesta = models.ForeignKey("Richiesta", on_delete=models.CASCADE, null=True)
    descrizione = models.ForeignKey("ListaPrestazioni", on_delete=models.CASCADE)
    nota = models.CharField(max_length=100, null=True, blank=True)
    stato = models.ForeignKey("StatoPrestazione", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.descrizione)


class Componente(models.Model):

    richiesta = models.ForeignKey("Richiesta", on_delete=models.CASCADE, null=True)
    cognome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    data_nascita = models.DateField(null=True, blank=True)
    luogo_nascita = models.CharField(max_length=100)
    note = models.TextField(max_length=500, help_text="Specificare rapporto di parentela rispetto al primo componente o altre note rilevanti")

    def __str__(self):
        return self.cognome + ' ' + self.nome + ' (' + self.luogo_nascita + ')'

class Richiesta(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID univoco per la richiesta")
    data_colloquio = models.DateField(null=True, blank=True)
    collocazione_attuale = models.TextField(max_length=1000, blank=True, null=True)
    telefono_1 = models.CharField(max_length=16, blank=True, null=True)
    telefono_1_note = models.CharField(max_length=50, blank=True, null=True)
    telefono_2 = models.CharField(max_length=16, blank=True, null=True)
    telefono_2_note = models.CharField(max_length=50, blank=True, null=True)
    ufficio_competente = models.ForeignKey("UfficioCompetente", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)
