# -*- coding: utf-8 -*-

import string
from django.db import models


class URL(models.Model):
    hashcode = models.CharField(max_length=10, unique=True,
                                db_index=True, null=True)
    longurl = models.CharField(max_length=1024, unique=True,
                               db_index=True, null=True)
    views = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(null=True)
    data = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if URL.objects.count():
            last = URL.objects.latest('id').pk + 1
            alphabet = string.digits + string.ascii_lowercase
            base36 = ''
            if last < len(alphabet):
                self.hashcode = alphabet[last]
            while last != 0:
                last, i = divmod(last, len(alphabet))
                base36 = alphabet[i] + base36
            self.hashcode = base36
        else:
            self.hashcode = '1'
        super(URL, self).save(*args, **kwargs)

    def short_url(self, request):
        return ''.join([
            request.scheme,
            '://', request.get_host(),
            '/', self.hashcode,
        ])

    def __unicode__(self):
        return ' - '.join([self.hashcode, self.longurl])
