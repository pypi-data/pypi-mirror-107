# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Copyright (c) 2021 scart97

import json
from pathlib import Path
from typing import Any, Iterable, Tuple, Union

import torchaudio
from torch import Tensor
from torch.utils.data import Dataset

from thunder.text_processing.preprocess import lower_text, normalize_text


class BaseSpeechDataset(Dataset):
    def __init__(
        self, items: Iterable, force_mono: bool = True, sample_rate: int = 16000
    ):
        """This is the base class that implements the minimal functionality to have a compatible
        speech dataset, in a way that can be easily customized by subclassing.

        Args:
            items : Source of items in the dataset, sorted by audio duration. This can be a list of files, a pandas dataframe or any other iterable structure where you record your data.
            force_mono : If true, convert all the loaded samples to mono.
            sample_rate : Sample rate used by the dataset. All of the samples that have different rate will be resampled.
        """
        super().__init__()
        self.items = items
        self.sample_rate = sample_rate
        self.force_mono = force_mono

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index: int) -> Tuple[Tensor, str]:
        item = self.get_item(index)
        # Dealing with input
        audio, sr = self.open_audio(item)
        audio = self.preprocess_audio(audio, sr)
        # Dealing with output
        text = self.open_text(item)
        text = self.preprocess_text(text)

        return audio, text

    def get_item(self, index: int) -> Any:
        """Get the item source specified by the index.

        Args:
            index : Indicates what item it needs to return information about.

        Returns:
            Whatever data necessary to open the audio and text corresponding to this index.
        """
        return self.items[index]

    def open_audio(self, item: Any) -> Tuple[Tensor, int]:
        """Uses the data returned by get_item to open the audio

        Args:
            item : Data returned by get_item(index)

        Returns:
            Tuple containing the audio tensor with shape (channels, time), and the corresponding sample rate.
        """
        return torchaudio.load(item)

    def preprocess_audio(self, audio: Tensor, sample_rate: int) -> Tensor:
        """Apply some base transforms to the audio, that fix silent problems.
        It transforms all the audios to mono (depending on class creation parameter),
        remove the possible DC bias present and then resamples the audios to a common
        sample rate.

        Args:
            audio : Audio tensor
            sample_rate : Sample rate

        Returns:
            Audio tensor after the transforms.
        """
        if self.force_mono and (audio.shape[0] > 1):
            audio = audio.mean(0, keepdim=True)

        # Removing the dc component from the audio
        # It happens when a faulty capture device introduce
        # an offset into the recorded waveform, and this can
        # cause problems with later transforms.
        # https://en.wikipedia.org/wiki/DC_bias
        audio = audio - audio.mean(1)

        if self.sample_rate != sample_rate:
            tfm = torchaudio.transforms.Resample(
                orig_freq=sample_rate, new_freq=self.sample_rate
            )
            audio = tfm(audio)
        return audio

    def open_text(self, item: Any) -> str:
        """Opens the transcription based on the data returned by get_item(index)

        Args:
            item : The data returned by get_item.

        Returns:
            The transcription corresponding to the item.
        """
        raise NotImplementedError()

    def preprocess_text(self, text: str) -> str:
        normalized = normalize_text(text)
        lower = lower_text(normalized)
        return lower


class ManifestSpeechDataset(BaseSpeechDataset):
    def __init__(self, file: Union[str, Path], force_mono: bool, sample_rate: int):
        """Dataset that loads from nemo manifest files.

        Args:
            file : Nemo manifest file.
            force_mono : If true, convert all the loaded samples to mono.
            sample_rate : Sample rate used by the dataset. All of the samples that have different rate will be resampled.
        """
        file = Path(file)
        # Reading from the manifest file
        items = [json.loads(line) for line in file.read_text().strip().splitlines()]
        super().__init__(items, force_mono=force_mono, sample_rate=sample_rate)

    def open_audio(self, item: dict) -> Tuple[Tensor, int]:
        return torchaudio.load(item["audio_filepath"])

    def open_text(self, item: dict) -> str:
        return item["text"]
