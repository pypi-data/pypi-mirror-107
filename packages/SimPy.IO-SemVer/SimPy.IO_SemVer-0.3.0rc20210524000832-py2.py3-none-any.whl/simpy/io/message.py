import traceback
import errno
import socket
import traceback

from itertools import count
from simpy.events import Event, Process
from simpy.io.codec import JSON
from simpy.io.network import RemoteException

REQUEST = 0
SUCCESS = 1
FAILURE = 2

UNCRITICAL_ERRORS = (errno.ECONNRESET, errno.EBADF, errno.ENOTCONN)


class MessageOverflowError(Exception):
    pass


class InMessage(Event):
    def __init__(self, message, id, content):
        Event.__init__(self, message.env)
        self.message = message
        self.id = id
        self.content = content


class OutMessage(Event):
    def __init__(self, message, id, content):
        Event.__init__(self, message.env)
        self.message = message
        self.id = id
        self.content = content


class Message(object):
    # TODO Rename class and module (channel)?

    def __init__(self, env, socket, codec=None, message_limit=1024):
        self.env = env
        self.socket = socket
        if codec is None:
            codec = JSON()
        self.codec = codec
        self.message_limit = message_limit

        self._message_id = count()
        self._in_queue = []
        self._out_queue = []
        self._in_messages = {}
        """Maps incoming message objects to ids."""
        self._out_messages = {}
        """Maps outgoing message ids to objects."""

        self._send_ev = None
        self._recv_ev = None

        self.reader = Process(self.env, self._reader())
        self.reader.callbacks.append(self._handle_error)
        self.writer = Process(self.env, self._writer())
        self.writer.callbacks.append(self._handle_error)

    def _reader(self):
        buffer = b''
        while True:
            data = yield self.socket.read()

            msg_type, msg_id, content = self.codec.decode(data)

            if msg_type == REQUEST:
                message = InMessage(self, msg_id, content)
                message.callbacks.append(self._reply)
                if len(self._in_messages) >= self.message_limit:
                    # Close the connection if the maximum number of incoming
                    # messages is reached.
                    self.close()
                    raise MessageOverflowError(
                            'Incoming message limit of %d has been '
                            'exceeded' % self.message_limit)
                self._in_messages[message] = msg_id
                if self._recv_ev is not None:
                    self._recv_ev.succeed(message)
                    self._recv_ev = None
                else:
                    self._in_queue.append(message)
            elif msg_type == SUCCESS:
                self._out_messages.pop(msg_id).succeed(content)
            elif msg_type == FAILURE:
                try:
                    raise RemoteException(self, content)
                except BaseException as e:
                    self._out_messages.pop(msg_id).fail(e)
            else:
                raise RuntimeError('Invalid message type %d' % msg_type)

    def _writer(self):
        env = self.env
        while True:
            if not self._out_queue:
                self._send_ev = Event(self.env)
                yield self._send_ev

            # TODO Is it possible that the connection gets closed while the
            # following write request is pending? If so, the _writer process
            # will not exit.
            yield self.socket.write(self._out_queue.pop(0))

    def _handle_error(self, process):
        if process._ok:
            return

        # TODO What about half-closes? The connection needs to be closed
        # completely in that case, because it is broken.

        err = process._value
        # FIXME Should I really ignore errors?
        if isinstance(err, socket.error) and err.errno in UNCRITICAL_ERRORS:
            uncritical = True
        else:
            uncritical = False

        process.defused = uncritical

        events = [self._send_ev, self._recv_ev]
        if self._out_queue is not None:
            # FIXME This may introduce non-deterministic behaviour.
            events.extend(self._out_messages.values())

        for event in events:
            if event is None:
                continue

            event.defused = uncritical
            event.fail(err)

        self._in_messages = None
        self._out_messages = None
        self._in_queue = None
        self._out_queue = None
        self._recv_ev = None
        self._send_ev = None

    def _reply(self, event):
        try:
            message_id = self._in_messages.pop(event)
        except AttributeError:
            if self._in_messages is not None:
                raise

            # Channel has been closed. Ignore the event.
            event.defused = True
            return

        if event._ok:
            failure = None
            try:
                self._out_queue.append(self.codec.encode(
                        (SUCCESS, message_id, event._value)))
            except BaseException as e:
                failure = e
        else:
            failure = event._value

        if failure is not None:
            # Failure is handled on the remote side.
            event.defused = True

            # FIXME Ugly hack for python < 3.3
            if hasattr(failure, '__traceback__'):
                stacktrace = traceback.format_exception(failure.__class__,
                        failure, failure.__traceback__)
            else:
                stacktrace = traceback.format_exception_only(failure.__class__,
                        failure)

            self._out_queue.append(self.codec.encode(
                    (FAILURE, message_id, ''.join(stacktrace))))

        if self._send_ev is not None:
            self._send_ev.succeed()
            self._send_ev = None

    def send(self, content):
        if self._out_queue is None:
            raise self.writer.value

        if len(self._out_messages) >= self.message_limit:
            raise MessageOverflowError('Outgoing message limit of %d has been '
                    'exceeded' % self.message_limit)

        message_id = next(self._message_id)
        data = self.codec.encode((REQUEST, message_id, content))
        message = OutMessage(self, message_id, content)

        self._out_queue.append(data)
        self._out_messages[message_id] = message

        # Wake the writer process.
        if self._send_ev is not None:
            self._send_ev.succeed()
            self._send_ev = None

        return message

    def recv(self):
        if self._in_queue is None:
            raise self.reader.value

        # Enqueue reads if there are no pending incoming messages.
        if not self._in_queue:
            if self._recv_ev is not None:
                raise RuntimeError('Concurrent receive attempt')

            self._recv_ev = Event(self.env)
            return self._recv_ev

        return Event(self.env).succeed(self._in_queue.pop(0))

    def close(self):
        self.socket.close()
