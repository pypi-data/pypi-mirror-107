#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2021 Kazuhiro KOBAYASHI <root.4mac@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import joblib
import torch
import torch.nn as nn

from .layer import Conv1d, ConvLTVFilterGenerator, SinusoidsGenerator
from .preprocess_layer import (LogMelSpectrogram2LogMagnitude,
                               LogMelSpectrogramScaler)


class NeuralHomomorphicVocoder(nn.Module):
    def __init__(
        self,
        fs=24000,
        fft_size=1024,
        hop_size=256,
        in_channels=80,
        conv_channels=256,
        ltv_out_channels=222,
        out_channels=1,
        kernel_size=3,
        group_size=8,
        dilation_size=1,
        fmin=80,
        fmax=7600,
        roll_size=24,
        use_causal=False,
        use_conv_postfilter=False,
        use_ltv_conv_postfilter=False,
        use_reference_mag=False,
        use_quefrency_norm=True,
        scaler_file=None,
    ):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.use_conv_postfilter = use_conv_postfilter

        if scaler_file is not None:
            self.melspc_scaler_fn = LogMelSpectrogramScaler(
                joblib.load(scaler_file)["mlfb"]
            )
        else:
            self.melspc_scaler_fn = None

        if use_reference_mag:
            mel2linear_fn = LogMelSpectrogram2LogMagnitude(
                fs=fs,
                fft_size=fft_size,
                n_mels=in_channels,
                fmin=fmin,
                fmax=fmax,
                roll_size=roll_size,
                melspc_scaler_fn=self.melspc_scaler_fn,
            )
        else:
            mel2linear_fn = None

        ltv_params = {
            "in_channels": in_channels,
            "conv_channels": conv_channels,
            "ltv_out_channels": ltv_out_channels,
            "kernel_size": kernel_size,
            "dilation_size": dilation_size,
            "group_size": group_size,
            "fft_size": fft_size,
            "hop_size": hop_size,
            "use_causal": use_causal,
            "use_ltv_conv_postfilter": use_ltv_conv_postfilter,
            "use_quefrency_norm": use_quefrency_norm,
        }
        self.impuluse_generator = SinusoidsGenerator(hop_size=hop_size, fs=fs)
        self.ltv_harmonic = ConvLTVFilterGenerator(
            **ltv_params, mel2spc_fn=mel2linear_fn
        )
        self.ltv_noise = ConvLTVFilterGenerator(**ltv_params)

        if self.use_conv_postfilter:
            self.conv_pf = Conv1d(
                in_channels=1, out_channels=1, kernel_size=fft_size, use_causal=True
            )

    def _forward(self, x, cf0, uv):
        """
        x: (B, T, D)
        cf0: (B, T, 1)
        uv: (B, T, 1)
        """
        if self.melspc_scaler_fn is not None:
            x = self.melspc_scaler_fn(x)

        harmonic, noise = self.impuluse_generator(cf0, uv)
        sig_harm = self.ltv_harmonic(x, harmonic)
        sig_noise = self.ltv_noise(x, noise)
        y = sig_harm + sig_noise

        if self.use_conv_postfilter:
            y = self.conv_pf(y.transpose(1, 2)).transpose(1, 2)

        return y.reshape(x.size(0), self.out_channels, -1)

    def forward(self, z, c):
        """Interface for PWG trainer
        z: (B, T, D)
        c: (B, T, n_mels + 2)
        """
        c = c.transpose(1, 2)
        x, cf0, uv = torch.split(c, [self.in_channels, 1, 1], dim=-1)
        y = self._forward(x, cf0, uv)
        return y

    def inference(self, c):
        """Interface for PWG decoder
        c: (T, D)
        """
        c = c.unsqueeze(0)
        x, cf0, uv = torch.split(c, [self.in_channels, 1, 1], dim=-1)
        y = self._forward(x, cf0, uv)
        return y.squeeze(0)

    def remove_weight_norm(self):
        """Interface for PWG"""
        pass
