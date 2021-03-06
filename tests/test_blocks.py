from matplotlib.testing import setup
import numpy as np
import matplotlib.pyplot as plt

import pytest

import animatplot as amp
from tests.tools import animation_compare

from animatplot.blocks import Block, Title

setup()


class TestTitleBlock:
    def test_list_of_str(self):
        labels = ['timestep 0', 'timestep 1']
        result = Title(labels)
        assert labels == result.titles
        assert len(result) == 2

    def test_invalid_input(self):
        with pytest.raises(TypeError):
            Title(0)
        with pytest.raises(TypeError):
            Title([6, 7])

    def test_format_str(self):
        actual = Title('timestep {num}', num=[1, 2]).titles
        assert actual == ['timestep 1', 'timestep 2']

        actual = Title('timestep {num}', num=[1]).titles
        assert actual == ['timestep 1']

    def test_no_replacements(self):
        actual = Title('Name').titles
        assert actual == ['Name']

    def test_multiple_replacements(self):
        actual = Title('timestep {num}, max density {n}',
                       num=[1, 2], n=[500, 10]).titles
        expected = ['timestep {num}, max density {n}'.format(num=1, n=500),
                    'timestep {num}, max density {n}'.format(num=2, n=10)]
        assert actual == expected

    def test_string_formatting(self):
        actual = Title('timestep {values:.2f}', values=[5e7]).titles
        assert actual == ['timestep 50000000.00']

    def test_format_str_numpy_arrays(self):
        actual = Title('timestep {num}', num=np.array([1, 2])).titles
        assert actual == ['timestep 1', 'timestep 2']

    # Hypothesis test that the strings are always formatted correctly?

    def test_text(self):
        # TODO test that the right type of object is produced?
        title_block = Title('timestep {num}', num=[1, 2])

        ax = plt.gca()
        assert ax.get_title() == 'timestep 1'
        title_block._update(1)
        assert ax.get_title() == 'timestep 2'
        plt.close('all')

    def test_mpl_kwargs(self):
        expected = {'loc': 'left', 'fontstyle': 'italic'}
        actual = Title('timestep {num}', num=[1, 2], **expected)
        assert actual._mpl_kwargs == expected


class TestComparisons:
    @animation_compare(baseline_images='Blocks/Line', nframes=5)
    def test_Line(self):
        x = np.linspace(0, 2*np.pi, 20)
        t = np.linspace(0, 2*np.pi, 5)

        X, T = np.meshgrid(x, t)
        Y = np.sin(X+T)
        block = amp.blocks.Line(X, Y)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Pcolormesh', nframes=3)
    def test_Pcolormesh(self):
        x = np.linspace(-2*np.pi, 2*np.pi, 100)
        t = np.linspace(0, 2*np.pi, 3)

        X, Y, T = np.meshgrid(x, x, t)
        Z = np.sin(X**2+Y**2-T)

        block = amp.blocks.Pcolormesh(X[:, :, 0], Y[:, :, 0], Z, t_axis=2)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Imshow', nframes=3)
    def test_Imshow(self):
        x = np.linspace(0, 1, 10)
        X, Y = np.meshgrid(x, x)

        U = []
        for i in range(3):
            U.append(X**2+Y**2+i)

        block = amp.blocks.Imshow(U)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Quiver', nframes=4)
    def test_Quiver(self):
        x = np.linspace(0, 1, 10)
        X, Y = np.meshgrid(x, x)

        U, V = [], []
        for i in range(4):
            U.append(X**2+Y**2+i)
            V.append(X**2+Y**2+i)

        block = amp.blocks.Quiver(X, Y, U, V)
        return amp.Animation([block])

    @animation_compare(baseline_images='Blocks/Nuke', nframes=3)
    def test_Nuke(self):
        ax = plt.gca()
        sizes = []

        def animate(i):
            sizes.append(i+1)
            ax.set_aspect("equal")
            ax.pie(sizes)
        block = amp.blocks.Nuke(animate, length=3, ax=ax)
        return amp.Animation([block])
