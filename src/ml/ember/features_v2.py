#!/usr/bin/env python3
"""
EMBER Feature Extractor (Modern)

Compatible with:
- Python 3.14
- NumPy 2.x
- LIEF 0.17+
- scikit-learn 1.7+

This is a modernized implementation of the original EMBER feature extractor.
Feature definitions are intentionally preserved.
"""

import hashlib
import json
import os
import re

import lief
import numpy as np
from sklearn.feature_extraction import FeatureHasher


# ------------------------------------------------------------------
# Compatibility
# ------------------------------------------------------------------

# NumPy compatibility
if not hasattr(np, "int"):
    np.int = np.int32

if not hasattr(np, "bool"):
    np.bool = bool

if not hasattr(np, "float"):
    np.float = float


# LIEF version info
LIEF_VERSION = tuple(map(int, lief.__version__.split("-")[0].split(".")))

LIEF_EXPORT_OBJECT = LIEF_VERSION >= (0, 10)
LIEF_HAS_SIGNATURE = LIEF_VERSION >= (0, 11)


def parse_pe(bytez):
    """
    Compatible PE parser for old/new LIEF versions.
    """
    try:
        return lief.PE.parse(bytez)
    except TypeError:
        return lief.PE.parse(list(bytez))
    except Exception:
        return None


# ------------------------------------------------------------------
# Base Feature Class
# ------------------------------------------------------------------

class FeatureType:

    name = ""
    dim = 0

    def raw_features(self, bytez, lief_binary):
        raise NotImplementedError

    def process_raw_features(self, raw_obj):
        raise NotImplementedError

    def feature_vector(self, bytez, lief_binary):
        return self.process_raw_features(
            self.raw_features(bytez, lief_binary)
        )
class ByteHistogram(FeatureType):

    name = "histogram"
    dim = 256

    def raw_features(self, bytez, lief_binary):
        counts = np.bincount(
            np.frombuffer(bytez, dtype=np.uint8),
            minlength=256
        )
        return counts.tolist()

    def process_raw_features(self, raw_obj):
        counts = np.asarray(raw_obj, dtype=np.float32)

        total = counts.sum()

        if total == 0:
            return counts

        return counts / total


class ByteEntropyHistogram(FeatureType):

    name = "byteentropy"
    dim = 256

    def __init__(self, step=1024, window=2048):
        self.window = window
        self.step = step

    def _entropy_bin_counts(self, block):

        c = np.bincount(
            block >> 4,
            minlength=16
        )

        p = c.astype(np.float32) / self.window

        nz = np.where(c)[0]

        H = np.sum(
            -p[nz] * np.log2(p[nz])
        ) * 2

        Hbin = int(H * 2)

        if Hbin == 16:
            Hbin = 15

        return Hbin, c

    def raw_features(self, bytez, lief_binary):

        output = np.zeros(
            (16, 16),
            dtype=np.int32
        )

        a = np.frombuffer(
            bytez,
            dtype=np.uint8
        )

        if a.size < self.window:

            Hbin, c = self._entropy_bin_counts(a)

            output[Hbin] += c

        else:

            shape = (
                a.shape[:-1]
                + (a.shape[-1] - self.window + 1,
                   self.window)
            )

            strides = (
                a.strides +
                (a.strides[-1],)
            )

            blocks = np.lib.stride_tricks.as_strided(
                a,
                shape=shape,
                strides=strides
            )[::self.step]

            for block in blocks:

                Hbin, c = self._entropy_bin_counts(block)

                output[Hbin] += c

        return output.flatten().tolist()

    def process_raw_features(self, raw_obj):

        counts = np.asarray(
            raw_obj,
            dtype=np.float32
        )

        total = counts.sum()

        if total == 0:
            return counts

        return counts / total
    
class SectionInfo(FeatureType):
    """
    Section information.

    Generates:
        • General section statistics
        • Section size hash
        • Section entropy hash
        • Section virtual size hash
        • Entry section hash
        • Entry section characteristics hash
    """

    name = "section"
    dim = 255

    def __init__(self):
        super().__init__()

    @staticmethod
    def _properties(section):
        try:
            return [
                str(x).split(".")[-1]
                for x in section.characteristics_lists
            ]
        except Exception:
            return []

    def raw_features(self, bytez, lief_binary):
        if lief_binary is None:
            return {
                "entry": "",
                "sections": []
            }

        entry_section = ""

        try:
            ep = lief_binary.entrypoint

            imagebase = getattr(
                lief_binary,
                "imagebase",
                0
            )

            rva = ep - imagebase

            sec = lief_binary.section_from_rva(rva)

            if sec is not None:
                entry_section = sec.name

        except Exception:
            pass

        if entry_section == "":
            for sec in lief_binary.sections:
                props = self._properties(sec)
                if "MEM_EXECUTE" in props:
                    entry_section = sec.name
                    break

        sections = []
        for sec in lief_binary.sections:
            sections.append({
                "name": sec.name,
                "size": sec.size,
                "entropy": sec.entropy,
                "vsize": sec.virtual_size,
                "props": self._properties(sec)
            })

        return {
            "entry": entry_section,
            "sections": sections
        }

    def process_raw_features(self, raw_obj):
        sections = raw_obj["sections"]

        general = [
            len(sections),
            sum(
                1
                for s in sections
                if s["size"] == 0
            ),
            sum(
                1
                for s in sections
                if s["name"] == ""
            ),
            sum(
                1
                for s in sections
                if (
                    "MEM_READ" in s["props"]
                    and
                    "MEM_EXECUTE" in s["props"]
                )
            ),
            sum(
                1
                for s in sections
                if "MEM_WRITE" in s["props"]
            )
        ]

        section_sizes = [
            (s["name"], s["size"])
            for s in sections
        ]

        section_sizes_hashed = FeatureHasher(
            50,
            input_type="pair"
        ).transform(
            [section_sizes]
        ).toarray()[0]

        section_entropy = [
            (s["name"], s["entropy"])
            for s in sections
        ]

        section_entropy_hashed = FeatureHasher(
            50,
            input_type="pair"
        ).transform(
            [section_entropy]
        ).toarray()[0]

        section_vsize = [
            (s["name"], s["vsize"])
            for s in sections
        ]

        section_vsize_hashed = FeatureHasher(
            50,
            input_type="pair"
        ).transform(
            [section_vsize]
        ).toarray()[0]

        entry = raw_obj["entry"]

        if isinstance(entry, str):
            entry = [entry]

        entry_name_hashed = FeatureHasher(
            50,
            input_type="string"
        ).transform(
            [entry]
        ).toarray()[0]

        characteristics = [
            p
            for s in sections
            for p in s["props"]
            if s["name"] == raw_obj["entry"]
        ]

        characteristics_hashed = FeatureHasher(
            50,
            input_type="string"
        ).transform(
            [characteristics]
        ).toarray()[0]

        return np.hstack([
            general,
            section_sizes_hashed,
            section_entropy_hashed,
            section_vsize_hashed,
            entry_name_hashed,
            characteristics_hashed
        ]).astype(np.float32)

class ImportsInfo(FeatureType):
    """
    Imported DLLs and imported APIs.
    Produces a 1280-dimensional hashed feature vector.
    """

    name = "imports"
    dim = 1280

    def __init__(self):
        super().__init__()

    def raw_features(self, bytez, lief_binary):

        imports = {}

        if lief_binary is None:
            return imports

        try:
            for lib in lief_binary.imports:

                libname = lib.name or ""

                if libname not in imports:
                    imports[libname] = []

                for entry in lib.entries:

                    try:

                        if entry.is_ordinal:

                            imports[libname].append(
                                f"ordinal{entry.ordinal}"
                            )

                        else:

                            if entry.name:

                                imports[libname].append(
                                    entry.name[:10000]
                                )

                    except Exception:
                        continue

        except Exception:
            pass

        return imports

    def process_raw_features(self, raw_obj):

        libraries = list(set([l.lower() for l in raw_obj.keys()]))

        libraries_hashed = FeatureHasher(
            256,
            input_type="string"
        ).transform(
            [libraries]
        ).toarray()[0]

        imports = []

        for lib, funcs in raw_obj.items():

            for fn in funcs:

                imports.append(
                    f"{lib}:{fn}"
                )

        imports_hashed = FeatureHasher(
            1024,
            input_type="string"
        ).transform(
            [imports]
        ).toarray()[0]

        return np.hstack([
            libraries_hashed,
            imports_hashed
        ]).astype(np.float32)

class ExportsInfo(FeatureType):
    """
    Exported functions.
    """

    name = "exports"

    dim = 128

    def __init__(self):
        super().__init__()

    def raw_features(self, bytez, lief_binary):

        if lief_binary is None:
            return []

        exports = []

        try:

            for e in lief_binary.exported_functions:

                if hasattr(e, "name"):

                    exports.append(
                        (e.name or "")[:10000]
                    )

                else:

                    exports.append(
                        str(e)[:10000]
                    )

        except Exception:
            pass

        return exports

    def process_raw_features(self, raw_obj):

        hashed = FeatureHasher(
            128,
            input_type="string"
        ).transform(
            [raw_obj]
        ).toarray()[0]

        return hashed.astype(np.float32)

class GeneralFileInfo(FeatureType):
    """
    General information about the PE file.
    """

    name = "general"
    dim = 10

    def __init__(self):
        super().__init__()

    def raw_features(self, bytez, lief_binary):

        if lief_binary is None:
            return {
                "size": len(bytez),
                "vsize": 0,
                "has_debug": 0,
                "exports": 0,
                "imports": 0,
                "has_relocations": 0,
                "has_resources": 0,
                "has_signature": 0,
                "has_tls": 0,
                "symbols": 0,
            }

        has_signature = 0

        try:
            if hasattr(lief_binary, "has_signatures"):
                has_signature = int(lief_binary.has_signatures)
            elif hasattr(lief_binary, "has_signature"):
                has_signature = int(lief_binary.has_signature)
        except Exception:
            has_signature = 0

        return {
            "size": len(bytez),
            "vsize": getattr(lief_binary, "virtual_size", 0),
            "has_debug": int(getattr(lief_binary, "has_debug", False)),
            "exports": len(getattr(lief_binary, "exported_functions", [])),
            "imports": len(getattr(lief_binary, "imported_functions", [])),
            "has_relocations": int(getattr(lief_binary, "has_relocations", False)),
            "has_resources": int(getattr(lief_binary, "has_resources", False)),
            "has_signature": has_signature,
            "has_tls": int(getattr(lief_binary, "has_tls", False)),
            "symbols": len(getattr(lief_binary, "symbols", [])),
        }

    def process_raw_features(self, raw_obj):

        return np.asarray([
            raw_obj["size"],
            raw_obj["vsize"],
            raw_obj["has_debug"],
            raw_obj["exports"],
            raw_obj["imports"],
            raw_obj["has_relocations"],
            raw_obj["has_resources"],
            raw_obj["has_signature"],
            raw_obj["has_tls"],
            raw_obj["symbols"],
        ], dtype=np.float32)

    class HeaderFileInfo(FeatureType):
        ''' Machine, architecure, OS, linker and other information extracted from header '''

        name = 'header'
        dim = 62

        def __init__(self):
            super().__init__()

        def raw_features(self, bytez, lief_binary):
            raw_obj = {}
            raw_obj['coff'] = {'timestamp': 0, 'machine': "", 'characteristics': []}
            raw_obj['optional'] = {
                'subsystem': "",
                'dll_characteristics': [],
                'magic': "",
                'major_image_version': 0,
                'minor_image_version': 0,
                'major_linker_version': 0,
                'minor_linker_version': 0,
                'major_operating_system_version': 0,
                'minor_operating_system_version': 0,
                'major_subsystem_version': 0,
                'minor_subsystem_version': 0,
                'sizeof_code': 0,
                'sizeof_headers': 0,
                'sizeof_heap_commit': 0
            }
            if lief_binary is None:
                return raw_obj

            raw_obj['coff']['timestamp'] = lief_binary.header.time_date_stamps
            raw_obj['coff']['machine'] = str(lief_binary.header.machine).split('.')[-1]
            raw_obj['coff']['characteristics'] = [str(c).split('.')[-1] for c in lief_binary.header.characteristics_list]
            raw_obj['optional']['subsystem'] = str(lief_binary.optional_header.subsystem).split('.')[-1]
            raw_obj['optional']['dll_characteristics'] = [
                str(c).split('.')[-1] for c in lief_binary.optional_header.dll_characteristics_lists
            ]
            raw_obj['optional']['magic'] = str(lief_binary.optional_header.magic).split('.')[-1]
            raw_obj['optional']['major_image_version'] = lief_binary.optional_header.major_image_version
            raw_obj['optional']['minor_image_version'] = lief_binary.optional_header.minor_image_version
            raw_obj['optional']['major_linker_version'] = lief_binary.optional_header.major_linker_version
            raw_obj['optional']['minor_linker_version'] = lief_binary.optional_header.minor_linker_version
            raw_obj['optional'][
                'major_operating_system_version'] = lief_binary.optional_header.major_operating_system_version
            raw_obj['optional'][
                'minor_operating_system_version'] = lief_binary.optional_header.minor_operating_system_version
            raw_obj['optional']['major_subsystem_version'] = lief_binary.optional_header.major_subsystem_version
            raw_obj['optional']['minor_subsystem_version'] = lief_binary.optional_header.minor_subsystem_version
            raw_obj['optional']['sizeof_code'] = lief_binary.optional_header.sizeof_code
            raw_obj['optional']['sizeof_headers'] = lief_binary.optional_header.sizeof_headers
            raw_obj['optional']['sizeof_heap_commit'] = lief_binary.optional_header.sizeof_heap_commit
            return raw_obj

        def process_raw_features(self, raw_obj):
            return np.hstack([
                raw_obj['coff']['timestamp'],
                FeatureHasher(10, input_type="string").transform([[raw_obj['coff']['machine']]]).toarray()[0],
                FeatureHasher(
                    10,
                    input_type="string"
                ).transform(
                    [list(raw_obj["coff"]["characteristics"])]
                ).toarray()[0],
                FeatureHasher(10, input_type="string").transform([[raw_obj['optional']['subsystem']]]).toarray()[0],
                FeatureHasher(
                    10,
                    input_type="string"
                ).transform(
                    [list(raw_obj["optional"]["dll_characteristics"])]
                ).toarray()[0],
                FeatureHasher(10, input_type="string").transform([[raw_obj['optional']['magic']]]).toarray()[0],
                raw_obj['optional']['major_image_version'],
                raw_obj['optional']['minor_image_version'],
                raw_obj['optional']['major_linker_version'],
                raw_obj['optional']['minor_linker_version'],
                raw_obj['optional']['major_operating_system_version'],
                raw_obj['optional']['minor_operating_system_version'],
                raw_obj['optional']['major_subsystem_version'],
                raw_obj['optional']['minor_subsystem_version'],
                raw_obj['optional']['sizeof_code'],
                raw_obj['optional']['sizeof_headers'],
                raw_obj['optional']['sizeof_heap_commit'],
            ]).astype(np.float32)
        


class StringExtractor(FeatureType):
    ''' Extracts strings from raw byte stream '''

    name = 'strings'
    dim = 1 + 1 + 1 + 96 + 1 + 1 + 1 + 1 + 1

    def __init__(self):
        super(FeatureType, self).__init__()
        # all consecutive runs of 0x20 - 0x7f that are 5+ characters
        self._allstrings = re.compile(b'[\x20-\x7f]{5,}')
        # occurances of the string 'C:\'.  Not actually extracting the path
        self._paths = re.compile(b'c:\\\\', re.IGNORECASE)
        # occurances of http:// or https://.  Not actually extracting the URLs
        self._urls = re.compile(b'https?://', re.IGNORECASE)
        # occurances of the string prefix HKEY_.  No actually extracting registry names
        self._registry = re.compile(b'HKEY_')
        # crude evidence of an MZ header (dropper?) somewhere in the byte stream
        self._mz = re.compile(b'MZ')

    def raw_features(self, bytez, lief_binary):
        allstrings = self._allstrings.findall(bytez)
        if allstrings:
            # statistics about strings:
            string_lengths = [len(s) for s in allstrings]
            avlength = sum(string_lengths) / len(string_lengths)
            # map printable characters 0x20 - 0x7f to an int array consisting of 0-95, inclusive
            as_shifted_string = [b - ord(b'\x20') for b in b''.join(allstrings)]
            c = np.bincount(as_shifted_string, minlength=96)  # histogram count
            # distribution of characters in printable strings
            csum = c.sum()
            p = c.astype(np.float32) / csum
            wh = np.where(c)[0]
            H = np.sum(-p[wh] * np.log2(p[wh]))  # entropy
        else:
            avlength = 0
            c = np.zeros((96,), dtype=np.float32)
            H = 0
            csum = 0

        return {
            'numstrings': len(allstrings),
            'avlength': avlength,
            'printabledist': c.tolist(),  # store non-normalized histogram
            'printables': int(csum),
            'entropy': float(H),
            'paths': len(self._paths.findall(bytez)),
            'urls': len(self._urls.findall(bytez)),
            'registry': len(self._registry.findall(bytez)),
            'MZ': len(self._mz.findall(bytez))
        }

    def process_raw_features(self, raw_obj):
        hist_divisor = float(raw_obj['printables']) if raw_obj['printables'] > 0 else 1.0
        return np.hstack([
            raw_obj['numstrings'], raw_obj['avlength'], raw_obj['printables'],
            np.asarray(raw_obj['printabledist']) / hist_divisor, raw_obj['entropy'], raw_obj['paths'], raw_obj['urls'],
            raw_obj['registry'], raw_obj['MZ']
        ]).astype(np.float32)


class DataDirectories(FeatureType):
    ''' Extracts size and virtual address of the first 15 data directories '''

    name = 'datadirectories'
    dim = 15 * 2

    def __init__(self):
        super(FeatureType, self).__init__()
        self._name_order = [
            "EXPORT_TABLE", "IMPORT_TABLE", "RESOURCE_TABLE", "EXCEPTION_TABLE", "CERTIFICATE_TABLE",
            "BASE_RELOCATION_TABLE", "DEBUG", "ARCHITECTURE", "GLOBAL_PTR", "TLS_TABLE", "LOAD_CONFIG_TABLE",
            "BOUND_IMPORT", "IAT", "DELAY_IMPORT_DESCRIPTOR", "CLR_RUNTIME_HEADER"
        ]

    def raw_features(self, bytez, lief_binary):
        output = []
        if lief_binary is None:
            return output

        for data_directory in lief_binary.data_directories:
            output.append({
                "name": str(data_directory.type).replace("DATA_DIRECTORY.", ""),
                "size": data_directory.size,
                "virtual_address": data_directory.rva
            })
        return output

    def process_raw_features(self, raw_obj):
        features = np.zeros(2 * len(self._name_order), dtype=np.float32)
        for i in range(len(self._name_order)):
            if i < len(raw_obj):
                features[2 * i] = raw_obj[i]["size"]
                features[2 * i + 1] = raw_obj[i]["virtual_address"]
        return features


class PEFeatureExtractor(object):
    ''' Extract useful features from a PE file, and return as a vector of fixed size. '''

    def __init__(self, feature_version=2, print_feature_warning=True, features_file=''):
        self.features = []
        features = {
                    'ByteHistogram': ByteHistogram(),
                    'ByteEntropyHistogram': ByteEntropyHistogram(),
                    'StringExtractor': StringExtractor(),
                    'GeneralFileInfo': GeneralFileInfo(),
                    'HeaderFileInfo': HeaderFileInfo(),
                    'SectionInfo': SectionInfo(),
                    'ImportsInfo': ImportsInfo(),
                    'ExportsInfo': ExportsInfo()
            }

        if os.path.exists(features_file):
            with open(features_file, encoding='utf8') as f:
                x = json.load(f)
                self.features = [features[feature] for feature in x['features'] if feature in features]
        else:
            self.features = list(features.values())

        if feature_version == 1:
            if not lief.__version__.startswith("0.8.3"):
                if print_feature_warning:
                    print(f"WARNING: EMBER feature version 1 were computed using lief version 0.8.3-18d5b75")
                    print(f"WARNING:   lief version {lief.__version__} found instead. There may be slight inconsistencies")
                    print(f"WARNING:   in the feature calculations.")
        elif feature_version == 2:
            self.features.append(DataDirectories())
            if not lief.__version__.startswith("0.9.0"):
                if print_feature_warning:
                    print(f"WARNING: EMBER feature version 2 were computed using lief version 0.9.0-")
                    print(f"WARNING:   lief version {lief.__version__} found instead. There may be slight inconsistencies")
                    print(f"WARNING:   in the feature calculations.")
        else:
            raise Exception(f"EMBER feature version must be 1 or 2. Not {feature_version}")
        self.dim = sum([fe.dim for fe in self.features])

    def raw_features(self, bytez):
        try:
            lief_errors = (lief.lief_errors, RuntimeError)
        except AttributeError:
            lief_errors = (
                lief.bad_format,
                lief.bad_file,
                lief.pe_error,
                lief.parser_error,
                lief.read_out_of_bound,
                RuntimeError
            )
        
        try:
            lief_binary = lief.PE.parse(bytez)
        except TypeError:
            lief_binary = lief.PE.parse(list(bytez))
        except lief_errors as e:
            print("lief error: ", str(e))
            lief_binary = None
        except Exception:  # everything else (KeyboardInterrupt, SystemExit, ValueError):
            raise

        features = {"sha256": hashlib.sha256(bytez).hexdigest()}
        features.update({fe.name: fe.raw_features(bytez, lief_binary) for fe in self.features})
        return features

    def process_raw_features(self, raw_obj):
        feature_vectors = [fe.process_raw_features(raw_obj[fe.name]) for fe in self.features]
        return np.hstack(feature_vectors).astype(np.float32)

    def feature_vector(self, bytez):
        return self.process_raw_features(self.raw_features(bytez))

