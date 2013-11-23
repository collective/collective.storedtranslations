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

    store_untranslated = schema.Bool(
        title=_(u'Store untranslated messages'),
        description=_(u'Create empty entry for untranslated strings. '
                      u'Click around on your website and entries get '
                      u'created automatically.'),
        default=False)


class ITranslationDomain(Interface):

    messages = schema.Dict(
        title=_(u'Messages'),
        key_type=schema.TextLine(title=u'Message ID'),
        value_type=schema.TextLine(title=u'Message String'))
