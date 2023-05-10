from django.contrib import admin

from .models import SkiPass, Month, RidingLevel
from .models import SkiResort
from .models import SkiLifts
from .models import SkyTrail


admin.site.register(SkiPass)
admin.site.register(SkiResort)
admin.site.register(SkiLifts)
admin.site.register(SkyTrail)
admin.site.register(Month)
admin.site.register(RidingLevel)
