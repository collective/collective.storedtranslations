from collective.storedtranslations import _
from zope import schema
from zope.interface import Interface


class IStoredTranslationsSettings(Interface):

    use_stored_translations = schema.Bool(
        title=_(u'Use stored translations'),
        default=True)

    show_untranslated = schema.Bool(
        title=_(u'Show untranslated messages'),
        description=_(u'Show strings that can be translated but have no '
                      u'translation. Warning: this will look ugly.'),
        default=False)
