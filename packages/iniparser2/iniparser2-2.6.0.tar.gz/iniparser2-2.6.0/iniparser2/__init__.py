"""An INI parser or a Config parser"""

import re
import io
import ast

__version__ = "2.6.0"
__all__ = ["ParsingError", "INI", "PropertyError", "DuplicateError", "SectionError"]


class ParsingError(Exception):
    """base exception for parsing error"""

    def __init__(self, message, line, text=""):
        self.message = message
        self.text = text
        self.line = line
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}, {self.text} [line {self.line}]"


class ParseDuplicateError(ParsingError):
    """dupe error raised while parsing"""


class PropertyError(Exception):
    pass


class DuplicateError(Exception):
    pass


class SectionError(Exception):
    pass


class ParsePropertyError(ParsingError):
    """raised when failed parsing property"""


class ParseSectionError(ParsingError):
    """raised when failed parsing section"""


class INI:
    """main class for parsing ini"""

    # parser patterns
    _key_pattern = re.compile(r"^\s*(\#\;)|((.*)\s[#;])")
    _val_pattern = re.compile(r"((.)^[#;]$)|\s([#;])")
    _section_pattern = re.compile(r"^\s*\[(.*)\]\s*(.*)$")
    _seccom_pattern = re.compile(r"(.*)\s[#;]")
    _comment_pattern = re.compile(r"^[#;]")

    # converter patterns
    _float_pattern = re.compile(r"^[-]?(\d+[.])\d+$")
    _int_pattern = re.compile(r"^[-]?\d+$")
    _str_pattern = re.compile(r'".*(?<!\\)(?:\\\\)*"')

    LITERAL_TYPES = (int, float, bool, str)
    BOOL_STATES = {
        "true": True,
        "1": True,
        "on": True,
        "yes": True,
        "false": False,
        "0": False,
        "off": False,
        "no": False,
    }

    def __init__(self, delimiter=("=",), convert_property=False):
        self.ini = dict()
        self.delimiter = delimiter
        self.convert_property = convert_property
        self._sections = list()

        self._property_pattern = re.compile(
            rf"^\s*(.*)\s*[{r'|'.join(delimiter)}]\s*(.*)\s*$"
        )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return self

    def __str__(self):
        return f"{self.ini}"

    def __iter__(self):
        yield from self.ini

    def __getitem__(self, key):
        return self.ini[key]

    def __setitem__(self, key, value):
        if type(value) not in self.LITERAL_TYPES and value is not None:
            raise ValueError("value must be a literal or NoneType")

        if key in self.ini:
            if isinstance(self.ini[key], dict) and key in self._sections:
                raise SectionError("Cannot assign values to section header")

        self.ini[key] = value

    def __delitem__(self, key):
        if key in self._sections and isinstance(self.ini[key], dict):
            self._sections.remove(key)
            del self.ini[key]

        else:
            del self.ini[key]

    def update(self, dict_):
        if not isinstance(dict_, dict):
            raise TypeError("value must be a dict")

        for sect in dict_:
            if sect in self._sections and type(dict_[sect]) is not dict:
                raise SectionError(f"Cannot update section header value [{sect}]")

            if isinstance(dict_[sect], dict):
                if sect not in self._sections:
                    self._sections.append(sect)
                    self.ini.update({sect: {}})

                for opt in dict_[sect]:
                    if (
                        type(dict_[sect][opt]) not in self.LITERAL_TYPES
                        and dict_[sect][opt] is not None
                    ):
                        raise PropertyError(
                            f"value must be a literal or NoneType [{sect}][{opt}]"
                        )

                    self.ini[sect].update({opt: dict_[sect][opt]})

            else:
                if (
                    type(dict_[sect]) not in self.LITERAL_TYPES
                    and dict_[sect] is not None
                ):
                    raise PropertyError(f"value must be a literal or NoneType [{sect}]")

                self.ini.update({sect: dict_[sect]})

    def __contains__(self, item):
        return item in self.ini

    def __len__(self):
        return len(self.ini)

    def read(self, string):
        self.ini = self._parse(string)
        self._sections = []
        for prop in self.ini:
            if isinstance(self.ini[prop], dict):
                self._sections.append(prop)

    def sections(self):
        return self._sections

    def has_section(self, name):
        return name in self._sections

    def has_property(self, name, section=None):
        if section is None:
            return name in self.ini

        return name in self.ini[section]

    def read_file(self, file):
        """read sections and properties"""
        if type(file) is str:
            # file path in string
            self.ini = self._parse(open(file, "r").read())
        elif type(file) is io.TextIOWrapper:
            self.ini = self._parse(file.read())
        self._sections = []
        for prop in self.ini:
            if isinstance(self.ini[prop], dict):
                self._sections.append(prop)

    def remove_section(self, name):
        if not self.has_section(name):
            raise SectionError("section %s not found" % name)

        del self.ini[name]
        self._sections.remove(name)

    def remove_property(self, name, section=None):
        if section is None:
            if not self.has_property(name):
                raise PropertyError("property %s not found" % name)

            del self.ini[name]
        else:
            if not self.has_section(section):
                raise SectionError("section %s not found" % section)
            if not self.has_property(name, section):
                raise PropertyError(f"property {name} not found in section {section}")

            del self.ini[section][name]

    def set(self, name, value="", section=None):
        if section is None:
            self.ini.update({name: value})
        else:
            if not self.has_section(section):
                raise SectionError("section %s not found" % section)

            self.ini[section].update({name: value})

    def get(self, name, section=None):
        if section is None:
            if not self.has_property(name):
                raise PropertyError("property %s not found" % name)

            return self.ini[name]

        if not self.has_section(section):
            raise SectionError("section %s not found" % section)
        if not self.has_property(name, section):
            raise PropertyError(f"property {name} not found in section {section}")

        return self.ini[section][name]

    def get_str(self, name, section=None):
        return str(self.get(name, section))

    def get_int(self, name, section=None):
        val = self.get(name, section)
        if isinstance(val, int):
            return val

        return int(val)

    def get_float(self, name, section=None):
        val = self.get(name, section)
        if isinstance(val, float):
            return val

        return float(val)

    def get_bool(self, name, section=None):
        val = self.get(name, section)

        if isinstance(val, bool):
            return val

        val = val.lower()

        if val not in self.BOOL_STATES:
            raise TypeError("unknown bool state for: %s" % (val))

        return self.BOOL_STATES[val]

    def items(self, section=None):
        result = []

        if section is None:
            for key in self.ini:
                if not isinstance(self.ini[key], dict):
                    result.append((key, self.ini[key]))
        else:
            if not self.has_section(section):
                raise SectionError("section %s not found" % section)

            for key in self.ini[section]:
                if self.ini[section][key] is not None:
                    result.append((key, self.ini[section][key]))

        return result

    def keys(self, section=None):
        result = []

        if section is None:
            for key in self.ini:
                result.append(key)
        else:
            if not self.has_section(section):
                raise SectionError("section %s not found" % section)

            for key in self.ini[section]:
                result.append(key)

        return result

    def set_section(self, name):
        if self.has_section(name):
            raise DuplicateError("section %s already exists" % name)

        self.ini.update({name: {}})
        self._sections.append(name)

    def write(self, file):
        """write properties and sections to file"""
        dump(file, self.ini)

    def _check_comment(self, string):
        """check comment"""
        sec = self._comment_pattern.match(string)
        if sec:
            return True
        return False

    def _parse_property(self, string):
        """parse property returns property key and property value"""
        if self._check_comment(string):
            return None
        prop = self._property_pattern.findall(string)
        if not prop:
            return None
        if len(prop[0]) < 2:
            return None
        key, val = prop[0][0], prop[0][1]
        _key = self._key_pattern.match(key)
        if _key:
            return None
        val = self._val_pattern.split(val)[0]

        return key, val

    def _is_property(self, string):
        """check property"""
        if self._parse_property(string) is not None:
            return True
        return False

    def _parse_section(self, string):
        """parse section returns section name"""
        if self._check_comment(string):
            return None
        sec = self._section_pattern.findall(string)
        if not sec:
            return None
        if sec[0][1] and not self._comment_pattern.match(sec[0][1].strip()):
            return None
        _sec = self._seccom_pattern.match(sec[0][0])
        if not _sec:
            return sec[0][0]

    def _is_section(self, string):
        """check section"""
        if self._parse_section(string) is not None:
            return True
        return False

    def _parse(self, string):
        """parse ini string returns ini dictionary"""
        result = {}

        if type(string) is str:
            lines = io.StringIO(string).readlines()
        elif type(string) is io.StringIO:
            lines = string.readlines()

        prev_section = None
        prev_property = (None, {"key_only": False})

        for lineno, line in enumerate(lines):
            lineno += 1

            if not line.strip():
                continue

            if self._check_comment(line.strip()):
                continue

            if self._is_section(line.strip()):
                prev_section = self._parse_section(line.strip())

                if not prev_section:
                    raise ParseSectionError(
                        "section header does not have a name", lineno, line.strip()
                    )

                if prev_section in result:
                    raise ParseDuplicateError(
                        "section already exists", lineno, prev_section
                    )

                result.update({prev_section: {}})

            elif self._is_property(line.strip()):
                key, val = self._parse_property(line.strip())

                if not key:
                    raise ParsePropertyError(
                        "property does not have a key name", lineno, line.strip()
                    )

                prev_property = (key, {"key_only": False})

                if prev_section:
                    if prev_property[0] in result[prev_section]:
                        raise ParseDuplicateError(
                            "property already exists", lineno, prev_property[0]
                        )

                    result[prev_section].update({key.strip(): val.strip()})
                else:
                    if prev_property[0] in result:
                        raise ParseDuplicateError(
                            "property already exists", lineno, prev_property[0]
                        )

                    result.update({key.strip(): val.strip()})

            else:  # allow value only property, the dict value set to None
                if re.match(r"^\s", line):
                    if prev_section:
                        if prev_property[0]:
                            if prev_property[1]["key_only"] is False:
                                result[prev_section][prev_property[0]] += (
                                    "\n" + self._val_pattern.split(line.strip())[0]
                                )
                                continue
                    else:
                        if prev_property[0]:
                            if prev_property[1]["key_only"] is False:
                                result[prev_property[0]] += (
                                    "\n" + self._val_pattern.split(line.strip())[0]
                                )
                                continue

                if prev_section:
                    if line.strip() in result[prev_section]:
                        raise ParseDuplicateError(
                            "property already exists", lineno, line.strip()
                        )

                    key = self._val_pattern.split(line.strip())[0]
                    prev_property = (key, {"key_only": True})

                    result[prev_section].update({key: None})
                else:
                    if line.strip() in result:
                        raise ParseDuplicateError(
                            "property already exists", lineno, line.strip()
                        )
                    key = self._val_pattern.split(line.strip())[0]
                    prev_property = (key, {"key_only": True})

                    result.update({key: None})

        if self.convert_property:
            return self._convert_property(result)

        return result

    def _convert_property(self, ini_dict):
        """converter"""
        eval_codes = [
            (self._float_pattern, float),
            (self._int_pattern, int),
            (self._str_pattern, ast.literal_eval),
        ]

        for sectf in ini_dict:
            if isinstance(ini_dict[sectf], dict):
                for prop in ini_dict[sectf]:
                    for eval_code in eval_codes:
                        if type(ini_dict[sectf][prop]).__name__ != "str":
                            continue

                        if eval_code[0].match(ini_dict[sectf][prop]):
                            try:
                                ini_dict[sectf][prop] = eval_code[1](
                                    ini_dict[sectf][prop]
                                )
                            except Exception:
                                break
                            else:
                                break

                    if type(ini_dict[sectf][prop]).__name__ != "str":
                        continue

                    if ini_dict[sectf][prop].lower() == "true":
                        ini_dict[sectf][prop] = True
                    elif ini_dict[sectf][prop].lower() == "false":
                        ini_dict[sectf][prop] = False
            else:
                for eval_code in eval_codes:
                    if type(ini_dict[sectf]).__name__ != "str":
                        continue

                    if eval_code[0].match(ini_dict[sectf]):
                        try:
                            ini_dict[sectf] = eval_code[1](ini_dict[sectf])
                        except Exception:
                            break
                        else:
                            break

                if type(ini_dict[sectf]).__name__ != "str":
                    continue

                if ini_dict[sectf].lower() == "true":
                    ini_dict[sectf] = True
                elif ini_dict[sectf].lower() == "false":
                    ini_dict[sectf] = False

        return ini_dict


def dump(file, ini_dict):
    """dump a dictionary or a set to INI file format"""
    found_sect = False
    found_prop = False

    if type(file) is str:
        # file path in string
        file = open(file, "w")
    elif type(file) is not io.TextIOWrapper:
        raise IOError("file must be either file path in string or file pointer")

    for sect in ini_dict:
        if isinstance(ini_dict[sect], dict):
            if found_sect is False and found_prop is False:
                file.write(f"[{sect}]\n")
            else:
                file.write(f"\n[{sect}]\n")
            found_sect = True
            for prop in ini_dict[sect]:
                found_prop = True
                if ini_dict[sect][prop] is not None:
                    file.write(f"{prop} = {ini_dict[sect][prop]}\n")
                else:
                    file.write(f"{prop}\n")
        else:
            found_prop = True
            if ini_dict[sect] is not None:
                file.write(f"{sect} = {ini_dict[sect]}\n")
            else:
                file.write(f"{sect}\n")

    file.close()
