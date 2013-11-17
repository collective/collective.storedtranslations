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
know which domains and which languages to support.


