from Blocks import Block
import Progressions
import Bands
import Blocks
import Movements
import Musicians
from Movements import Movement
from Instrument import Instrument
from optparse import OptionParser
from os import sys
from mingus.core import diatonic
from Sequencer import Sequencer


UPLOAD_HOME = "http://improviser.onderstekop.nl/"
UPLOAD_SONG = 1
UPLOAD_PROGRESSION = 2
UPLOAD_INSTRUMENTS = 3
UPLOAD_BLOCKS = 4


class OptionError(Exception):
	pass

def get_available_bands():
	return [x for x in Bands.__dict__ if \
		type(getattr(Bands, x)) == type([])]

def get_available_progressions():
	return [x for x in Progressions.__dict__ if \
		type(getattr(Progressions, x)) == type([]) and \
		x[0] != "_"]

def get_available_instruments():
	return [x for x in Bands.__dict__ if \
		type(getattr(Bands, x)) == type(Instrument) and \
		issubclass(getattr(Bands,x), Instrument)]


def get_available_blocks():
	return [x for x in Blocks.__dict__ if \
		type(getattr(Blocks, x)) == type(Block) and \
		issubclass(getattr(Blocks,x), Block)]


def get_available_movements():
	return [x for x in Movements.__dict__ if \
		type(getattr(Movements,x)) == type(Movement) and \
		issubclass(getattr(Movements, x), Movement)]


def check_options(test, test_func, test_str, module):
	"""Returns test in module if it can be found in the list or \
iterator generated by test_func. """

	if test != None:
		if test in test_func():
			return getattr(module, test)
		else:
			return False
	return False


def get_options():
	parser = OptionParser()
	parser.add_option("-a", "--audio_driver", dest="driver",
		help="The driver ['oss', 'alsa', 'jack', 'portaudio', 'sndmgr', 'coreaudio', 'Direct Sound']")
	parser.add_option("-b", "--bpm", dest="bpm", type="int",
		default=120,help="Set the bpm to start with.")

	parser.add_option("--blocks", dest="blocks", default="Block",
		help="Set blocks separated by comma.")

	parser.add_option("-d", "--duration", dest="duration", type="int",
		help="Set the number of times the progression should be \
		repeated.", default=1)

	parser.add_option("-e", "--ensemble", dest="ensemble",
		metavar="EN", help="Set the ensemble")

	parser.add_option("-f", "--frontend", dest="frontend",
		metavar="F", help="Choose front-end [blocks, cli, lines, mixed]")
	parser.add_option("--height", dest='height', type='int',
		default=400, help='Height of the visualization screen')

	parser.add_option("-i", "--instruments",
		help="Set instrument(s), separate by comma.",
		dest="instrument")

	parser.add_option("-k", "--key", dest="key", default='C',
		help="Set the default key.")

	parser.add_option("-l", "--list", dest="list",
		help="List [blocks, ensembles, progressions, \
		instruments, movements]. Don't play.")

	parser.add_option("--loop", dest="loop", type="int",
		default=1, help="The number of times the movements should\
		be repeated")

	parser.add_option("-m", "--movement", dest="movement",
		help="Set the movement.")

	parser.add_option("-n", "--no-fluidsynth", dest="no_fluidsynth",
		action="store_true", default=False,
		help="Don't connect to a fluidsynth server, \
		just write the midi file."),

	parser.add_option("-o", "--output-file", dest="midifile",
		help="The file to write the midi to.",
		default="improviser.mid"),

	parser.add_option("-p", "--progression",
		dest="progression", default="reincarnatie",
		help="Set the progression(s), separate by comma.")

	parser.add_option("-r", "--resolution", dest="resolution",
		default=8, type="int", help="The default resolution \
		[1,2,4,8,16,32,etc]")

	parser.add_option("-q", "--quiet", action="store_false",
		dest="verbose", default=True,
		help="Don't output to stdout")

	parser.add_option("-s", "--swing", action="store_true",
		dest="swing", default=False, help="Set swing")

	parser.add_option("--sf2", dest="SF2", default="default.sf2", 
		help="The soundfont to load.")

	parser.add_option("-w", "--wildness", type="float", dest="wild",
		help="Floating point number indicating wildness",
		default=0.5)

	parser.add_option("--width", dest="width", default=400,
		type="int", help="Width of the visualization screen")

	return parser.parse_args()


def save_options(filename, options):
	fp = open(filename, "w")
	fp.write(get_song_as_text(options))
	fp.close()

def get_song_as_text(options):
	res =  "# Improviser configuration\n"
	res += "conf_version = 11\n"
	for x in options.__dict__:
		res += "%s = %s\n" % (x, getattr(options, x))
	return res


def load_options_from_file(filename, option_class):
	version = -1
	f = open(filename, "r")
	o = option_class
	handled = []
	for line in f.readlines():
		if line[0] != "#": #no comment
			parts = line.split("=")
			if len(parts) == 2:
				attr = parts[0]
				val = parts[1]

				# Remove whitespace
				if attr[-1] == " ":
					attr = attr[:-1]
				if val[0] == " ":
					val = val[1:]

				if val[-1] == '\n':
					val = val[:-1]
				if len(val) != 0 and val[-1] == '\r':
					val = val[:-1]

				# Parse attributes
				if attr == "conf_version":
					if int(val) > 11 or int(val) < 0:
						raise OptionError, "Cannot handle version %d." % int(val)
					else:
						version = int(val)
				elif attr in ["bpm", "duration",
					"resolution", "loop", "swing",
					"no_fluidsynth"]:
					try:
						setattr(o, attr, int(val))
					except:
						raise OptionError, "Integer value expected for '%s'" % attr
				elif attr in ["blocks", "instrument",
						"progression", "SF2",
						"key", "project",
						"midifile", "driver", "frontend",
						"author", "movement"]:
					setattr(o, attr, val)
				elif attr == "wild":
					o.wild = float(val)
				else:
					print "Unknown attribute", attr
				handled.append(attr)

			else:
				raise OptionError, "Not a valid imp file."

	if version == -1:
		raise OptionError, "Unknown file version."

	if version <= 7:
		o.movement = "Movement"

	for x in ["bpm", "duration", "conf_version", "resolution", "loop",
		 "swing", "no_fluidsynth", "blocks", "instrument",
		 "progression", "SF2", "key", "project", "midifile",
		 "wild"]:
		if x not in handled:
			raise OptionError, "Missing attribute '%s' in imp file '%s'." % (x, filename)

	return o



def get_movement(options):
	b = check_options(options.movement, get_available_movements,
		"movement", Movements)
	if b != False:
		movement = b()
	else:
		movement = Movement()
	movement.swing = options.swing
	movement.default_resolution = options.resolution
	movement.default_bpm = options.bpm
	movement.default_wildness = options.wild
	movement.loop = options.loop
	if options.key in diatonic.basic_keys:
		movement.default_key = options.key
	return movement

def get_blocks(options):
	res = []
	for block in options.blocks.split(","):
		parts = block.split(" ")
		block = parts[0]
		params = parse_block_params(parts[1:])

		b = check_options(block, get_available_blocks,
			"block", Blocks)
		if b != False:
			block = b()
			for x in ["bpm", "resolution", "duration", "swing", "key", "wild"]:
				if x in params:
					setattr(block, x, params[x])
			res.append(block)
		else:
			if block != "":
				raise OptionError, "Unknown block '%s'" % block
	if res == []:
		b = Block()
		res = [b]
	return res

def get_visualization(options):
	w = options.width
	h = options.height

	if options.frontend == "blocks":
		from Visualizations import PygameBlockVisualization
		visual = PygameBlockVisualization(w,h)
	elif options.frontend == "lines":
		from Visualizations import PygameLineVisualization
		visual = PygameLineVisualization(w,h)
	elif options.frontend == "mixed":
		from Visualizations import PygameMixedVisualizations
		visual = PygameMixedVisualizations(w,h)
	elif options.frontend == "cli":
		from Visualizations import DefaultVisualization
		visual = DefaultVisualization()
	else:
		return None

	return visual

def list_arguments(options):

	if options.list != None:
		if options.list == "ensembles" or \
			options.list[0] == 'e':
			i = 1
			for x in get_available_bands():
				print "%d. %s" % (i, x)
				i += 1
		elif options.list == "progressions" or\
			options.list[0] == 'p':
			i = 1
			for x in get_available_progressions():
				print "%d. %s" % (i, x)
				i += 1
		elif options.list == "instruments" or\
			options.list[0] == 'i':
			i = 1
			for x in get_available_instruments():
				print "%d. %s" % (i, x)
				i += 1
		elif options.list == "blocks" or\
			options.list[0] == 'b':
			i = 1
			for x in get_available_blocks():
				print "%d. %s" % (i, x)
				i += 1
		elif options.list == "movements" or\
			options.list[0] == 'm':
			i = 1
			for x in get_available_movements():
				print "%d. %s" % (i, x)
				i += 1
		else:
			print "Unknown list", options.list
		sys.exit(0)



def set_ensemble(options, block):
	b = check_options(options.ensemble, get_available_bands,
			"ensemble", Bands)
	if b != False:
		if not options.no_fluidsynth:
			for i in b:
				i.reset()
				i.import_fluidsynth()
		block.instruments = b


def set_progressions(options, movement):
	movement.progressions = []
	for prog in options.progression.split(","):
		movement.add_progression(parse_progression(prog))

def set_instrument(options, movement):

	if options.instrument != None:
		c = 1
		for inst in options.instrument.split(","):
			inst = inst.split(" ")
			algo = inst[0]
			params = inst[1:]

			if algo in get_available_instruments():
				i = getattr(Musicians, algo)
				p = parse_instrument_params(params)
				if 'channel' not in p:
					p["channel"] = c
				i = i(p)
				i.reset()
				if not options.no_fluidsynth:
					i.import_fluidsynth()
					i.no_fluidsynth = options.no_fluidsynth
				c += 1
				movement.instruments += [i]
			else:
				if options.verbose:
					raise OptionError, \
					"Unknown instrument '%s'" % algo

def parse_instrument_params(params):
	if len(params) == 0:
		return {}
	if params[0] != "{" or params[-1] != "}":
		raise OptionError, "Syntax error in instrument parameters. Need to open and close with curly brackets."

	params = params[1:-1]
	res = {}
	for p in params:
		try:
			key, value = p.split(":")
		except:
			raise OptionError, "Syntax error in instrument parameters."
		if key in ["max_velocity", "min_velocity", "midi_instr", "channel",
				"let_ring", "note_length", "step", "start", "end",
				"global_end",
				"max_notes", "min_note_length", "min_note", "max_note"]:
			res[key] = int(value)
		elif key in ["chance"]:
			res[key] = float(value)
		elif key in ["must_play", "must_not_play"]:
			res[key] = value
		else:
			res[key] = value
	return res

def parse_block_params(params):
	if len(params) == 0:
		return {}
	if params[0] != "{" or params[-1] != "}":
		raise OptionError, "Syntax error in block parameters. Need to open and close with curly brackets."

	params = params[1:-1]
	res = {}
	for p in params:
		parts = p.split(":")
		key = parts[0]
		if key in ["bpm", "duration", "resolution", "swing"]:
			res[key] = int(parts[1])
		elif key in ["wild"]:
			res[key] = float(parts[1])
		elif key in ["key"]:
			res[key] = parts[1]
		else:
			res[key] = value
	return res


def parse_progression(prog_str):
	p = str(prog_str)
	p = p.split(" ")
	if len(p) == 0:
		return [(0, 'I'), (1, 'R')]
	elif len(p) == 1:
		b = check_options(p[0], get_available_progressions,
			"progression", Progressions)
		if b != False:
			return b
		else:
			if p[0] == "":
				raise OptionError, "No progressions selected."
			raise OptionError, "Unknown progression '%s'." % p[0]

	if p[1] != "{" or p[-1] != "}":
		raise OptionError, "Syntax error in progression parameters. Need to open and close with curly brackets."

	params = p[2:-1]
	res = []
	place = 0
	for x in params:
		if x != "":
			parts = x.split("*")
			progression = parts[1].split("-")
			prog = []
			for p in progression:
				prog.append(p)
			res.append((place, prog))
			place += int(parts[0])
	if res != []:
		res.append((place, 'R'))
	else:
		return [(0, 'I'), (1, 'R')]
	return res


def progression_to_string(prog):
	last_place = 0
	last_r = ""
	res = "{ "
	for p in prog:
		start = int(p[0])
		if last_r != "":
			res += "%d*%s " % (start - last_place, last_r)
		last_r = reduce(lambda x,y: "%s-%s" % (x, y), p[1])
		last_place = start
	res += "}"
	return res

def set_block_options(options, block):

	if block.key == "Default":
		if options.key in diatonic.basic_keys:
			block.key = options.key
		else:
			raise OptionError, "Invalid key '%s'" % options.key
	else:
		if block.key not in diatonic.basic_keys:
			raise OptionError, "Invalid key '%s'" % options.key

	if block.bpm == 0:
		block.bpm = int(options.bpm)
	if block.duration == 0:
		block.duration = int(options.duration)
	if block.wildness == 0.0:
		block.wildness = options.wild
	if block.resolution == 0:
		block.resolution = int(options.resolution)
	if block.swing == "Default":
		block.swing = bool(options.swing)

def load_fluidsynth(options):
	if not options.no_fluidsynth:
		try:
			from mingus.midi import fluidsynth
		except ImportError, msg:
			raise OptionError, msg
		except:
			raise OptionError, "Couldn't load the FluidSynth bindings in mingus. Are you sure FluidSyth has been installed?"
		if hasattr(options, 'driver'):
			driver = options.driver
		else:
			driver = None
		if not fluidsynth.init(options.SF2, driver):
			raise OptionError, "Couldn't load '%s'." % options.SF2

def get_sequencer_from_cli():

	options, args = get_options()
	list_arguments(options)
	return get_sequencer(options)

def get_sequencer(options):
	movement = get_movement(options)
	movement.blocks = []
	movement.instruments = []
	set_ensemble(options, movement)
	set_instrument(options, movement)
	blocks = get_blocks(options)
	visual = get_visualization(options)

	for block in blocks:
		set_ensemble(options, block)
		set_block_options(options,block)
		movement.add_block(block)

	set_progressions(options, movement)

	load_fluidsynth(options)



	if movement.instruments == []:
		raise OptionError, "No instruments or ensemble selected."

	for x in movement.instruments:
		x.no_fluidsynth = options.no_fluidsynth

	seq = Sequencer(movement)
	seq.verbose = options.verbose
	seq.no_fluidsynth = options.no_fluidsynth
	seq.output_file = options.midifile
	if visual != None:
		seq.paint_function = visual.paint_screen
		seq.tick_function = visual.tick
		seq.update_function = visual.update_screen
	return seq
