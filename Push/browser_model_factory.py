# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/browser_model_factory.py
# Compiled at: 2019-05-08 17:06:57
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .browser_model import filter_type_for_browser, EmptyBrowserModel, QueryingBrowserModel
from .browser_query import TagBrowserQuery, PathBrowserQuery, PlacesBrowserQuery, SourceBrowserQuery, ColorTagsBrowserQuery
FilterType = Live.Browser.FilterType
PLACES_LABEL = 'Places'

def make_plugins_query():
    return TagBrowserQuery(include=[
     'Plug-Ins'], root_name='plugins', subfolder='Plug-Ins')


def make_midi_effect_browser_model(browser):
    midi_effects = TagBrowserQuery(include=['MIDI Effects'], root_name='midi_effects')
    max = TagBrowserQuery(include=[['Max for Live', 'Max MIDI Effect']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[
     color_tags, midi_effects, max, plugins, places])


def make_audio_effect_browser_model(browser):
    audio_effects = TagBrowserQuery(include=['Audio Effects'], root_name='audio_effects')
    max = TagBrowserQuery(include=[['Max for Live', 'Max Audio Effect']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[
     color_tags, audio_effects, max, plugins, places])


def make_instruments_browser_model(browser):
    instrument_rack = PathBrowserQuery(path=['Instruments', 'Instrument Rack'], root_name='instruments')
    drums = SourceBrowserQuery(include=['Drums'], exclude=[
     'Drum Hits'], subfolder='Drum Rack', root_name='drums')
    instruments = TagBrowserQuery(include=['Instruments'], exclude=[
     'Drum Rack', 'Instrument Rack'], root_name='instruments')
    drum_hits = TagBrowserQuery(include=[['Drums', 'Drum Hits']], subfolder='Drum Hits', root_name='drums')
    max = TagBrowserQuery(include=[['Max for Live', 'Max Instrument']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[
     color_tags, instrument_rack, drums, instruments,
     max, drum_hits, plugins, places])


def make_drum_pad_browser_model(browser):
    drums = TagBrowserQuery(include=[['Drums', 'Drum Hits']], root_name='drums')
    samples = SourceBrowserQuery(include=['Samples'], subfolder='Samples', root_name='samples')
    instruments = TagBrowserQuery(include=['Instruments'], root_name='instruments')
    max = TagBrowserQuery(include=[['Max for Live', 'Max Instrument']], subfolder='Max for Live', root_name='max_for_live')
    plugins = make_plugins_query()
    places = PlacesBrowserQuery(subfolder=PLACES_LABEL)
    color_tags = ColorTagsBrowserQuery()
    return QueryingBrowserModel(browser=browser, queries=[
     color_tags, drums, samples, instruments, max, plugins, places])


def make_fallback_browser_model(browser):
    return EmptyBrowserModel(browser=browser)


def make_browser_model(browser, filter_type=None):
    u"""
    Factory that returns an appropriate browser model depending on the
    browser filter type and hotswap target.
    """
    factories = {FilterType.instrument_hotswap: make_instruments_browser_model, 
       FilterType.drum_pad_hotswap: make_drum_pad_browser_model, 
       FilterType.audio_effect_hotswap: make_audio_effect_browser_model, 
       FilterType.midi_effect_hotswap: make_midi_effect_browser_model}
    if filter_type == None:
        filter_type = filter_type_for_browser(browser)
    return factories.get(filter_type, make_fallback_browser_model)(browser)