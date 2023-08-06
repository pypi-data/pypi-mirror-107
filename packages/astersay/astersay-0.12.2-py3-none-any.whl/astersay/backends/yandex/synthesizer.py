#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
import json
import re
import requests
from gettext import gettext as _
from os import system as os_system, remove as os_remove
from os.path import join as path_join, exists, basename
from wave import open as wave_open

from astersay.utils import make_checksum
from astersay.backends.yandex.base import YandexBaseBackend


class YandexSynthesizer(YandexBaseBackend):
    URL = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    LANGS = ('ru-RU', 'en-US', 'tr-TR')
    VOICES = {
        'ru-RU': ('oksana', 'jane', 'omazh', 'zahar', 'ermil',
                  'alena', 'filipp'),
        'tr-TR': ('silaerkan', 'erkanyavas'),
        'en-US': ('alyss', 'nick'),
    }
    EMOTIONS = ('good', 'evil', 'neutral')
    AUDIO_FORMATS = ('lpcm', 'oggopus')
    HERTZ_LIST = (48000, 16000, 8000)

    def __init__(self, settings):
        YandexBaseBackend.__init__(self)
        self.set_token_manager(settings)

        conf = settings.yandex
        self.folder_id = conf['auth']['folder_id']

        synthesizer = conf['synthesizer']
        self.storage_path = synthesizer['storage']
        self.convertor = synthesizer['convertor']

        lang = synthesizer['lang']
        assert lang in self.LANGS
        self.lang = lang

        voice = synthesizer['voice']
        assert voice in self.VOICES[lang]
        self.voice = voice

        emotion = synthesizer['emotion']
        assert emotion in self.EMOTIONS
        self.emotion = emotion

        speed = synthesizer['speed']
        assert 0.1 <= speed <= 3.0
        self.speed = speed

        audio_format = synthesizer['format']
        assert audio_format in self.AUDIO_FORMATS
        self.audio_format = audio_format

        sample_rate_hertz = synthesizer['sample_rate_hertz']
        assert sample_rate_hertz in self.HERTZ_LIST
        self.sample_rate_hertz = sample_rate_hertz

    @property
    def message_params(self):
        return {
            'lang': self.lang,
            'voice': self.voice,
            'emotion': self.emotion,
            'speed': self.speed,
            'folderId': self.folder_id,
            'format': self.audio_format,
            'sampleRateHertz': self.sample_rate_hertz,
        }

    def make_message(self, text):
        assert len(text) <= 5000
        message = self.message_params
        message['text'] = text
        return message

    def _synthesize(self, message: dict):
        self.token_manager.update_token()
        logger_debug = self.logger.debug

        headers = {
            'Authorization': 'Bearer %s' % self.token_manager.token,
        }
        logger_debug(_('Заголовки синтеза речи: %s'), headers)
        logger_debug(_('Параметры синтеза речи: %s'), message)
        response = requests.post(self.URL, data=message, headers=headers)
        if response.ok:
            logger_debug(_('Синтез речи выполнен.'))
            return response.content
        self.logger.warning(
            _('Ошибка синтеза речи. Яндекс вернул код, отличный от 200. %s'),
            response.text,
        )

    def make_voice(self, text):
        logger_debug = self.logger.debug
        logger_info = self.logger.info
        logger_info(_('Начинается синтез речи.'))

        # Убираем лишние пробелы.
        text = re.sub(r'\s+', ' ', text)

        convertor = self.convertor

        def find_voice(checksum):
            voice = path_join(self.storage_path, checksum)
            filename = '%s.wav' % voice
            # Именно такой файл уже есть, не нужно синтезировать.
            if exists(filename):
                logger_info(
                    _('Речь %r существует и будет взята из хранилища.'), voice)
                found = True
            else:
                found = False
            return voice, filename, found

        def save_info(voice, spec):
            spec_filename = '%s.json' % voice
            json.dump(spec, open(spec_filename, 'w'), indent=4, ensure_ascii=False)
            logger_debug(_('Сохранён файл спецификации: %s'), spec_filename)

        def synthesize(voice, filename, message, spec):
            save_info(voice, spec)

            audio_data = self._synthesize(message)

            src_filename = '%s.%s' % (voice, convertor['src_format'])
            with open(src_filename, 'wb') as f:
                f.write(audio_data)
            logger_info(_('Записан исходный файл речи: %s'), src_filename)
            command = convertor['command'] % (src_filename, filename)
            os_system(command)
            logger_info(_('Записан конечный файл речи: %s'), filename)

            if convertor.get('src_delete'):
                os_remove(src_filename)
            return True

        # Символ | является разделителем на несколько составных файлов, но
        # он может быть и цельным.
        message = self.make_message(text.replace('|', ''))
        spec = message.copy()
        spec['convertor'] = convertor
        checksum = make_checksum(spec)
        voice, filename, found = find_voice(checksum)

        texts = text.split('|')
        if len(texts) == 1:
            if not found:
                logger_info(_('Синтезирую в речь текст: %r'), text)
                synthesize(voice, filename, message, spec)
        elif not found:
            chunks = []
            for chunk_text in texts:
                chunk_message = self.make_message(chunk_text)
                chunk_spec = chunk_message.copy()
                chunk_spec['convertor'] = convertor
                chunk_checksum = make_checksum(chunk_spec)
                chunk_voice, chunk_filename, found = find_voice(chunk_checksum)
                if not found:
                    logger_info(_('Синтезирую в речь текст: %r'), chunk_text)
                    synthesize(chunk_voice, chunk_filename, chunk_message,
                               chunk_spec)
                chunks.append((chunk_voice, chunk_filename))

            frames = []
            params = None
            last_voice = chunks[-1][0]
            for chunk_voice, chunk_filename in chunks:
                with wave_open(chunk_filename) as f:
                    if chunk_voice == last_voice:
                        params = f.getparams()
                    frames.append(f.readframes(f.getnframes()))
            # Записываем информацию по слитому файлу.
            spec['chunks'] = [basename(v) for v, f in chunks]
            save_info(voice, spec)
            # Записываем конечный, слитый файл.
            with wave_open(filename, 'wb') as f:
                f.setparams(params)
                for frame in frames:
                    f.writeframes(frame)

        return voice
