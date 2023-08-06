import asyncio
from importlib import util
from jcore.helpers.settings import Settings
from jcore.message import *
import jcore.exceptions
import jcore.jsocket
import jcore
import logging
import os
import sys
import traceback

INTERVAL = 0.001

log = logging.getLogger(__name__)


# todo: 
#   - Copy remaining callbacks over
#   - copy / implement parser + message types
#   - Update socket with parser and new callbacks
#   - Add join function to channel (should load balance against channel list and implement or spin up an additional socket as required.)
#       -> may require load_query? function to be implemented in socket, to check if there's space against `max_connections`



class Client():

    def __init__(self, channel:str = None, channels:list = None, max_connections: int = 50, command_activator: str = "!"):
        log.info(f"Starting new connection with a maximum of `{max_connections}` connections per socket.")
        self.command_activator = command_activator
        self.max_connections_per_socket = max_connections
        self.sockets = []
        self.__modules = {}
        
        # pull channels from settings file.
        settings = Settings()
        if settings.has_key("channels"):
            channel_list = list(settings.get_setting("channels"))
        else:
            channel_list = []
        # if channel is set, attempt to add it to the channels list.
        if channel is not None and channel not in channel_list:
            channel_list.append(channel)
        
        # if channels is set, attempt to add new channels to the list.
        if channels is not None:
            for chn in channels:
                if chn not in channel_list:
                    channel_list.append(chn)
        
        self.loop = asyncio.get_event_loop()
        for segment in self.__segment_channels(channel_list):
            sock = jcore.jsocket.Socket(self, command_activator)
            sock.set_channels(segment)
            self.sockets.append(sock)
        self.__cache_modules()

    async def run(self):
        try:
            loop = asyncio.get_event_loop()
            for sock in self.sockets:
                await sock.connect()
                await asyncio.sleep(0.001)
                loop.create_task(sock.run())
            while True:
                await asyncio.sleep(INTERVAL)
        except KeyboardInterrupt:
            log.debug("Keyboard Interrupt Detected - departing channels.")
            for sock in self.sockets:
                sock.disconnect()

    
    def load_module(self, module):
        self.__modules[module.name] = module


    async def join_channel(self, channel):
        socket: jcore.jsocket.Socket
        for socket in self.sockets:
            if socket.has_channel(channel):
                raise jcore.exceptions.ClientException("Channel has already been joined.")
        for socket in self.sockets:
            if socket.current_connections < (self.max_connections_per_socket * 0.9):
                await socket.join_channel(channel)

    async def depart_channel(self, channel):
        socket: jcore.jsocket.Socket
        for socket in self.sockets:
            if socket.has_channel(channel):
                await socket.depart_channel(channel)
        


    # Callbacks: These can be overwritten to provide functionality in user-built apps.

    async def on_raw(self, message: RawMessage):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass
    
    async def on_message(self, message: Message):
        """Called when a message event is received."""
        # not implemented
        pass
    
    async def on_join(self, message: Join):
        """Called when a JOIN event is received."""
        # not implemented
        pass
    
    async def on_mode(self, message: Mode):
        """Called when a MODE event is received."""
        # not implemented
        pass

    async def on_names(self, message: Names):
        """Called when a NAMES event is received."""
        # not implemented
        pass
        
    async def on_part(self, message: Part):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_clearchat(self, message: ClearChat):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_clearmessage(self, message: ClearMessage):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_hosttarget(self, message: HostTarget):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_notice(self, message: Notice):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_reconnect(self, message: Reconnect):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass


    async def on_roomstate(self, message: RoomState):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_userstate(self, message: UserState):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_globaluserstate(self, message: GlobalUserState):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_usernotice(self, message: UserNotice):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_ritual_usernotice(self, message: RitualUserNotice):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_bitbadgeupgrade_usernotice(self, message: BitBadgeUpgradeUserNotice):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_raid_usernotice(self, message: RaidUserNotice):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_whisper(self, message: Whisper):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_subscriber_usernotice(self, message: SubscriberUserNotice):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_giftedsubscriber_usernotice(self, message: GiftedSubscriberUserNotice):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass
    
    async def on_privmessage(self, message: PrivateMessage):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass

    async def on_command(self, message: CommandMessage):
        """Called when a raw message event is received. Triggers in all cases."""
        # not implemented
        pass
    

    # jcore.jsocket.Socket Callbacks: These are called by the socket when recieving messages.

    async def _scb_on_raw(self, message: RawMessage):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_raw"):
            try:
                self.loop.create_task(module.on_raw(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_raw(message))
    

    async def _scb_on_message(self, message: Message):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_message"):
            try:
                self.loop.create_task(module.on_message(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_message(message))


    async def _scb_on_join(self, message: Join):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_join"):
            try:
                self.loop.create_task(module.on_join(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_join(message))


    async def _scb_on_mode(self, message: Mode):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_mode"):
            try:
                self.loop.create_task(module.on_mode(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_mode(message))

    async def _scb_on_names(self, message: Names):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_names"):
            try:
                self.loop.create_task(module.on_names(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_names(message))

    async def _scb_on_part(self, message: Part):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_part"):
            try:
                self.loop.create_task(module.on_part(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_part(message))

    async def _scb_on_clearchat(self, message: ClearChat):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_clearchat"):
            try:
                self.loop.create_task(module.on_clearchat(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_clearchat(message))

    async def _scb_on_clearmessage(self, message: ClearMessage):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_clearmessage"):
            try:
                self.loop.create_task(module.on_clearmessage(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_clearmessage(message))

    async def _scb_on_hosttarget(self, message: HostTarget):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_hosttarget"):
            try:
                self.loop.create_task(module.on_hosttarget(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_hosttarget(message))

    async def _scb_on_notice(self, message: Notice):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_notice"):
            try:
                self.loop.create_task(module.on_notice(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_notice(message))

    async def _scb_on_reconnect(self, message: Reconnect):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_reconnect"):
            try:
                self.loop.create_task(module.on_reconnect(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_reconnect(message))

    async def _scb_on_roomstate(self, message: RoomState):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_roomstate"):
            try:
                self.loop.create_task(module.on_roomstate(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_roomstate(message))

    async def _scb_on_userstate(self, message: UserState):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_userstate"):
            try:
                self.loop.create_task(module.on_userstate(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_userstate(message))

    async def _scb_on_global_userstate(self, message: GlobalUserState):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_global_userstate"):
            try:
                self.loop.create_task(module.on_global_userstate(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_global_userstate(message))

    async def _scb_on_usernotice(self, message: UserNotice):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_usernotice"):
            try:
                self.loop.create_task(module.on_usernotice(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_usernotice(message))

    async def _scb_on_ritual_usernotice(self, message: RitualUserNotice):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_ritual_usernotice"):
            try:
                self.loop.create_task(module.on_ritual_usernotice(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_ritual_usernotice(message))

    async def _scb_on_bitbadgeupgrade_usernotice(self, message: BitBadgeUpgradeUserNotice):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_bitbadgeupgrade_usernotice"):
            try:
                self.loop.create_task(module.on_bitbadgeupgrade_usernotice(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_bitbadgeupgrade_usernotice(message))

    async def _scb_on_raid_usernotice(self, message: RaidUserNotice):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_raid_usernotice"):
            try:
                self.loop.create_task(module.on_raid_usernotice(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_raid_usernotice(message))

    async def _scb_on_whisper(self, message: Whisper):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_whisper"):
            try:
                self.loop.create_task(module.on_whisper(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_whisper(message))

    async def _scb_on_subscriber_usernotice(self, message: SubscriberUserNotice):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_subscriber_usernotice"):
            try:
                self.loop.create_task(module.on_subscriber_usernotice(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_subscriber_usernotice(message))

    async def _scb_on_giftedsubscriber_usernotice(self, message: GiftedSubscriberUserNotice):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_giftedsubscriber_usernotice"):
            try:
                self.loop.create_task(module.on_giftedsubscriber_usernotice(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_giftedsubscriber_usernotice(message))

    async def _scb_on_privmessage(self, message: PrivateMessage):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_privmessage"):
            try:
                self.loop.create_task(module.on_privmessage(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_privmessage(message))

    async def _scb_on_command(self, message: CommandMessage):
        # parse modules and queue tasks
        for module in self.__get_module_with_handler("on_command"):
            try:
                self.loop.create_task(module.on_command(message))
            except Exception as e:
                log.exception(f"Suppressing a caught an exception, will continue without raising. Details below\n{type(e)}: {traceback.format_exc()}")
        # call local callback
        self.loop.create_task(self.on_command(message))





    # Internal Functions: Internal functions used to make the system work

    def __segment_channels(self, channels):
        return_list = []
        counter = 0
        for channel in channels:
            if counter < self.max_connections_per_socket:
                return_list.append(channel)
                counter +=1 
            else:
                counter = 0
                yield return_list
                return_list = []
        yield return_list


    def __cache_modules(self):
        modules = []
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'modules/')):
            log.debug("Loading core modules")
            for _file in os.listdir(os.path.join(os.path.dirname(__file__), 'modules/')):
                if "__" not in _file:
                    # print ("r1: Found: ", _file)
                    filename, ext = os.path.splitext(_file)
                    if '.py' in ext:
                        modules.append(f'jcore.modules.{filename}')
        
        if os.path.exists("modules/"):
            log.info("Loading custom modules")
            for _file in os.listdir('modules/'):
                if "__" not in _file:
                    log.debug(f"Found: {_file}")
                    filename, ext = os.path.splitext(_file)
                    if '.py' in ext:
                        log.info(f"Loaded custom module `{_file}`")
                        modules.append(f'modules.{filename}')
        
        if os.path.exists("bots/twitch/modules/"):
            log.debug("Loading custom jarvis modules")
            for _file in os.listdir('bots/twitch/modules/'):
                if "__" not in _file:
                    log.debug(f"Found jarvis module: {_file}")
                    filename, ext = os.path.splitext(_file)
                    if '.py' in ext:
                        modules.append(f'bots.twitch.modules.{filename}')

        for extension in reversed(modules):
            try:
                self._load_module(f'{extension}')
            except Exception as e:
                try:
                    # extension = extension.replace("jcore", "JarvisCore")
                    log.warn("module load failed, re-attempting to load: ", extension)
                    self._load_module(f'{extension}')
                except Exception as e:
                    exc = f'{type(e).__name__}: {e}'
                    log.error(f'Failed to load extension {extension}\n{exc}')
        

    def _load_module(self, module):
        if module in self.__modules:
            raise jcore.exceptions.ExtensionAlreadyLoaded(module)

        spec = util.find_spec(module)
        if spec is None:
            raise jcore.exceptions.ExtensionNotFound(module)

        self._load_from_module_spec(spec, module)

    
    def _load_from_module_spec(self, spec, key):
        lib = util.module_from_spec(spec)
        sys.modules[key] = lib
        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            del sys.modules[key]
            raise jcore.exceptions.ExtensionFailed(key, e) from e

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            del sys.modules[key]
            raise jcore.exceptions.NoEntryPointError(key)

        try:
            setup(self)
        except Exception as e:
            del sys.modules[key]
            self._call_module_finalizers(lib, key)
            raise jcore.exceptions.ExtensionFailed(key, e) from e
        else:
            self.__modules[key] = lib

    

    def _call_module_finalizers(self, lib, key):
        try:
            teardown = getattr(lib, 'teardown')
        except AttributeError:
            pass
        else:
            try:
                teardown(self)
            except Exception:
                pass
        finally:
            self.__modules.pop(key, None)
            sys.modules.pop(key, None)

    def __get_module_with_handler(self, handler: str):
        for module in self.__modules:
            try:
                if hasattr(self.__modules[module], handler):
                    yield self.__modules[module]
            except AttributeError:
                pass



