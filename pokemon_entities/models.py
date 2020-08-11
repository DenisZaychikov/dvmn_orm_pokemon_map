from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    image = models.ImageField(verbose_name='Картинка')
    title_en = models.CharField(max_length=200, default='', blank=True, verbose_name='Имя на английском')
    title_jp = models.CharField(max_length=200, default='', blank=True, verbose_name='Имя на японском')
    description = models.TextField(default='', blank=True, verbose_name='Описание')
    evolved_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Эволлюционировал из',
        related_name='next_evolutions',
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='entities')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Появился')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Исчез')
    level = models.IntegerField(blank=True, null=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True, null=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, null=True, verbose_name='Атака')
    defence = models.IntegerField(blank=True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, verbose_name='Выносливость')

    def __str__(self):
        return self.pokemon.title
