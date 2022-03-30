from django.db import models
from django.utils.timezone import now
import uuid

# Create your models here.
class UfficioCompetente(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome dell'ufficio competente")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Uffici competenti'


class StatoPrestazione(models.Model):
    descrizione = models.CharField(max_length=30)

    def __str__(self):
        return str(self.descrizione)

    class Meta:
        verbose_name_plural = 'Stato prestazioni'


class ListaPrestazioni(models.Model):
    descrizione = models.CharField(max_length=100)

    def __str__(self):
        return str(self.descrizione)

    class Meta:
        verbose_name_plural = 'Lista prestazioni'


class Prestazione(models.Model):
    richiesta = models.ForeignKey("Richiesta", on_delete=models.CASCADE, null=True)
    descrizione = models.ForeignKey("ListaPrestazioni", on_delete=models.CASCADE)
    nota = models.CharField(max_length=100, null=True, blank=True)
    stato = models.ForeignKey("StatoPrestazione", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.descrizione)

    class Meta:
        verbose_name_plural = 'Prestazioni'


class Componente(models.Model):
    richiesta = models.ForeignKey("Richiesta", on_delete=models.CASCADE, null=True)
    cognome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    data_nascita = models.DateField(null=True, blank=True)
    luogo_nascita = models.CharField(max_length=100)
    note = models.TextField(max_length=500,
                            help_text="Specificare rapporto di parentela rispetto al primo componente o altre note rilevanti")

    def __str__(self):
        return self.cognome + ' ' + self.nome + ' (' + self.luogo_nascita + ')'

    class Meta:
        verbose_name_plural = 'Componenti'


class Richiesta(models.Model):
    id = models.UUIDField(primary_key=True, max_length=5, default=uuid.uuid4, help_text="ID univoco per la richiesta")
    data_colloquio = models.DateField(default=now, blank=False, null=False)
    collocazione_attuale = models.TextField(max_length=1000, null=True)
    telefono_1 = models.CharField(max_length=16, blank=False, null=False)
    telefono_1_note = models.CharField(max_length=50, blank=True)
    telefono_2 = models.CharField(max_length=16, blank=True)
    telefono_2_note = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    ufficio_competente = models.ForeignKey("UfficioCompetente", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id) + \
               str(self.data_colloquio) + \
               str(self.collocazione_attuale) + \
               str(self.telefono_1) + \
               str(self.telefono_1_note) + \
               str(self.telefono_2) + \
               str(self.telefono_2_note) + \
               str(self.email) + \
               str(self.ufficio_competente)

    class Meta:
        verbose_name_plural = 'Richieste'
