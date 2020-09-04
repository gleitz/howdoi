#!/usr/bin/env python

######################################################
#
# howdoi - instant coding answers via the command line
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
######################################################

from __future__ import print_function

import gc
import inspect
import os
import pkgutil
import sys

from howdoi.utils import (
    STASH_EMPTY,
    STASH_REMOVE,
    STASH_SAVE,
    STASH_VIEW,
    SUPPORTED_SEARCH_ENGINES,
    _clear_cache,
    _print_err,
    _print_ok,
    cache,
    get_parser,
    howdoi_session,
    keep_utils,
    print_stash,
    prompt_stash_remove,
)

from . import __version__

gc.disable()  # noqa: E402


def command_line_runner():
    plugins = HowDoi("plugins").plugins
    parser = get_parser()

    args = vars(parser.parse_args())

    if args["version"]:
        _print_ok(__version__)
        return

    if args["clear_cache"]:
        if _clear_cache():
            _print_ok("    Cache cleared successfully")
        else:
            _print_err("    Clearing cache failed")

    if args[STASH_VIEW]:
        print_stash()
        return

    if args[STASH_EMPTY]:
        os.system("keep init")
        return

    if args[STASH_REMOVE] and len(args["query"]) == 0:
        commands = keep_utils.read_commands()
        if commands is None or len(commands.items()) == 0:
            print(
                'No commands found in stash. Add a command with "howdoi --{stash_save} <query>".'.format(
                    stash_save=STASH_SAVE
                )
            )
            return
        stash_list = [
            {"command": cmd, "fields": field} for cmd, field in commands.items()
        ]
        prompt_stash_remove(args, stash_list)
        return

    if not args["query"]:
        parser.print_help()
        return

    if os.getenv("HOWDOI_COLORIZE"):
        args["color"] = True

    if not args["search_engine"] in SUPPORTED_SEARCH_ENGINES:
        _print_err(
            "Unsupported engine.\nThe supported engines are: %s"
            % ", ".join(SUPPORTED_SEARCH_ENGINES)
        )
        return
    elif args["search_engine"] != "google":
        os.environ["HOWDOI_SEARCH_ENGINE"] = args["search_engine"]

    # Walk plugin directory and run individual plugins against query.
    # TODO: (mwizasimbeye11) Enable default plugins.
    # TODO: (mwizasimbeye11) Check if args for specific plugins have been passed.
    for plugin in plugins:
        plugin.raw_query = args
        utf8_result = plugin.howdoi(args, parser, cache).encode("utf-8", "ignore")

        # utf8_result = howdoi(args).encode("utf-8", "ignore")
        if sys.version < "3":
            print(utf8_result)
        else:
            # Write UTF-8 to stdout: https://stackoverflow.com/a/3603160
            sys.stdout.buffer.write(utf8_result)
        # close the session to release connection
    howdoi_session.close()


class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        self.description = "UNKNOWN"
        self.raw_query = ""

    def _get_answers(self, args):
        return NotImplementedError

    def _get_answer(self, args, links):
        return NotImplementedError

    def howdoi(self, raw_query, parser):
        return NotImplementedError


class HowDoi:
    """Walks the default plugin folder and looks for plugins and applys the query to it.
    """

    def __init__(self, plugin_package):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package = plugin_package
        self.reload_plugins()

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.plugins = []
        self.seen_paths = []
        print()
        print(f"Looking for plugins under package {self.plugin_package}")
        self.walk_package(self.plugin_package)

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, globals(), fromlist=["blah"], level=1)

        for _, pluginname, ispkg in pkgutil.iter_modules(
            imported_package.__path__, imported_package.__name__ + "."
        ):
            if not ispkg:
                plugin_module = __import__(pluginname, globals(), fromlist=["blah"])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # TODO: Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    # TODO: use issubclass() function to check if plugin is subclass.
                    # if issubclass(Plugin, c):
                    if str(c.__base__.__name__) == "Plugin":
                        print(f"    Found plugin class: {c.__module__}.{c.__name__}")
                        self.plugins.append(c())

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [
                    p
                    for p in os.listdir(pkg_path)
                    if os.path.isdir(os.path.join(pkg_path, p))
                ]

                # For each sub directory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + "." + child_pkg)


if __name__ == "__main__":
    command_line_runner()
