'''wavfile.py'''
# View the original code here:
#   https://github.com/scipy/scipy/blob/master/scipy/io/wavfile.py

"""
Copyright Notice
-----------------

Copyright (c) 2001-2002 Enthought, Inc.  2003-2019, SciPy Developers.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of
   conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list
   of conditions and the following disclaimer in the documentation and/or other
   materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be
   used to endorse or promote products derived from this software without specific
   prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import io
import sys
import numpy
import struct
import warnings
from enum import IntEnum


__all__ = [
    'WavFileWarning',
    'read',
    'write'
]


class WavFileWarning(UserWarning):
    pass


class WAVE_FORMAT(IntEnum):
    UNKNOWN = 0x0000
    PCM = 0x0001
    ADPCM = 0x0002
    IEEE_FLOAT = 0x0003
    VSELP = 0x0004
    IBM_CVSD = 0x0005
    ALAW = 0x0006
    MULAW = 0x0007
    DTS = 0x0008
    DRM = 0x0009
    WMAVOICE9 = 0x000A
    WMAVOICE10 = 0x000B
    OKI_ADPCM = 0x0010
    DVI_ADPCM = 0x0011
    IMA_ADPCM = 0x0011  # Duplicate
    MEDIASPACE_ADPCM = 0x0012
    SIERRA_ADPCM = 0x0013
    G723_ADPCM = 0x0014
    DIGISTD = 0x0015
    DIGIFIX = 0x0016
    DIALOGIC_OKI_ADPCM = 0x0017
    MEDIAVISION_ADPCM = 0x0018
    CU_CODEC = 0x0019
    HP_DYN_VOICE = 0x001A
    YAMAHA_ADPCM = 0x0020
    SONARC = 0x0021
    DSPGROUP_TRUESPEECH = 0x0022
    ECHOSC1 = 0x0023
    AUDIOFILE_AF36 = 0x0024
    APTX = 0x0025
    AUDIOFILE_AF10 = 0x0026
    PROSODY_1612 = 0x0027
    LRC = 0x0028
    DOLBY_AC2 = 0x0030
    GSM610 = 0x0031
    MSNAUDIO = 0x0032
    ANTEX_ADPCME = 0x0033
    CONTROL_RES_VQLPC = 0x0034
    DIGIREAL = 0x0035
    DIGIADPCM = 0x0036
    CONTROL_RES_CR10 = 0x0037
    NMS_VBXADPCM = 0x0038
    CS_IMAADPCM = 0x0039
    ECHOSC3 = 0x003A
    ROCKWELL_ADPCM = 0x003B
    ROCKWELL_DIGITALK = 0x003C
    XEBEC = 0x003D
    G721_ADPCM = 0x0040
    G728_CELP = 0x0041
    MSG723 = 0x0042
    INTEL_G723_1 = 0x0043
    INTEL_G729 = 0x0044
    SHARP_G726 = 0x0045
    MPEG = 0x0050
    RT24 = 0x0052
    PAC = 0x0053
    MPEGLAYER3 = 0x0055
    LUCENT_G723 = 0x0059
    CIRRUS = 0x0060
    ESPCM = 0x0061
    VOXWARE = 0x0062
    CANOPUS_ATRAC = 0x0063
    G726_ADPCM = 0x0064
    G722_ADPCM = 0x0065
    DSAT = 0x0066
    DSAT_DISPLAY = 0x0067
    VOXWARE_BYTE_ALIGNED = 0x0069
    VOXWARE_AC8 = 0x0070
    VOXWARE_AC10 = 0x0071
    VOXWARE_AC16 = 0x0072
    VOXWARE_AC20 = 0x0073
    VOXWARE_RT24 = 0x0074
    VOXWARE_RT29 = 0x0075
    VOXWARE_RT29HW = 0x0076
    VOXWARE_VR12 = 0x0077
    VOXWARE_VR18 = 0x0078
    VOXWARE_TQ40 = 0x0079
    VOXWARE_SC3 = 0x007A
    VOXWARE_SC3_1 = 0x007B
    SOFTSOUND = 0x0080
    VOXWARE_TQ60 = 0x0081
    MSRT24 = 0x0082
    G729A = 0x0083
    MVI_MVI2 = 0x0084
    DF_G726 = 0x0085
    DF_GSM610 = 0x0086
    ISIAUDIO = 0x0088
    ONLIVE = 0x0089
    MULTITUDE_FT_SX20 = 0x008A
    INFOCOM_ITS_G721_ADPCM = 0x008B
    CONVEDIA_G729 = 0x008C
    CONGRUENCY = 0x008D
    SBC24 = 0x0091
    DOLBY_AC3_SPDIF = 0x0092
    MEDIASONIC_G723 = 0x0093
    PROSODY_8KBPS = 0x0094
    ZYXEL_ADPCM = 0x0097
    PHILIPS_LPCBB = 0x0098
    PACKED = 0x0099
    MALDEN_PHONYTALK = 0x00A0
    RACAL_RECORDER_GSM = 0x00A1
    RACAL_RECORDER_G720_A = 0x00A2
    RACAL_RECORDER_G723_1 = 0x00A3
    RACAL_RECORDER_TETRA_ACELP = 0x00A4
    NEC_AAC = 0x00B0
    RAW_AAC1 = 0x00FF
    RHETOREX_ADPCM = 0x0100
    IRAT = 0x0101
    VIVO_G723 = 0x0111
    VIVO_SIREN = 0x0112
    PHILIPS_CELP = 0x0120
    PHILIPS_GRUNDIG = 0x0121
    DIGITAL_G723 = 0x0123
    SANYO_LD_ADPCM = 0x0125
    SIPROLAB_ACEPLNET = 0x0130
    SIPROLAB_ACELP4800 = 0x0131
    SIPROLAB_ACELP8V3 = 0x0132
    SIPROLAB_G729 = 0x0133
    SIPROLAB_G729A = 0x0134
    SIPROLAB_KELVIN = 0x0135
    VOICEAGE_AMR = 0x0136
    G726ADPCM = 0x0140
    DICTAPHONE_CELP68 = 0x0141
    DICTAPHONE_CELP54 = 0x0142
    QUALCOMM_PUREVOICE = 0x0150
    QUALCOMM_HALFRATE = 0x0151
    TUBGSM = 0x0155
    MSAUDIO1 = 0x0160
    WMAUDIO2 = 0x0161
    WMAUDIO3 = 0x0162
    WMAUDIO_LOSSLESS = 0x0163
    WMASPDIF = 0x0164
    UNISYS_NAP_ADPCM = 0x0170
    UNISYS_NAP_ULAW = 0x0171
    UNISYS_NAP_ALAW = 0x0172
    UNISYS_NAP_16K = 0x0173
    SYCOM_ACM_SYC008 = 0x0174
    SYCOM_ACM_SYC701_G726L = 0x0175
    SYCOM_ACM_SYC701_CELP54 = 0x0176
    SYCOM_ACM_SYC701_CELP68 = 0x0177
    KNOWLEDGE_ADVENTURE_ADPCM = 0x0178
    FRAUNHOFER_IIS_MPEG2_AAC = 0x0180
    DTS_DS = 0x0190
    CREATIVE_ADPCM = 0x0200
    CREATIVE_FASTSPEECH8 = 0x0202
    CREATIVE_FASTSPEECH10 = 0x0203
    UHER_ADPCM = 0x0210
    ULEAD_DV_AUDIO = 0x0215
    ULEAD_DV_AUDIO_1 = 0x0216
    QUARTERDECK = 0x0220
    ILINK_VC = 0x0230
    RAW_SPORT = 0x0240
    ESST_AC3 = 0x0241
    GENERIC_PASSTHRU = 0x0249
    IPI_HSX = 0x0250
    IPI_RPELP = 0x0251
    CS2 = 0x0260
    SONY_SCX = 0x0270
    SONY_SCY = 0x0271
    SONY_ATRAC3 = 0x0272
    SONY_SPC = 0x0273
    TELUM_AUDIO = 0x0280
    TELUM_IA_AUDIO = 0x0281
    NORCOM_VOICE_SYSTEMS_ADPCM = 0x0285
    FM_TOWNS_SND = 0x0300
    MICRONAS = 0x0350
    MICRONAS_CELP833 = 0x0351
    BTV_DIGITAL = 0x0400
    INTEL_MUSIC_CODER = 0x0401
    INDEO_AUDIO = 0x0402
    QDESIGN_MUSIC = 0x0450
    ON2_VP7_AUDIO = 0x0500
    ON2_VP6_AUDIO = 0x0501
    VME_VMPCM = 0x0680
    TPC = 0x0681
    LIGHTWAVE_LOSSLESS = 0x08AE
    OLIGSM = 0x1000
    OLIADPCM = 0x1001
    OLICELP = 0x1002
    OLISBC = 0x1003
    OLIOPR = 0x1004
    LH_CODEC = 0x1100
    LH_CODEC_CELP = 0x1101
    LH_CODEC_SBC8 = 0x1102
    LH_CODEC_SBC12 = 0x1103
    LH_CODEC_SBC16 = 0x1104
    NORRIS = 0x1400
    ISIAUDIO_2 = 0x1401
    SOUNDSPACE_MUSICOMPRESS = 0x1500
    MPEG_ADTS_AAC = 0x1600
    MPEG_RAW_AAC = 0x1601
    MPEG_LOAS = 0x1602
    NOKIA_MPEG_ADTS_AAC = 0x1608
    NOKIA_MPEG_RAW_AAC = 0x1609
    VODAFONE_MPEG_ADTS_AAC = 0x160A
    VODAFONE_MPEG_RAW_AAC = 0x160B
    MPEG_HEAAC = 0x1610
    VOXWARE_RT24_SPEECH = 0x181C
    SONICFOUNDRY_LOSSLESS = 0x1971
    INNINGS_TELECOM_ADPCM = 0x1979
    LUCENT_SX8300P = 0x1C07
    LUCENT_SX5363S = 0x1C0C
    CUSEEME = 0x1F03
    NTCSOFT_ALF2CM_ACM = 0x1FC4
    DVM = 0x2000
    DTS2 = 0x2001
    MAKEAVIS = 0x3313
    DIVIO_MPEG4_AAC = 0x4143
    NOKIA_ADAPTIVE_MULTIRATE = 0x4201
    DIVIO_G726 = 0x4243
    LEAD_SPEECH = 0x434C
    LEAD_VORBIS = 0x564C
    WAVPACK_AUDIO = 0x5756
    OGG_VORBIS_MODE_1 = 0x674F
    OGG_VORBIS_MODE_2 = 0x6750
    OGG_VORBIS_MODE_3 = 0x6751
    OGG_VORBIS_MODE_1_PLUS = 0x676F
    OGG_VORBIS_MODE_2_PLUS = 0x6770
    OGG_VORBIS_MODE_3_PLUS = 0x6771
    ALAC = 0x6C61
    _3COM_NBX = 0x7000  # Can't have leading digit
    OPUS = 0x704F
    FAAD_AAC = 0x706D
    AMR_NB = 0x7361
    AMR_WB = 0x7362
    AMR_WP = 0x7363
    GSM_AMR_CBR = 0x7A21
    GSM_AMR_VBR_SID = 0x7A22
    COMVERSE_INFOSYS_G723_1 = 0xA100
    COMVERSE_INFOSYS_AVQSBC = 0xA101
    COMVERSE_INFOSYS_SBC = 0xA102
    SYMBOL_G729_A = 0xA103
    VOICEAGE_AMR_WB = 0xA104
    INGENIENT_G726 = 0xA105
    MPEG4_AAC = 0xA106
    ENCORE_G726 = 0xA107
    ZOLL_ASAO = 0xA108
    SPEEX_VOICE = 0xA109
    VIANIX_MASC = 0xA10A
    WM9_SPECTRUM_ANALYZER = 0xA10B
    WMF_SPECTRUM_ANAYZER = 0xA10C
    GSM_610 = 0xA10D
    GSM_620 = 0xA10E
    GSM_660 = 0xA10F
    GSM_690 = 0xA110
    GSM_ADAPTIVE_MULTIRATE_WB = 0xA111
    POLYCOM_G722 = 0xA112
    POLYCOM_G728 = 0xA113
    POLYCOM_G729_A = 0xA114
    POLYCOM_SIREN = 0xA115
    GLOBAL_IP_ILBC = 0xA116
    RADIOTIME_TIME_SHIFT_RADIO = 0xA117
    NICE_ACA = 0xA118
    NICE_ADPCM = 0xA119
    VOCORD_G721 = 0xA11A
    VOCORD_G726 = 0xA11B
    VOCORD_G722_1 = 0xA11C
    VOCORD_G728 = 0xA11D
    VOCORD_G729 = 0xA11E
    VOCORD_G729_A = 0xA11F
    VOCORD_G723_1 = 0xA120
    VOCORD_LBC = 0xA121
    NICE_G728 = 0xA122
    FRACE_TELECOM_G729 = 0xA123
    CODIAN = 0xA124
    FLAC = 0xF1AC
    EXTENSIBLE = 0xFFFE
    DEVELOPMENT = 0xFFFF


KNOWN_WAVE_FORMATS = {WAVE_FORMAT.PCM, WAVE_FORMAT.IEEE_FLOAT}


def _raise_bad_format(format_tag):
    try:
        format_name = WAVE_FORMAT(format_tag).name
    except ValueError:
        format_name = f'{format_tag:#06x}'
    raise ValueError(f"Unknown wave file format: {format_name}. Supported "
                     "formats: " +
                     ', '.join(x.name for x in KNOWN_WAVE_FORMATS))


def _read_fmt_chunk(fid, is_big_endian):
    if is_big_endian:
        fmt = '>'
    else:
        fmt = '<'

    size = struct.unpack(fmt+'I', fid.read(4))[0]

    if size < 16:
        raise ValueError("Binary structure of wave file is not compliant")

    res = struct.unpack(fmt+'HHIIHH', fid.read(16))
    bytes_read = 16

    format_tag, channels, fs, bytes_per_second, block_align, bit_depth = res

    if format_tag == WAVE_FORMAT.EXTENSIBLE and size >= (16+2):
        ext_chunk_size = struct.unpack(fmt+'H', fid.read(2))[0]
        bytes_read += 2
        if ext_chunk_size >= 22:
            extensible_chunk_data = fid.read(22)
            bytes_read += 22
            raw_guid = extensible_chunk_data[2+4:2+4+16]
            # GUID template {XXXXXXXX-0000-0010-8000-00AA00389B71} (RFC-2361)
            # MS GUID byte order: first three groups are native byte order,
            # rest is Big Endian
            if is_big_endian:
                tail = b'\x00\x00\x00\x10\x80\x00\x00\xAA\x00\x38\x9B\x71'
            else:
                tail = b'\x00\x00\x10\x00\x80\x00\x00\xAA\x00\x38\x9B\x71'
            if raw_guid.endswith(tail):
                format_tag = struct.unpack(fmt+'I', raw_guid[:4])[0]
        else:
            raise ValueError("Binary structure of wave file is not compliant")

    if format_tag not in KNOWN_WAVE_FORMATS:
        _raise_bad_format(format_tag)

    # move file pointer to next chunk
    if size > bytes_read:
        fid.read(size - bytes_read)

    # fmt should always be 16, 18 or 40, but handle it just in case
    _handle_pad_byte(fid, size)

    return (size, format_tag, channels, fs, bytes_per_second, block_align,
            bit_depth)


def _read_data_chunk(fid, format_tag, channels, bit_depth, is_big_endian,
                     block_align, mmap=False):
    if is_big_endian:
        fmt = '>'
    else:
        fmt = '<'

    # Size of the data subchunk in bytes
    size = struct.unpack(fmt+'I', fid.read(4))[0]

    # Number of bytes per sample (sample container size)
    bytes_per_sample = block_align // channels
    n_samples = size // bytes_per_sample

    if format_tag == WAVE_FORMAT.PCM:
        if 1 <= bit_depth <= 8:
            dtype = 'u1'  # WAV of 8-bit integer or less are unsigned
        elif bytes_per_sample in {3, 5, 6, 7}:
            # No compatible dtype.  Load as raw bytes for reshaping later.
            dtype = 'V1'
        elif bit_depth <= 64:
            # Remaining bit depths can map directly to signed numpy dtypes
            dtype = f'{fmt}i{bytes_per_sample}'
        else:
            raise ValueError("Unsupported bit depth: the WAV file "
                             f"has {bit_depth}-bit integer data.")
    elif format_tag == WAVE_FORMAT.IEEE_FLOAT:
        if bit_depth in {32, 64}:
            dtype = f'{fmt}f{bytes_per_sample}'
        else:
            raise ValueError("Unsupported bit depth: the WAV file "
                             f"has {bit_depth}-bit floating-point data.")
    else:
        _raise_bad_format(format_tag)

    start = fid.tell()
    if not mmap:
        try:
            count = size if dtype == 'V1' else n_samples
            data = numpy.fromfile(fid, dtype=dtype, count=count)
        except io.UnsupportedOperation:  # not a C-like file
            fid.seek(start, 0)  # just in case it seeked, though it shouldn't
            data = numpy.frombuffer(fid.read(size), dtype=dtype)

        if dtype == 'V1':
            # Rearrange raw bytes into smallest compatible numpy dtype
            dt = numpy.int32 if bytes_per_sample == 3 else numpy.int64
            a = numpy.zeros((len(data) // bytes_per_sample, dt().itemsize),
                            dtype='V1')
            a[:, -bytes_per_sample:] = data.reshape((-1, bytes_per_sample))
            data = a.view(dt).reshape(a.shape[:-1])
    else:
        if bytes_per_sample in {1, 2, 4, 8}:
            start = fid.tell()
            data = numpy.memmap(fid, dtype=dtype, mode='c', offset=start,
                                shape=(n_samples,))
            fid.seek(start + size)
        else:
            raise ValueError("mmap=True not compatible with "
                             f"{bytes_per_sample}-byte container size.")

    _handle_pad_byte(fid, size)

    if channels > 1:
        data = data.reshape(-1, channels)
    return data


def _skip_unknown_chunk(fid, is_big_endian):
    if is_big_endian:
        fmt = '>I'
    else:
        fmt = '<I'

    data = fid.read(4)
    # call unpack() and seek() only if we have really read data from file
    # otherwise empty read at the end of the file would trigger
    # unnecessary exception at unpack() call
    # in case data equals somehow to 0, there is no need for seek() anyway
    if data:
        size = struct.unpack(fmt, data)[0]
        fid.seek(size, 1)
        _handle_pad_byte(fid, size)


def _read_riff_chunk(fid):
    str1 = fid.read(4)  # File signature
    if str1 == b'RIFF':
        is_big_endian = False
        fmt = '<I'
    elif str1 == b'RIFX':
        is_big_endian = True
        fmt = '>I'
    else:
        # There are also .wav files with "FFIR" or "XFIR" signatures?
        raise ValueError(f"File format {repr(str1)} not understood. Only "
                         "'RIFF' and 'RIFX' supported.")

    # Size of entire file
    file_size = struct.unpack(fmt, fid.read(4))[0] + 8

    str2 = fid.read(4)
    if str2 != b'WAVE':
        raise ValueError(f"Not a WAV file. RIFF form type is {repr(str2)}.")

    return file_size, is_big_endian


def _handle_pad_byte(fid, size):
    # "If the chunk size is an odd number of bytes, a pad byte with value zero
    # is written after ckData." So we need to seek past this after each chunk.
    if size % 2:
        fid.seek(1, 1)


def read(filename, mmap=False):
    if hasattr(filename, 'read'):
        fid = filename
        mmap = False
    else:
        fid = open(filename, 'rb')

    try:
        file_size, is_big_endian = _read_riff_chunk(fid)
        fmt_chunk_received = False
        data_chunk_received = False
        while fid.tell() < file_size:
            # read the next chunk
            chunk_id = fid.read(4)

            if not chunk_id:
                if data_chunk_received:
                    # End of file but data successfully read
                    warnings.warn(
                        "Reached EOF prematurely; finished at {:d} bytes, "
                        "expected {:d} bytes from header."
                        .format(fid.tell(), file_size),
                        WavFileWarning, stacklevel=2)
                    break
                else:
                    raise ValueError("Unexpected end of file.")
            elif len(chunk_id) < 4:
                msg = f"Incomplete chunk ID: {repr(chunk_id)}"
                # If we have the data, ignore the broken chunk
                if fmt_chunk_received and data_chunk_received:
                    warnings.warn(msg + ", ignoring it.", WavFileWarning,
                                  stacklevel=2)
                else:
                    raise ValueError(msg)

            if chunk_id == b'fmt ':
                fmt_chunk_received = True
                fmt_chunk = _read_fmt_chunk(fid, is_big_endian)
                format_tag, channels, fs = fmt_chunk[1:4]
                bit_depth = fmt_chunk[6]
                block_align = fmt_chunk[5]
            elif chunk_id == b'fact':
                _skip_unknown_chunk(fid, is_big_endian)
            elif chunk_id == b'data':
                data_chunk_received = True
                if not fmt_chunk_received:
                    raise ValueError("No fmt chunk before data")
                data = _read_data_chunk(fid, format_tag, channels, bit_depth,
                                        is_big_endian, block_align, mmap)
            elif chunk_id == b'LIST':
                # Someday this could be handled properly but for now skip it
                _skip_unknown_chunk(fid, is_big_endian)
            elif chunk_id in {b'JUNK', b'Fake'}:
                # Skip alignment chunks without warning
                _skip_unknown_chunk(fid, is_big_endian)
            else:
                warnings.warn("Chunk (non-data) not understood, skipping it.",
                              WavFileWarning, stacklevel=2)
                _skip_unknown_chunk(fid, is_big_endian)
    finally:
        if not hasattr(filename, 'read'):
            fid.close()
        else:
            fid.seek(0)

    return fs, data


def write(filename, rate, data):
    if hasattr(filename, 'write'):
        fid = filename
    else:
        fid = open(filename, 'wb')

    fs = rate

    try:
        dkind = data.dtype.kind
        if not (dkind == 'i' or dkind == 'f' or (dkind == 'u' and
                                                 data.dtype.itemsize == 1)):
            raise ValueError("Unsupported data type '%s'" % data.dtype)

        header_data = b''

        header_data += b'RIFF'
        header_data += b'\x00\x00\x00\x00'
        header_data += b'WAVE'

        # fmt chunk
        header_data += b'fmt '
        if dkind == 'f':
            format_tag = WAVE_FORMAT.IEEE_FLOAT
        else:
            format_tag = WAVE_FORMAT.PCM
        if data.ndim == 1:
            channels = 1
        else:
            channels = data.shape[1]
        bit_depth = data.dtype.itemsize * 8
        bytes_per_second = fs*(bit_depth // 8)*channels
        block_align = channels * (bit_depth // 8)

        fmt_chunk_data = struct.pack('<HHIIHH', format_tag, channels, fs,
                                     bytes_per_second, block_align, bit_depth)
        if not (dkind == 'i' or dkind == 'u'):
            # add cbSize field for non-PCM files
            fmt_chunk_data += b'\x00\x00'

        header_data += struct.pack('<I', len(fmt_chunk_data))
        header_data += fmt_chunk_data

        # fact chunk (non-PCM files)
        if not (dkind == 'i' or dkind == 'u'):
            header_data += b'fact'
            header_data += struct.pack('<II', 4, data.shape[0])

        # check data size (needs to be immediately before the data chunk)
        if ((len(header_data)-4-4) + (4+4+data.nbytes)) > 0xFFFFFFFF:
            raise ValueError("Data exceeds wave file size limit")

        fid.write(header_data)

        # data chunk
        fid.write(b'data')
        fid.write(struct.pack('<I', data.nbytes))
        if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and
                                           sys.byteorder == 'big'):
            data = data.byteswap()
        _array_tofile(fid, data)

        # Determine file size and place it in correct
        #  position at start of the file.
        size = fid.tell()
        fid.seek(4)
        fid.write(struct.pack('<I', size-8))

    finally:
        if not hasattr(filename, 'write'):
            fid.close()
        else:
            fid.seek(0)


def _array_tofile(fid, data):
    # ravel gives a c-contiguous buffer
    fid.write(data.ravel().view('b').data)
