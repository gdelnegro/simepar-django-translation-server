from django.db import models
from django.utils.translation import ugettext_lazy as _

TRANSLATION_TYPES_CHOICES = (
    ('MDL', _('MDL1')),
    ('TTP', _('MDL2')),
    ('MTA', _('MDL3')),
    ('MTP', _('MDL4')),
    ('GEN', _('MDL5')),
    ('GTP', _('MDL6'))
)


class TranslationType(models.Model):
    created_at = models.DateTimeField(_('MDL7'), auto_now_add=True, null=True, blank=True, help_text=_('TTP7'))
    updated_at = models.DateTimeField(_('MDL8'), auto_now=True, null=True, blank=True, help_text=_('TTP8'))
    tag = models.CharField(_('MDL9'), help_text=_('TTP9'), max_length=20, unique=True)
    name = models.TextField(_('MDL10'), help_text=_('TTP10'))
    has_auxiliary_text = models.BooleanField(_('MDL11'), help_text=_('TTP11'), default=True)
    auxiliary_tag = models.CharField(_('MDL12'), help_text=_('TTP12'), max_length=20, unique=True)

    class Meta:
        verbose_name = _('MTA1')
        verbose_name_plural = _('MTP1')

    def __str__(self):
        return "%s - %s" % (self.tag, self.name)

    def __unicode__(self):
        return "%s - %s" % (self.tag, self.name)


class Translation(models.Model):
    created_at = models.DateTimeField(_('MDL7'), auto_now_add=True, null=True, blank=True, help_text=_('TTP7'))
    updated_at = models.DateTimeField(_('MDL8'), auto_now=True, null=True, blank=True, help_text=_('TTP8'))
    type = models.ForeignKey(TranslationType, on_delete=None, related_name="translation_translation_type",
                             verbose_name=_('MDL13'), help_text=_('TTP13'))
    tag = models.CharField(_('MDL14'), help_text=_('TTP14'), max_length=20, unique=True)
    text = models.TextField(_('MDL15'), help_text=_('TTP15'))
    auxiliary_tag = models.CharField(_('MDL16'), help_text=_('TTP16'), max_length=20, blank=True, null=True)
    auxiliary_text = models.TextField(_('MDL17'), help_text=_('TTP17'), blank=True, null=True)
    migration_created = models.BooleanField(_('MDL18'), help_text=_('TTP18'), default=False)

    class Meta:
        verbose_name = _('MTA2')
        verbose_name_plural = _('MTP2')

    def __str__(self):
        return "%s" % self.tag

    def __unicode__(self):
        return "%s" % self.tag


# @receiver(post_save, sender=Translation, dispatch_uid="update_stock_count")
# def update_translation(sender, instance, **kwargs):
#     from django.core.management import call_command
#     call_command('make_translation')

class LastTranslationTag(object):
    translation_tag = None

    def __init__(self, translation_tag, *args, **kwargs):
        self.translation_tag = translation_tag

    def return_last_tag(self):
        from django.db import connection
        # query = """ SELECT max(tag) FROM portfolio_translation WHERE tag LIKE '%s%%' """ % self.translation_tag
        query = "SELECT tag FROM portfolio_translation WHERE tag LIKE '%(translation_tag)s%%' ORDER BY NULLIF(regexp_replace(TAG, E'\\\\D', '', 'g'), '')::int DESC LIMIT 1" % {
            'translation_tag': self.translation_tag}
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except Exception as err:
            raise err
        else:
            result = []
            for row in cursor.fetchall():
                result = row[0]
            if result:
                import re
                tag = Translation.objects.get(tag=result)
                return dict(result=dict(last_tag=result, last_id=re.findall("(\d+)", result)[0], type=tag.type.name,
                                        has_auxiliary_text=tag.type.has_auxiliary_text,
                                        auxiliary_tag=tag.type.auxiliary_tag, tag=tag.type.tag))
            else:
                return dict(result=dict())
