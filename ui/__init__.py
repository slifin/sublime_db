
from .render import *
from .events import (
	GutterEvent,
	HoverEvent,
	ViewEventsListener,
	view_loaded,
	view_activated,
	view_text_hovered,
	view_gutter_hovered,
	view_gutter_double_clicked,
	view_selection_modified,
	view_modified,
	view_drag_select)

from .layout import *
from .component import *
from .image import *
from .segment import *
from .table import *
from .button import *
from .label import *
from .input import *

import os

from sublime_db.libs import asyncio 
from sublime_db import core

def startup () -> None:
	Images.shared = Images()
	dir_path = os.path.dirname(os.path.abspath(__file__))
	import_css(dir_path + '/ui.css')
	_start_render()

def shutdown () -> None:
	_stop_render()
	

_rendering = False
def _start_render() -> None:
	_rendering = True
	
	@core.async
	def _run_render() -> core.awaitable[None]:
		last_time = core.main_loop.time()
		while _rendering:
			time = core.main_loop.time()
			delta = time - last_time
			last_time = time
			update(delta)
			render()
			yield from asyncio.sleep(0.05)
	core.run(_run_render())

def _stop_render() -> None:
	_rendering = False