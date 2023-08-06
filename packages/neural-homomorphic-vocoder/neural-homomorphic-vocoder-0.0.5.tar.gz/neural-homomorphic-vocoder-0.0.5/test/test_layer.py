#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2021 Kazuhiro KOBAYASHI <root.4mac@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

from pathlib import Path

import pytest
import soundfile as sf
import torch
import torch.nn.functional as F

B, T, D = 3, 100, 80
hop_size, fft_size, window_size = 128, 1024, 1024
fs = 24000

dirname = Path(__file__).parent
scalerf = dirname / "data" / "test_scaler.pkl"


@pytest.mark.parametrize(
    [
        "use_causal",
        "use_conv_postfilter",
        "use_ltv_conv_postfilter",
        "use_reference_mag",
        "scaler_file",
    ],
    [
        (True, False, False, False, None),
        (False, False, False, False, None),
        (False, True, False, False, None),
        (False, False, True, False, None),
        (False, False, False, True, None),
        (False, False, False, False, scalerf),
    ],
    ids=[
        "use_causal",
        "not_use_causal",
        "use_conv_postfilter",
        "use_ltv_conv_postfilter",
        "use_reference_mag",
        "use_scaler",
    ],
)
def test_nhv(
    use_causal,
    use_conv_postfilter,
    use_ltv_conv_postfilter,
    use_reference_mag,
    scaler_file,
):
    from nhv.layer import NeuralHomomorphicVocoder

    net = NeuralHomomorphicVocoder(
        fs=fs,
        fft_size=fft_size,
        hop_size=hop_size,
        in_channels=D,
        use_causal=use_causal,
        use_conv_postfilter=use_conv_postfilter,
        use_ltv_conv_postfilter=use_ltv_conv_postfilter,
        use_reference_mag=use_reference_mag,
        scaler_file=scaler_file,
    )
    z = torch.randn((B, 1, T * D))
    x = torch.randn((B, T, D))
    f0 = torch.randn(B, T, 1)
    uv = torch.randn(B, T, 1)
    y = net._forward(x, f0, uv)  # noqa
    y = net.forward(z, torch.cat([x, f0, uv], dim=-1).transpose(1, 2))
    assert y.size(2) == T * hop_size


def test_layer():
    from nhv.layer import ConvLTVFilterGenerator

    x = torch.randn((B, T, D))
    z = torch.randn((B, 1, T * hop_size))
    conv = ConvLTVFilterGenerator(
        in_channels=80, ltv_out_channels=256, fft_size=fft_size, hop_size=hop_size
    )
    y = conv(x, z)  # noqa


def test_sinusoids_generator():
    from nhv.layer import SinusoidsGenerator

    net = SinusoidsGenerator(hop_size=hop_size, fs=fs)
    cf0 = torch.arange(100, 100 + T).reshape(1, -1, 1)
    cf0 = torch.cat([cf0, cf0, cf0], axis=0).float()
    uv = torch.ones_like(cf0).float()
    excit, noise = net(cf0, uv)
    outf = dirname / "test_sinusoids_generator_output.wav"
    sf.write(outf, excit[0].squeeze().numpy(), fs)
    outf.unlink()


def test_sinusoids_generator_fromf0():
    import numpy as np
    from nhv.layer import SinusoidsGenerator

    net = SinusoidsGenerator(hop_size=hop_size, fs=fs)
    f0 = np.loadtxt(dirname / "data" / "test.f0")
    cf0 = torch.from_numpy(f0).reshape(1, -1, 1)
    cf0 = torch.cat([cf0, cf0], axis=0)
    uv = torch.ones_like(cf0).float()
    excit, noise = net(cf0, uv)
    outf = dirname / "test_sinusoids_generator_from_f0_output.wav"
    sf.write(outf, excit[0].squeeze().numpy(), fs)
    outf.unlink()


def test_unfold():
    x = torch.randn(B, T, hop_size)
    _ = torch.randn(B, T, fft_size)

    z = torch.randn(B, 1, T * hop_size)
    z = z.squeeze()  # B, T x hop_size
    z = F.pad(z, (fft_size, fft_size - 1))
    z = z.unfold(-1, fft_size * 2, step=hop_size)  # B x T x window_size
    z = F.pad(z, (hop_size // 2, hop_size // 2 - 1))
    z = z.unfold(-1, hop_size, step=1)  # B x T x window_size x hop_size
    z = torch.matmul(z.squeeze(), x.unsqueeze(-1)).squeeze()  # B x T x window_size


def test_ola():
    win = torch.bartlett_window(window_size, periodic=False)
    z = torch.randn(3, 100, window_size)
    z = z * win
    l, r = torch.chunk(z, 2, dim=-1)
    z = l + r.roll(1, dims=-1)
    z = z.reshape(z.size(0), -1).unsqueeze(1)
