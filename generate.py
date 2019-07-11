import png


from dataclasses import dataclass
from typing import List, Dict, Tuple
from toke import tokenize_line, classify_line
from random import choice


Color = Tuple[int, int, int]


def paddedarray_from_string(s, length=80, solid_bars=False):
    if len(s) > length:
        s = s[:length]
    s = s.ljust(length)

    s1 = ""
    multiplier = 2
    for i in s:
        for _ in range(multiplier):
            s1 += i

    top = [[0 for _ in range(length * multiplier)] for _ in range(1)]

    if solid_bars:
        arr = []
        for _ in range(2):
            val = []
            dirty = False
            for i in range(len(s1)):
                if not s1[i] == "\n" and not s1[i] == " ":
                    dirty = True
                    val.append(1)
                elif dirty and s1[i:-1].rstrip() != "":
                    val.append(1)
                else:
                    val.append(0)
            arr.append(val)
    else:
        arr = [[0 if i == "\n" or i == " " else 1 for i in s1] for _ in range(2)]

    return top + arr  # + bottom


def bitarray_from_string(s, length=80):
    if len(s) > length:
        s = s[:length]
    s = s.ljust(length)

    return [0 if i == "\n" or i == " " else 1 for i in s]


@dataclass
class ImgColor:
    colors: List[Color]
    assignment: str

    def get(self):
        if self.assignment == 'random':
            return choice(colors)
        elif self.assignment == 'iterate':
            if not hasattr(self, 'n'):
                self.n = 0
            val = self.colors[self.n % len(self.colors)]
            self.n += 1
            return val
        else:
            raise Exception("assignment value incorrect")


@dataclass
class ImgGenerator:
    token_type: str
    colors: List[Color]
    color_dict: Dict[str, Color]
    color_assignment: str
    solid_bars: bool
    line_length: int

    def generate_from_file(self, fin, fout):
        if not hasattr(self, 'color_gen'):
            self.color_gen = ImgColor(self.colors, self.color_assignment)

        color_array = []
        background = (55, 55, 55)
        for line in fin.readlines():
            if self.token_type == 'classify':
                line_token = classify_line(line, "pyclassifications.json")
            elif self.token_type == 'initial':
                line_token = tokenize_line(line)[0] if tokenize_line(line) else None
            else:
                raise Exception('token_type incorrect')

            if line_token not in self.color_dict:
                self.color_dict[line_token] = self.color_gen.get()

            for array in paddedarray_from_string(line, solid_bars=self.solid_bars, length=self.line_length):
                color_array.append([self.color_dict[line_token] if i == 1 else background for i in array])
        bottom = [0 for _ in range(self.line_length * 2)]
        color_array.append([background for _ in bottom])
        img = png.from_array(color_array, mode="RGB")
        img.save(fout)


if __name__ == "__main__":
    colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0), (200, 0, 200), (0, 200, 200)]
    kwargs = {'token_type': 'classify', 'colors': colors, 'color_dict': {None: (200, 200, 200)}, 'color_assignment': 'random', 'solid_bars': False, 'line_length': 80}
    img_gen = ImgGenerator(**kwargs)
    with open('generate.py', 'r') as f:
        img_gen.generate_from_file(f, 'test.png')
