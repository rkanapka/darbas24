from django.db import models


class JobOffers(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    salary = models.CharField(max_length=50)
    salary_period = models.CharField(max_length=25)
    salary_calculation = models.CharField(max_length=25)
    location = models.CharField(max_length=50)
    job_link = models.CharField(max_length=2083, default="", unique=True)
    image_link = models.CharField(max_length=2083, default="")
    image_width = models.SmallIntegerField()
    image_height = models.SmallIntegerField()
    offer_upload_date = models.CharField(max_length=50)
    source_link = models.CharField(max_length=30, default="", blank=True, null=True)

    @property
    def category_color(self):
        category_with_color = {
            "Administravimas/darbų sauga": "bg-soft-light-red",
            "Apsauga": "bg-soft-light-orange",
            "Dizainas/architektūra": "bg-soft-light-yellow",
            "Draudimas": "bg-soft-light-lime",
            "Eksportas": "bg-soft-light-mint",
            "Energetika/elektronika": "bg-soft-light-steel-blue",
            "Finansai/apskaita/bankininkystė": "bg-soft-light-pink",
            "Gamyba": "bg-soft-light-purple",
            "Informacinės technologijos": "bg-soft-light-blue",
            "Inžinerija/mechanika": "bg-soft-light-cyan",
            "Klientų aptarnavimas/paslaugos": "bg-soft-light-green",
            "Maisto gamyba": "bg-soft-light-gold",
            "Marketingas/reklama": "bg-soft-light-peach",
            "Medicina/farmacija": "bg-soft-light-lavender",
            "Nekilnojamasis turtas": "bg-soft-light-rose",
            "Pardavimų vadyba": "bg-soft-light-apricot",
            "Personalo valdymas": "bg-soft-light-chartreuse",
            "Pirkimai/tiekimas": "bg-soft-light-turquoise",
            "Prekyba - konsultavimas": "bg-soft-light-cornflower",
            "Sandėliavimas": "bg-soft-soft-red",
            "Statyba": "bg-soft-soft-orange",
            "Švietimas/mokymai/kultūra": "bg-soft-soft-beige",
            "Teisė": "bg-soft-soft-mint",
            "Transporto vairavimas": "bg-soft-soft-pastel-green",
            "Transporto/logistikos vadyba": "bg-soft-soft-lavender-grey",
            "Vadovavimas/kokybės vadyba": "bg-soft-soft-pink",
            "Valstybinis/viešasis administravimas": "bg-soft-soft-lilac",
            "Žemės ūkis": "bg-soft-soft-sky-blue",
            "Žiniasklaida/komunikacija": "bg-soft-soft-aqua",
        }
        return category_with_color[self.category]
