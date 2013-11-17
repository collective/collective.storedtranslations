Introduction
============

This package allows you to add translations in the Plone registry.


Usage
-----

- Add it to the eggs of your zope instance.

- Install it in the add-ons control panel.

- Go to the configuration registry, filter on
  collective.storedtranslations, and add a domain (for example
  `plone`) with a language code (for example `nl` for
  Dutch/Netherlands) and some message ids and message strings
  (translations).

If you have picked the correct domain, language and message id, then
your translation should show up in the user interface.


Configuration of supported domains and languages
------------------------------------------------

Some information needs to be available when Zope starts up: we need to
know which domains and which languages to support.  We look for
definitions of these in environment variables::

  collective_storedtranslations_domains
  zope_i18n_allowed_languages

We expect that you use a buildout to configure your Plone Site.  You
would need to add those environment variables to your buildout config
then, something like this:

  [instance]
  environment-vars =
       zope_i18n_allowed_languages en de es fr nl
       collective_storedtranslations_domains plone collective.storedtranslations

This would register languages English, German, Spanish, French and
Dutch, for the domains `plone` and `collective.storedtranslations`.


Overriding translations
-----------------------

The translations that you add in this way are not meant for overriding
existing translations.This will not work, at least not for
translations in the `plone` domain.  The given translations are extra.

