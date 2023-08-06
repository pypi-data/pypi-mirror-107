#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from audioop import rms
from logging import getLogger
from time import time


class Listener:
    chunk_size = 4000
    # Максимальный размер потокового файла для Яндекса - 10 мегабайт.
    max_size = 10485760
    amplitude_size = 2
    sample_width = 2
    total_size = 0
    _continue = True
    logger = getLogger('astersay.backends.Listener')

    def __init__(self, stream, amplitude=None):
        """
        :param stream: файлоподобный обЪект потока голоса.
        :param amplitude: список (пустой) для записи результатов посекундного
                          анализа потока.
        :type amplitude: list
        """
        self._stream = stream
        if amplitude is None:
            amplitude = []
        self.amplitude = amplitude

    def has_continue(self):
        return self._continue and (
            self.total_size + self.chunk_size < self.max_size)

    def listen(self):
        chunk_size = self.chunk_size
        stream_read = self._stream.read
        logger_debug = self.logger.debug

        amplitude = self.amplitude
        amplitude_size = self.amplitude_size
        sample_width = self.sample_width
        chunk_number = 0
        sample = b''
        sample_second = int(time())
        while self.has_continue():
            chunk_number += 1
            chunk_second = int(time())
            chunk = stream_read(chunk_size)
            length = len(chunk)
            if sample_second < chunk_second:
                rms_value = rms(sample, sample_width)
                # logger_debug('rms=%d', rms_value)
                amplitude.append((sample_second, rms_value))
                if len(amplitude) > amplitude_size:
                    amplitude.pop(0)
                sample = b''
                sample_second = chunk_second
            sample += chunk
            # logger_debug('chunck %d length is %d', chunk_number, length)
            if length == 0:
                self.stop()
            self.total_size += length
            yield chunk
        logger_debug('listener ended, total size %d', self.total_size)

    def stop(self):
        self._continue = False
        self.logger.debug('listener stopped')


class BaseBackend:

    def __init__(self):
        cls = self.__class__
        name = '%s.%s' % (cls.__module__, cls.__name__)
        self.logger = getLogger(name)

    def __str__(self):
        return str(self.__class__)[8:-2]
