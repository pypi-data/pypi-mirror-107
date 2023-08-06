"""An INI parser or a Config parser"""

import re
import io
import ast

__version__ = "2.5.0"
__all__ = ["ParsingError", "INI", "PropertyError", "DuplicateError", "SectionError"]


class ParsingError(Exception):
    """base exception for parsing error"""

    def __init__(self, message, text, line):
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
    _section_pattern = re.compile(r"^\s*\[(.*)\]\s*?(.*)$")
    _comment_pattern = re.compile(r"^[#;]")

    # converter patterns
    _float_pattern = re.compile(r"^[-+]?(\d+[.])\d+$")
    _int_pattern = re.compile(r"^[-+]?\d+$")
    _str_pattern = re.compile(r'".*?(?<!\\)(?:\\\\)*?"')

    def __init__(self, delimiter=("=",), convert_property=False):
        self.ini = dict()
        self.delimiter = delimiter
        self.convert_property = convert_property
        self._sections = list()

        self._property_pattern = re.compile(
            rf"^\s*(.+?)\s*[{r'|'.join(delimiter)}]\s*(.+?)?\s*$"
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
        if type(value) not in [int, float, str, bool]:
            raise ValueError("value must be a literal")

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

    def read_file(self, filename):
        """read sections and properties"""
        self.ini = self._parse(open(filename, "r").read())
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

    def set_section(self, name):
        if self.has_section(name):
            raise DuplicateError("section %s already exists" % name)

        self.ini.update({name: {}})
        self._sections.append(name)

    def write(self, filename):
        """write properties and sections to file"""
        dump(filename, self.ini)

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
        _sec = re.match(r"(.*)\s[#]", sec[0][0])
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

        lines = io.StringIO(string).readlines()

        prev_section = None
        prev_property = (None, {'key_only': False})

        for lineno, line in enumerate(lines):
            lineno += 1

            if not line.strip():
                continue

            if self._check_comment(line.strip()):
                continue

            if self._is_section(line.strip()):
                prev_section = self._parse_section(line.strip())

                if prev_section in result:
                    raise ParseDuplicateError(
                        "section already exists", prev_section, lineno
                    )

                result.update({prev_section: {}})

            elif self._is_property(line.strip()):
                key, val = self._parse_property(line.strip())

                prev_property = (key, {"key_only": False})

                if prev_section:
                    if prev_property[0] in result[prev_section]:
                        raise ParseDuplicateError(
                            "property already exists", prev_property[0], lineno
                        )

                    result[prev_section].update({key: val.strip()})
                else:
                    if prev_property[0] in result:
                        raise ParseDuplicateError(
                            "property already exists", prev_property[0], lineno
                        )

                    result.update({key: val.strip()})

            else:  # allow value only property, the dict value set to True
                if re.match(r"^\s", line):
                    if prev_section:
                        if prev_property[0]:
                            if prev_property[1]["key_only"] is True:
                                raise ParsePropertyError(
                                    "Multiline value is not supported for key only property",
                                    prev_property[0],
                                    lineno,
                                )

                            result[prev_section][prev_property[0]] += (
                                "\n" + self._val_pattern.split(line.strip())[0]
                            )
                            continue
                    else:
                        if prev_property[0]:
                            if prev_property[1]["key_only"] is True:
                                raise ParsePropertyError(
                                    "Multiline value is not supported for key only property",
                                    prev_property[0],
                                    lineno,
                                )

                            result[prev_property[0]] += (
                                "\n" + self._val_pattern.split(line.strip())[0]
                            )
                            continue

                if prev_section:
                    if line.strip() in result[prev_section]:
                        raise ParseDuplicateError(
                            "property already exists", line.strip(), lineno
                        )

                    key = self._val_pattern.split(line.strip())[0]
                    prev_property = (key, {"key_only": True})

                    result[prev_section].update({key: True})
                else:
                    if line.strip() in result:
                        raise ParseDuplicateError(
                            "property already exists", line.strip(), lineno
                        )

                    key = self._val_pattern.split(line.strip())[0]
                    prev_property = (key, {"key_only": True})

                    result.update({key: True})

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
                                ini_dict[sectf][prop] = eval_code[1](ini_dict[sectf][prop])
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


def dump(filename, ini_dict):
    """dump a dictionary or a set to INI file format"""
    with open(filename, "w+") as file:
        for sect in ini_dict:
            if isinstance(ini_dict[sect], dict):
                file.write(f"[{sect}]\n")
                for prop in ini_dict[sect]:
                    file.write(f"{prop} = {ini_dict[sect][prop]}\n")
            else:
                file.write(f"{sect} = {ini_dict[sect]}\n")
